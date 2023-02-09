import netCDF4
import xarray as xr
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
from pandas import DataFrame
import sys
import json
import datetime
import urllib.request
import urllib.error
import tarfile
import time

import pysftp




#import cdsapi
from flood_model.dynamicDataDb import DatabaseManager
from flood_model.settings import *
try:
    from flood_model.secrets import *
except ImportError:
    print('No secrets file found.')
import os
import logging
logger = logging.getLogger(__name__)


class GlossisData:

    def __init__(self, leadTimeLabel, leadTimeValue, countryCodeISO3, glossis_stations, district_mapping):
        #self.db = DatabaseManager(leadTimeLabel, countryCodeISO3)
        self.leadTimeLabel = leadTimeLabel
        self.leadTimeValue = leadTimeValue
        self.countryCodeISO3 = countryCodeISO3
        self.GLOSSIS_FILENAME=SETTINGS[countryCodeISO3]['GLOSSIS_FILENAME']
        self.GLOSSIS_FTP=SETTINGS[countryCodeISO3]['GLOSSIS_FTP']
        self.TRIGGER_LEVELS=SETTINGS[countryCodeISO3]['TRIGGER_LEVELS']
        self.inputPath = PIPELINE_DATA+'input/glossis/'
        self.GlossisInputPath = PIPELINE_DATA+'input/glossis/'
        self.triggerPerDay = PIPELINE_OUTPUT + \
            'triggers_rp_per_station/trigger_per_day_' + countryCodeISO3 + '.json'
        self.extractedGlossisDir = PIPELINE_OUTPUT + 'glossis_extraction'
        if not os.path.exists(self.extractedGlossisDir):
            os.makedirs(self.extractedGlossisDir)
        self.extractedGlossisPath = PIPELINE_OUTPUT + \
            'glossis_extraction/glossis_forecast_' + \
            self.leadTimeLabel + '_' + countryCodeISO3 + '.json'
        self.triggersPerStationDir = PIPELINE_OUTPUT + 'triggers_rp_per_station'
        if not os.path.exists(self.triggersPerStationDir):
            os.makedirs(self.triggersPerStationDir)
        self.triggersPerStationPath = PIPELINE_OUTPUT + \
            'triggers_rp_per_station/triggers_rp_' + \
            self.leadTimeLabel + '_' + countryCodeISO3 + '.json'
        self.GLOSSIS_STATIONS = glossis_stations
        self.DISTRICT_MAPPING = district_mapping
        self.current_date = CURRENT_DATE.strftime('%Y%m%d')

    def process(self):
        if SETTINGS[self.countryCodeISO3]['mock'] == False:
            self.removeOldGlossisData()
            self.download()
            self.postDataToDatalake()
            self.getGlossisData()
            #self.start_download_loop()
        if SETTINGS[self.countryCodeISO3]['mock'] == True:
            self.extractMockData()
        else:
            self.extractGlossisData()
        self.findTrigger()

    def removeOldGlossisData(self):
        if os.path.exists(self.GlossisInputPath):
            for f in [f for f in os.listdir(self.GlossisInputPath)]:
                os.remove(os.path.join(self.GlossisInputPath, f))
        else:
            os.makedirs(self.GlossisInputPath)

    def download(self):
        downloadDone = False

        timeToTryDownload = 43200
        timeToRetry = 600

        start = time.time()
        end = start + timeToTryDownload
        fname='2022-09-27_T060000'

        while downloadDone == False and time.time() < end:
            try:
                cnopts = pysftp.CnOpts()
                cnopts.hostkeys = None
                with pysftp.Connection(GLOSSIS_FTP, username=GLOSSIS_USER, password=GLOSSIS_PW,cnopts=cnopts) as sftp:
                    for filename in sftp.listdir('/data'):
                        if filename in [f'{fname}_DflowFM_gtsm4_1.25eu_meteo_fc_H.simulated_fc.nc',
                                        f'{fname}_Calculate_surge_gtsm4_1.25eu_H.surge.simulated_fc.nc']
                            sftp.get("data/" + filename, self.GlossisInputPath+ filename)            
                downloadDone = True
            except Exception as exception:
                error = 'Download data failed. Trying again in {} minutes.\n{}'.format(timeToRetry//60, exception)
                logger.error(error)
                time.sleep(timeToRetry)
        if downloadDone == False:
            raise ValueError('GLossis download failed for ' +
                            str(timeToTryDownload/3600) + ' hours, no new dataset was found')


            
            
    def postDataToDatalake(self):
        import requests
        import datetime
        import hmac
        import hashlib
        import base64
        from azure.identity import DefaultAzureCredential
        from azure.storage.filedatalake import DataLakeServiceClient
        import os, uuid, sys

        try:


            service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format("https", 
                                                                                                    DATALAKE_STORAGE_ACCOUNT_NAME), 
                                                credential=DATALAKE_STORAGE_ACCOUNT_KEY)

            container_name='ibf/stormsurge/Bronze/glossis/'
            file_system_client = service_client.get_file_system_client(file_system=container_name)
            for glossisfile in os.listdir(self.GlossisInputPath):  
                directory_name= glossisfile.split('_')[0]   
                
                dir_client = file_system_client.get_directory_client(directory_name)
                dir_client.create_directory()
                local_file = open(self.GlossisInputPath + glossisfile,'rb')
                
                file_contents = local_file.read()
                file_client = dir_client.create_file(f"{glossisfile}")
                file_client.upload_data(file_contents, overwrite=True)

        except Exception as e:
            print(e)            

                          
 

 
        
    def extractGlossisData(self):
        logger.info('\nExtracting Glossis (FTP) Data\n')

        files = [f for f in listdir(self.GlossisInputPath) if isfile(
            join(self.GlossisInputPath, f)) and f.endswith('.nc')]

        df_thresholds = pd.read_json(json.dumps(self.GLOSSIS_STATIONS))
        df_thresholds = df_thresholds.set_index("stationCode", drop=False)
        df_district_mapping = pd.read_json(json.dumps(self.DISTRICT_MAPPING))
        df_district_mapping = df_district_mapping.set_index("glossisStation", drop=False)

        stations = []
        trigger_per_day = {
            '1-day': False,
            '2-day': False,
            '3-day': False,
            '4-day': False,
            '5-day': False,
            '6-day': False,
            '7-day': False,
        }
        for i in range(0, len(files)):
            Filename = os.path.join(self.GlossisInputPath, files[i])
            
            # Skip old stations > need to be removed from FTP
            #if 'G5230_Na_ZambiaRedcross' in Filename or 'G5196_Uganda_Gauge' in Filename:
            #    continue

            station = {}
            station['code'] = files[i].split(
                '_')[2]

            data = xr.open_dataset(Filename)
            
            df_wl=data.water_level_surge.to_dataframe()
            
            df_wl.reset_index(inplace=True)  
            
            df_wl['station_id'] = df_wl['station_id'].str.decode('utf-8') 
            

            # Get threshold for this specific station
            if station['code'] in df_thresholds['stationCode'] and station['code'] in df_district_mapping['glofasStation']:
                
                logger.info(Filename)
                threshold = df_thresholds[df_thresholds['stationCode'] ==
                                          station['code']][TRIGGER_LEVEL][0]

                # Set dimension-values
                time = 0

                for step in range(1, 8):

                    # Loop through 51 ensembles, get forecast and compare to threshold
                    ensemble_options = 51
                    count = 0
                    dis_sum = 0
                    for ensemble in range(0, ensemble_options):

                        discharge = data['dis'].sel(
                            ensemble=ensemble, step=step).values[time][0]

                        if discharge >= threshold:
                            count = count + 1
                        dis_sum = dis_sum + discharge

                    prob = count/ensemble_options
                    dis_avg = dis_sum/ensemble_options
                    station['fc'] = dis_avg
                    station['fc_prob'] = prob 
                    station['fc_trigger'] = 1 if prob > self.TRIGGER_LEVELS['minimum'] else 0
                    #station['fc_trigger'] = 1 if prob > TRIGGER_LEVELS['minimum'] else 0
                    if station['fc_trigger'] == 1:
                        trigger_per_day[str(step)+'-day'] = True

                    if step == self.leadTimeValue:
                        stations.append(station)
                    station = {}
                    station['code'] = files[i].split(
                        '_')[2]

            data.close()

        # Add 'no_station'
        for station_code in ['no_station']:
            station = {}
            station['code'] = station_code
            station['fc'] = 0
            station['fc_prob'] = 0
            station['fc_trigger'] = 0
            stations.append(station)

        with open(self.extractedGlossisPath, 'w') as fp:
            json.dump(stations, fp)
            logger.info('Extracted Glossis data - File saved')

        with open(self.triggerPerDay, 'w') as fp:
            json.dump([trigger_per_day], fp)
            logger.info('Extracted Glossis data - Trigger per day File saved')

    def extractMockData(self):
        logger.info('\nExtracting Glossis (mock) Data\n')

        # Load input data
        df_thresholds = pd.read_json(json.dumps(self.GLOFAS_STATIONS))
        df_thresholds = df_thresholds.set_index("stationCode", drop=False)
        df_district_mapping = pd.read_json(json.dumps(self.DISTRICT_MAPPING))
        df_district_mapping = df_district_mapping.set_index("glofasStation", drop=False)

        # Set up variables to fill
        stations = []
        trigger_per_day = {
            '1-day': False,
            '2-day': False,
            '3-day': False,
            '4-day': False,
            '5-day': False,
            '6-day': False,
            '7-day': False,
        }

        for index, row in df_thresholds.iterrows():
            station = {}
            station['code'] = row['stationCode']

            if station['code'] in df_district_mapping['glofasStation'] and station['code'] != 'no_station':
                logger.info(station['code'])
                threshold = df_thresholds[df_thresholds['stationCode'] ==
                                          station['code']][TRIGGER_LEVEL][0]

                for step in range(1, 8):
                    # Loop through 51 ensembles, get forecast and compare to threshold
                    ensemble_options = 51
                    count = 0
                    dis_sum = 0

                    for ensemble in range(1, ensemble_options):

                        # MOCK OVERWRITE DEPENDING ON COUNTRY SETTING
                        if SETTINGS[self.countryCodeISO3]['if_mock_trigger'] == True:
                            if step < 3: # Only dummy trigger for 3-day and above
                                discharge = 0
                            elif station['code'] == 'G5220':  # UGA dummy flood station 1
                                discharge = 600
                            elif station['code'] == 'G1067':  # ETH dummy flood station 1
                                discharge = 5000
                            elif station['code'] == 'G1904':  # ETH dummy flood station 2
                                discharge = 5500
                            elif station['code'] == 'G5305':  # KEN dummy flood station
                                discharge = 3000
                            elif station['code'] == 'G7195':  # KEN dummy flood station
                                discharge = 3000
                            elif station['code'] == 'G1361':  # ZMB dummy flood station 1
                                discharge = 8000
                            elif station['code'] == 'G1328':  # ZMB dummy flood station 2
                                discharge = 9000
                            elif station['code'] == 'G1319':  # ZMB dummy flood station 3
                                discharge = 1400
                            elif station['code'] == 'G5369':  # PHL dummy flood station 1 G1964 G1966 G1967
                                discharge = 7000
                            elif station['code'] == 'G4630':  # PHL dummy flood station 2
                                discharge = 19000
                            elif station['code'] == 'G196700':  # PHL dummy flood station 3
                                discharge = 11400
                            else:
                                discharge = 0
                        else:
                            discharge = 0

                        if discharge >= threshold:
                            count = count + 1
                        dis_sum = dis_sum + discharge

                    prob = count/ensemble_options
                    dis_avg = dis_sum/ensemble_options
                    station['fc'] = dis_avg
                    station['fc_prob'] = prob
                    station['fc_trigger'] = 1 if prob > self.TRIGGER_LEVELS['minimum'] else 0
                    #station['fc_trigger'] = 1 if prob > TRIGGER_LEVELS['minimum'] else 0

                    if station['fc_trigger'] == 1:
                        trigger_per_day[str(step)+'-day'] = True

                    if step == self.leadTimeValue:
                        stations.append(station)
                    station = {}
                    station['code'] = row['stationCode']


        # Add 'no_station'
        for station_code in ['no_station']:
            station = {}
            station['code'] = station_code
            station['fc'] = 0
            station['fc_prob'] = 0
            station['fc_trigger'] = 0
            stations.append(station)

        with open(self.extractedGlossisPath, 'w') as fp:
            json.dump(stations, fp)
            logger.info('Extracted Glossis data - File saved')

        with open(self.triggerPerDay, 'w') as fp:
            json.dump([trigger_per_day], fp)
            logger.info('Extracted Glossis data - Trigger per day File saved')

    def findTrigger(self):
        # Load (static) threshold values per station
        df_thresholds = pd.read_json(json.dumps(self.GLOFAS_STATIONS))
        df_thresholds = df_thresholds.set_index("stationCode", drop=False)
        df_thresholds.sort_index(inplace=True)
        # Load extracted Glossis discharge levels per station
        with open(self.extractedGlossisPath) as json_data:
            d = json.load(json_data)
        df_discharge = pd.DataFrame(d)
        df_discharge.index = df_discharge['code']
        df_discharge.sort_index(inplace=True)

        # Merge two datasets
        df = pd.merge(df_thresholds, df_discharge, left_index=True,
                      right_index=True)
        del df['lat']
        del df['lon']

        # Determine trigger + return period per water station
        for index, row in df.iterrows():
            fc = float(row['fc'])
            trigger = int(row['fc_trigger'])
            if trigger == 1:
                if self.countryCodeISO3 == 'ZMB':
                    if fc >= row['threshold20Year']:
                        return_period_flood_extent = 20
                    else:
                        return_period_flood_extent = 10
                else:
                    return_period_flood_extent = 25
            else:
                return_period_flood_extent = None
                
            if fc >= row['threshold20Year']:
                return_period = 20
            elif fc >= row['threshold10Year']:
                return_period = 10
            elif fc >= row['threshold5Year']:
                return_period = 5
            elif fc >= row['threshold2Year']:
                return_period = 2
            else:
                return_period = None
            
            df.at[index, 'fc_rp_flood_extent'] = return_period_flood_extent
            df.at[index, 'fc_rp'] = return_period

        out = df.to_json(orient='records')
        with open(self.triggersPerStationPath, 'w') as fp:
            fp.write(out)
            logger.info('Processed Glossis data - File saved')