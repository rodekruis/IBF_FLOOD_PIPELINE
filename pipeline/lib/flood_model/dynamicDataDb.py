import pandas as pd
import requests
import json
from flood_model.settings import *
try:
    from flood_model.secrets import *
except ImportError:
    print('No secrets file found.')
import os
import numpy as np
import logging
logger = logging.getLogger(__name__)
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry 
import datetime
 

    
class DatabaseManager:

    """ Class to upload and process data in the database """

    def __init__(self, leadTimeLabel, countryCodeISO3,admin_level):
        self.countryCodeISO3 = countryCodeISO3
        self.leadTimeLabel = leadTimeLabel
        self.triggerFolder = PIPELINE_OUTPUT + "triggers_rp_per_station/"
        self.affectedFolder = PIPELINE_OUTPUT + "calculated_affected/"
        self.EXPOSURE_DATA_SOURCES = SETTINGS[countryCodeISO3]['EXPOSURE_DATA_SOURCES']
        if countryCodeISO3 == 'MWI':
            self.EXPOSURE_DATA_UBR_SOURCES = SETTINGS[countryCodeISO3]['EXPOSURE_DATA_UBR_SOURCES']
        self.API_SERVICE_URL = SETTINGS[countryCodeISO3]['IBF_API_URL']
        self.ADMIN_PASSWORD = SETTINGS[countryCodeISO3]['PASSWORD']
        self.levels = SETTINGS[countryCodeISO3]['levels']
        self.admin_level = admin_level
        current_time = datetime.datetime.now()
        
        self.uploadTime = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    def upload(self):
        self.uploadTriggersPerLeadTime()
        self.uploadTriggerPerStation()
        self.uploadCalculatedAffected()
        self.uploadRasterFile()
        if self.countryCodeISO3=='SSD':
            self.uploadImage()
    
    def sendNotification(self):
        leadTimes = SETTINGS[self.countryCodeISO3]['lead_times']
        max_leadTime = max(leadTimes, key=leadTimes.get)

        if SETTINGS[self.countryCodeISO3]["notify_email"] and self.leadTimeLabel == max_leadTime:
            body = {
                'countryCodeISO3': self.countryCodeISO3,
                'disasterType': self.getDisasterType()
            } 
            self.apiPostRequest('notification/send', body=body)

    
    def getDisasterType(self):
        disasterType = 'floods'
        return disasterType
    

    def uploadCalculatedAffected2(self):
        for indicator, values in self.EXPOSURE_DATA_SOURCES.items():
            adminlevels=self.admin_level
            with open(self.affectedFolder +
                      'affected_' + self.leadTimeLabel + '_' + self.countryCodeISO3 + '_admin_' + str(adminlevels) + '_' + indicator + '.json') as json_file:
                body = json.load(json_file)
                body['disasterType'] = self.getDisasterType()
                #body['adminLevel'] = self.admin_level
                self.apiPostRequest('admin-area-dynamic-data/exposure', body=body)
            logger.info(f'Uploaded calculated_affected for indicator: {indicator} for admin level: ' + str(adminlevels))
            if indicator == 'population':
                with open(self.affectedFolder +
                        'affected_' + self.leadTimeLabel + '_' + self.countryCodeISO3  + '_admin_' + str(adminlevels) + '_' + 'population_affected_percentage' + '.json') as json_file:
                    body = json.load(json_file)
                    body['disasterType'] = self.getDisasterType()
                    #body['adminLevel'] = self.admin_level
                    self.apiPostRequest('admin-area-dynamic-data/exposure', body=body)
                logger.info('Uploaded calculated_affected for indicator: ' + 'population_affected_percentage for admin level: ' + str(adminlevels))


    def uploadCalculatedAffected(self):
        for adminlevels in SETTINGS[self.countryCodeISO3]['levels']:#range(1,self.admin_level+1):            
            for indicator, values in self.EXPOSURE_DATA_SOURCES.items():
                if indicator == 'population':
                    with open(self.affectedFolder +
                            'affected_' + self.leadTimeLabel + '_' + self.countryCodeISO3  + '_admin_' + str(adminlevels) + '_' + 'population_affected_percentage' + '.json') as json_file:
                        body = json.load(json_file)
                        body['disasterType'] = self.getDisasterType()
                        body['date']=self.uploadTime
                        #body['adminLevel'] = self.admin_level
                        self.apiPostRequest('admin-area-dynamic-data/exposure', body=body)
                    logger.info('Uploaded calculated_affected for indicator: ' + 'population_affected_percentage for admin level: ' + str(adminlevels))
                    with open(self.affectedFolder+'affected_' + self.leadTimeLabel + '_' + self.countryCodeISO3 + '_admin_' + str(adminlevels) + '_' + indicator + '.json') as json_file:
                        body = json.load(json_file)
                        #body['disasterType'] = self.getDisasterType()
                        #body['adminLevel'] = self.admin_level
                        body['disasterType'] = self.getDisasterType()
                        body['date']=self.uploadTime
                        self.apiPostRequest('admin-area-dynamic-data/exposure', body=body)
                    logger.info(f'Uploaded calculated_affected for indicator: {indicator}' +' for admin level: ' + str(adminlevels))
                    indicator2 = 'alert_threshold'
                    with open(self.affectedFolder +
                                'affected_' + self.leadTimeLabel + '_' + self.countryCodeISO3 + '_admin_' + str(adminlevels) + '_' + indicator2 + '.json') as json_file:
                        body = json.load(json_file)
                        body['disasterType'] = self.getDisasterType()
                        body['date']=self.uploadTime
                        self.apiPostRequest('admin-area-dynamic-data/exposure', body=body)
                        
                    logger.info(f'Uploaded calculated_affected for indicator: {indicator2}' +' for admin level: ' + str(adminlevels))
                else:
                    with open(self.affectedFolder +'affected_' + self.leadTimeLabel + '_' + self.countryCodeISO3 + '_admin_' + str(adminlevels) + '_' + indicator + '.json') as json_file:
                        body = json.load(json_file)
                        body['disasterType'] = self.getDisasterType()
                        body['date']=self.uploadTime
                        #body['adminLevel'] = self.admin_level
                        self.apiPostRequest('admin-area-dynamic-data/exposure', body=body)
                    logger.info(f'Uploaded calculated_affected for indicator: {indicator}' +' for admin level: ' + str(adminlevels))                                    
                    
            if self.countryCodeISO3 == 'MWI':
                for indicator, values in self.EXPOSURE_DATA_UBR_SOURCES.items():
                    affectedIndicatorPath = self.affectedFolder + \
                            'affected_' + self.leadTimeLabel + '_' + self.countryCodeISO3  + '_admin_' + str(adminlevels) + '_' + indicator + '.json'
                    with open(affectedIndicatorPath) as json_file:
                        body = json.load(json_file)
                        body['disasterType'] = self.getDisasterType()
                        body['date']=self.uploadTime
                        self.apiPostRequest('admin-area-dynamic-data/exposure', body=body)
                        logger.info('Uploaded calculated_affected for indicator: ' + f'{indicator} for admin level: ' + str(adminlevels))


    def uploadRasterFile(self):
        disasterType = self.getDisasterType()
        rasterFile = RASTER_OUTPUT + '0/flood_extents/flood_extent_' + self.leadTimeLabel + '_' + self.countryCodeISO3 + '.tif'
        files = {'file': open(rasterFile,'rb')}
        self.apiPostRequest('admin-area-dynamic-data/raster/' + disasterType, files=files)
        logger.info(f'Uploaded raster-file: {rasterFile}')


    def uploadImage(self,eventName='no-name'):
        disasterType = self.getDisasterType()
       
        imageFile = PIPELINE_OUTPUT + self.countryCodeISO3 + '_' +self.leadTimeLabel +'_floods-map-image.png'     
        
        files = {
            'image': (imageFile, open(imageFile, 'rb'), "image/png"), 
            }
        
        data = {"submit": "Upload Image" }
        
        path_=f'event/event-map-image/{self.countryCodeISO3}/{disasterType}/{eventName}'          
        
        self.apiPostRequestImage(path_,
                                 files=files,
                                 data=data
                                 )
        logger.info(f'Uploaded image-file: {imageFile}')


    def uploadTriggerPerStation(self):
        df = pd.read_json(self.triggerFolder +
                          'triggers_rp_' + self.leadTimeLabel + '_' + self.countryCodeISO3 + ".json", orient='records')
        
        filename= self.triggerFolder +'triggers_rp_' + self.leadTimeLabel + '_' + self.countryCodeISO3 + ".json"

        with open(filename) as json_file:
            triggers = json.load(json_file) 

        stationForecasts = {
            "forecastLevel": [],
            "eapAlertClass": [],
            "forecastReturnPeriod": [],
            "triggerLevel": []
        }

        for key in triggers:
            stationForecasts["forecastLevel"].append({
                "fid": key['stationCode'],
                "value": int(key['fc'])
            })
            stationForecasts["eapAlertClass"].append({
                "fid": key['stationCode'],
                "value": 'no' if not key['eapAlertClass'] else key['eapAlertClass']
            })
            stationForecasts["forecastReturnPeriod"].append({
                "fid": key['stationCode'],
                "value": key['fc_rp']
            })
            stationForecasts["triggerLevel"].append({
                "fid": key['stationCode'],
                "value": 0 if not key['triggerLevel'] else int(key['triggerLevel'])
            })

        for key in ["forecastLevel", "eapAlertClass", "forecastReturnPeriod", "triggerLevel"]:
            body = {
                "leadTime": self.leadTimeLabel,
                "date": self.uploadTime,
                "disasterType": self.getDisasterType(),
                "pointDataCategory": "glofas_stations",
                "key": key,
                "dynamicPointData": stationForecasts[key]
                }
            self.apiPostRequest('point-data/dynamic', body=body)
            logger.info(f'Uploaded triggers per station, key: {key}')


    def uploadTriggersPerLeadTime(self):
        with open(self.triggerFolder +
                  'trigger_per_day_' + self.countryCodeISO3 + ".json") as json_file:
            triggers = json.load(json_file)[0]
            triggersPerLeadTime = []
            for key in triggers:
                triggersPerLeadTime.append({
                    'leadTime': str(key),
                    'triggered': triggers[key]['triggered'],
                    "thresholdReached": triggers[key]['thresholdReached']
                })
        body = {
            'countryCodeISO3': self.countryCodeISO3,
            'disasterType': self.getDisasterType(),
            'triggersPerLeadTime': triggersPerLeadTime
        }
        body['date']=self.uploadTime
        self.apiPostRequest('event/triggers-per-leadtime', body=body)
        logger.info('Uploaded triggers per leadTime')

    def apiGetRequest(self, path, countryCodeISO3):
        TOKEN = self.apiAuthenticate()
        
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get(
            self.API_SERVICE_URL + path + '/' + countryCodeISO3,
            headers={'Authorization': 'Bearer ' + TOKEN}
        )

        '''
        response = requests.get(
            self.API_SERVICE_URL + path + '/' + countryCodeISO3,
            headers={'Authorization': 'Bearer ' + TOKEN}
        )
        '''
        data = response.json()
        return(data)

    def apiPostRequest(self, path, body=None, files=None):
        TOKEN = self.apiAuthenticate()

        if body != None:
            headers={'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        elif files != None:
            headers={'Authorization': 'Bearer ' + TOKEN}
        '''
        r = requests.post(
            self.API_SERVICE_URL + path,
            json=body,
            files=files,
            headers=headers
        )
        '''
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
      

        r = session.post(
            self.API_SERVICE_URL + path,
            json=body,
            files=files,
            headers=headers
        )
         
        if r.status_code >= 400:
            #logger.info(r.text)
            logger.error("PIPELINE ERROR")
            raise ValueError()
        
    def apiPostRequestImage(self, path,files=None,data=None):
        TOKEN = self.apiAuthenticate()

        headers={'Authorization': 'Bearer ' + TOKEN}

        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
      

        r = session.post(
            self.API_SERVICE_URL + path,  
            files=files,
            data=data,
            headers=headers
        )
         
        if r.status_code >= 400:
            #logger.info(r.text)
            logger.error("PIPELINE ERROR")
            raise ValueError()
        

    def apiAuthenticate(self):
        API_LOGIN_URL=self.API_SERVICE_URL+'user/login'
        
        login_response = requests.post(API_LOGIN_URL, data=[(
            'email', ADMIN_LOGIN), ('password', self.ADMIN_PASSWORD)])
        
        return login_response.json()['user']['token']

    def getDataFromDatalake(self, path):
        import requests
        import datetime
        import hmac
        import hashlib
        import base64

        request_time = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        file_system_name = 'ibf/' + path
        logger.info(f'Downloading from datalake: {file_system_name}')

        string_params = {
            'verb': 'GET',
            'Content-Encoding': '',
            'Content-Language': '',
            'Content-Length': '',
            'Content-MD5': '',
            'Content-Type': '',
            'Date': '',
            'If-Modified-Since': '',
            'If-Match': '',
            'If-None-Match': '',
            'If-Unmodified-Since': '',
            'Range': '',
            'CanonicalizedHeaders': 'x-ms-date:' + request_time + '\nx-ms-version:' + DATALAKE_API_VERSION,
            'CanonicalizedResource': '/' + DATALAKE_STORAGE_ACCOUNT_NAME+'/'+file_system_name
        }

        string_to_sign = (string_params['verb'] + '\n'
                          + string_params['Content-Encoding'] + '\n'
                          + string_params['Content-Language'] + '\n'
                          + string_params['Content-Length'] + '\n'
                          + string_params['Content-MD5'] + '\n'
                          + string_params['Content-Type'] + '\n'
                          + string_params['Date'] + '\n'
                          + string_params['If-Modified-Since'] + '\n'
                          + string_params['If-Match'] + '\n'
                          + string_params['If-None-Match'] + '\n'
                          + string_params['If-Unmodified-Since'] + '\n'
                          + string_params['Range'] + '\n'
                          + string_params['CanonicalizedHeaders']+'\n'
                          + string_params['CanonicalizedResource'])

        signed_string = base64.b64encode(hmac.new(base64.b64decode(
            DATALAKE_STORAGE_ACCOUNT_KEY), msg=string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()).decode()
        headers = {
            'x-ms-date': request_time,
            'x-ms-version': DATALAKE_API_VERSION,
            'Authorization': ('SharedKey ' + DATALAKE_STORAGE_ACCOUNT_NAME + ':' + signed_string)
        }
        url = ('https://' + DATALAKE_STORAGE_ACCOUNT_NAME +
               '.dfs.core.windows.net/'+file_system_name)
        r = requests.get(url, headers=headers)
        return r