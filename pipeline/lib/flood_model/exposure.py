import rasterio
import rasterio.mask
import rasterio.features
import rasterio.warp
from rasterio.features import shapes
import fiona
import numpy as np
import pandas as pd
from pandas import DataFrame
import json
from flood_model.settings import *
import os
import functools
from flood_model.dynamicDataDb import DatabaseManager
import geopandas
import time
import logging
logger = logging.getLogger(__name__)
class Exposure:

    """Class used to calculate the exposure per exposure type"""

    def __init__(self, leadTimeLabel, countryCodeISO3, admin_area_gdf, population_total, admin_level, district_mapping,pcodes):
        self.leadTimeLabel = leadTimeLabel
        self.admin_level = admin_level
        self.countryCodeISO3 = countryCodeISO3
        self.disasterExtentRaster = RASTER_OUTPUT + \
            '0/flood_extents/flood_extent_' + leadTimeLabel + '_' + countryCodeISO3 + '.tif'
        self.selectionValue = 0.9
        self.outputPath = PIPELINE_OUTPUT + "out.tif"
        self.district_mapping = district_mapping
        self.ADMIN_AREA_GDF = admin_area_gdf
        self.PIPELINE_INPUT_COD=PIPELINE_INPUT+'cod/'
        self.POPULATION_PATH= os.path.join(self.PIPELINE_INPUT_COD,f"{countryCodeISO3}_{self.admin_level}_population.json") 

        #self.ADMIN_AREA_GDF_TMP_PATH = os.path.join(PIPELINE_OUTPUT,"admin-areas_TMP.geojson")  #s.geojson', driver='GeoJSON')
        self.ADMIN_AREA_GDF_TMP_PATH = PIPELINE_OUTPUT+"admin-areas_TMP.shp"   
        self.EXPOSURE_DATA_SOURCES = SETTINGS[countryCodeISO3]['EXPOSURE_DATA_SOURCES']
        
        self.levels = SETTINGS[countryCodeISO3]['levels']
        self.pcode_df=pcodes
        self.db = DatabaseManager(leadTimeLabel, countryCodeISO3,admin_level)
        if "population" in self.EXPOSURE_DATA_SOURCES:
            self.population_total = population_total
              
                   
    def callAllExposure(self):
        for indicator, values in self.EXPOSURE_DATA_SOURCES.items():
            logger.info(f'indicator: {indicator}')
            self.inputRaster = RASTER_INPUT + values['source'] + ".tif"
            self.outputRaster = RASTER_OUTPUT + "0/" + values['source'] + self.leadTimeLabel
            
            stats = self.calcAffected(self.disasterExtentRaster, indicator, values['rasterValue'])
            df_stats=pd.DataFrame(stats) 
            df_stats = pd.merge(self.pcode_df,df_stats,  how='left',left_on=f"placeCode_{self.admin_level}" , right_on ='placeCode')
 
  
            #stats_dff = pd.merge(df,self.pcode_df,  how='left',left_on='placeCode', right_on = f'placeCode_{self.admin_level}')
            for adm_level in SETTINGS[self.countryCodeISO3]['levels']:
                logger.info(f'processing indicator: {indicator} for admin level{adm_level}')         
                if adm_level==self.admin_level:
                    df_stats_levl=stats
                else:
                    df_stats_levl =df_stats.groupby(f'placeCode_{adm_level}').agg({'amount': 'sum'})
                    df_stats_levl.reset_index(inplace=True)
                    df_stats_levl['placeCode']=df_stats_levl[f'placeCode_{adm_level}']
                    df_stats_levl=df_stats_levl[['amount','placeCode']].to_dict(orient='records')

 
                self.statsPath = PIPELINE_OUTPUT + 'calculated_affected/affected_' + \
                    self.leadTimeLabel + '_' + self.countryCodeISO3 +'_admin_' +str(adm_level) + '_' + indicator + '.json'

                result = {
                    'countryCodeISO3': self.countryCodeISO3,
                    'exposurePlaceCodes': df_stats_levl,
                    'leadTime': self.leadTimeLabel,
                    'dynamicIndicator': indicator + '_affected',
                    'adminLevel': adm_level
                }
                
                with open(self.statsPath, 'w') as fp:
                    json.dump(result, fp)

                if self.population_total:
                    get_population_affected_percentage_ = functools.partial(self.get_population_affected_percentage, adm_level=adm_level)
                    population_affected_percentage = list(map(get_population_affected_percentage_, df_stats_levl))
                    #population_affected_percentage = list(map(self.get_population_affected_percentage, df_stats,adm_level))
     
                    population_affected_percentage_file_path = PIPELINE_OUTPUT + 'calculated_affected/affected_' + \
                        self.leadTimeLabel + '_' + self.countryCodeISO3 + '_admin_' + str(adm_level) + '_' + 'population_affected_percentage' + '.json'
                        
                    population_affected_percentage_records = {
                        'countryCodeISO3': self.countryCodeISO3,
                        'exposurePlaceCodes': population_affected_percentage, 
                        'leadTime': self.leadTimeLabel,
                        'dynamicIndicator': 'population_affected_percentage',
                        'adminLevel': adm_level
                    }

                    with open(population_affected_percentage_file_path, 'w') as fp:
                        json.dump(population_affected_percentage_records, fp)

                    # define alert_threshold layer
                alert_threshold = list(map(self.get_alert_threshold, df_stats_levl))

                alert_threshold_file_path = PIPELINE_OUTPUT + 'calculated_affected/affected_' + \
                    self.leadTimeLabel + '_' + self.countryCodeISO3 + '_admin_' + str(adm_level) + '_' + 'alert_threshold' + '.json'

                alert_threshold_records = {
                    'countryCodeISO3': self.countryCodeISO3,
                    'exposurePlaceCodes': alert_threshold,
                    'leadTime': self.leadTimeLabel,
                    'dynamicIndicator': 'alert_threshold',
                    'adminLevel': adm_level
                }

                with open(alert_threshold_file_path, 'w') as fp:
                    json.dump(alert_threshold_records, fp)


    def get_alert_threshold(self, population_affected):
        # population_total = next((x for x in self.population_total if x['placeCode'] == population_affected['placeCode']), None)
        alert_threshold = 0
        if (population_affected['amount'] > 0):
            alert_threshold = 1
        else:
            alert_threshold = 0
        return {
            'amount': alert_threshold,
            'placeCode': population_affected['placeCode']
        }
        
    def get_population_affected_percentage(self, population_affected,adm_level):
        ##get population for admin level
        try:
            #df_stats = self.db.apiGetRequest('admin-area-data/{}/{}/{}'.format(self.countryCodeISO3, adm_level, 'populationTotal'),countryCodeISO3='')
            self.POPULATION_PATH= os.path.join(self.PIPELINE_INPUT_COD,f"{self.countryCodeISO3}_{adm_level}_population.json") 
            with open(self.POPULATION_PATH) as fp:
                df_stats=json.load(fp)
        except Exception as e:
            logger.info('file not found')
            '''
            logger.info(f'connection error while getting population data, waiting 60 seconds then trying again (1/2)')
            
            time.sleep(60)
            try:
                df_stats = self.db.apiGetRequest(
                    'admin-area-data/{}/{}/{}'.format(self.countryCodeISO3, adm_level, 'populationTotal'),
                    countryCodeISO3='')
            except Exception as e:
                logger.info(f'connection error while getting population data, waiting 60 seconds then trying again (2/2)')
                time.sleep(60)
                df_stats = self.db.apiGetRequest(
                    'admin-area-data/{}/{}/{}'.format(self.countryCodeISO3, adm_level, 'populationTotal'),
                    countryCodeISO3='')
            '''        
        population_total = next((x for x in df_stats if x['placeCode'] == population_affected['placeCode']), None)
        population_affected_percentage = 0.0
        if population_total and population_total['value'] > 0:
            population_affected_percentage = population_affected['amount'] / population_total['value']
        return {
            'amount': population_affected_percentage,
            'placeCode': population_total['placeCode']
        }
    
    def calcAffected(self, disasterExtentRaster, indicator, rasterValue):
        disasterExtentShapes = self.loadTiffAsShapes(disasterExtentRaster)
        if disasterExtentShapes != []:
            try:
                affectedImage, affectedMeta = self.clipTiffWithShapes(
                    self.inputRaster, disasterExtentShapes)
                with rasterio.open(self.outputRaster, "w", **affectedMeta) as dest:
                    dest.write(affectedImage)
            except ValueError:
                logger.info('Rasters do not overlap')
        #self.ADMIN_AREA_GDF_ADM_LEL_=self.ADMIN_AREA_GDF_ADM_LEL.query(f'adminLevel == {adm_level}')
        self.ADMIN_AREA_GDF.to_file(self.ADMIN_AREA_GDF_TMP_PATH)
        #self.ADMIN_AREA_GDF.to_file(self.ADMIN_AREA_GDF_TMP_PATH,driver='GeoJSON')
        stats = self.calcStatsPerAdmin(indicator, disasterExtentShapes, rasterValue)
        return stats

    def calcStatsPerAdmin(self, indicator, disasterExtentShapes, rasterValue):
        # Load trigger_data per station
        path = PIPELINE_DATA+'output/triggers_rp_per_station/triggers_rp_' + \
            self.leadTimeLabel + '_' + self.countryCodeISO3 + '.json'
        df_triggers = pd.read_json(path, orient='records')
        df_triggers = df_triggers.set_index("stationCode", drop=False)
        # Load assigned station per district
        #df_district_mapping = pd.read_json(json.dumps(self.district_mapping))
        df_district_mapping=pd.DataFrame(self.district_mapping)
        df_district_mapping = df_district_mapping.set_index("placeCode", drop=False)

        stats = []
        with fiona.open(self.ADMIN_AREA_GDF_TMP_PATH, "r") as shapefile:

            # Clip affected raster per area
            for area in shapefile:
                if disasterExtentShapes != []:
                    try:
                        outImage, outMeta = self.clipTiffWithShapes(
                            self.outputRaster, [area["geometry"]])

                        # Write clipped raster to tempfile to calculate raster stats
                        with rasterio.open(self.outputPath, "w", **outMeta) as dest:
                            dest.write(outImage)

                        statsDistrict = self.calculateRasterStats(indicator,  str(
                            area['properties']['placeCode']), self.outputPath, rasterValue)

                        # Overwrite non-triggered areas with positive exposure (due to rounding errors) to 0
                        if self.checkIfTriggeredArea(df_triggers, df_district_mapping, str(area['properties']['placeCode'])) == 0:
                            statsDistrict = {'amount': 0, 'placeCode': str(
                                area['properties']['placeCode'])}
                    except (ValueError, rasterio.errors.RasterioIOError):
                        # If there is no disaster in the district set  the stats to 0
                        statsDistrict = {'amount': 0, 'placeCode': str(
                            area['properties']['placeCode'])}
                else:
                    statsDistrict = {'amount': 0, 'placeCode': str(
                        area['properties']['placeCode'])}
                stats.append(statsDistrict)
        os.remove(self.ADMIN_AREA_GDF_TMP_PATH)
        return stats

    def checkIfTriggeredArea(self, df_triggers, df_district_mapping, pcode):
        df_station_code = df_district_mapping[df_district_mapping['placeCode'] == pcode]
        if df_station_code.empty:
            return 0
        station_code = df_station_code['glofasStation'][0]
        if station_code == 'no_station':
            return 0
        df_trigger = df_triggers[df_triggers['stationCode'] == station_code]
        if df_trigger.empty:
            return 0
        trigger = df_trigger['fc_trigger'][0]
        return trigger

    def calculateRasterStats(self, indicator, district, outFileAffected, rasterValue):
        raster = rasterio.open(outFileAffected)
        stats = []

        array = raster.read(masked=True)
        band = array[0]
        theSum = band.sum() * rasterValue
        stats.append({
            'amount': float(str(theSum)),
            'placeCode': district
        })
        return stats[0]

    def loadTiffAsShapes(self, tiffLocaction):
        allgeom = []
        with rasterio.open(tiffLocaction) as dataset:
            # Read the dataset's valid data mask as a ndarray.
            image = dataset.read(1).astype(np.float32)
            image[image >= 0] = 1
            mask = dataset.dataset_mask()
            theShapes = shapes(image, mask=mask, transform=dataset.transform)

            # Extract feature shapes and values from the array.
            for geom, val in theShapes:
                if val >= self.selectionValue:
                    # Transform shapes from the dataset's own coordinate
                    # reference system to CRS84 (EPSG:4326).
                    geom = rasterio.warp.transform_geom(
                        dataset.crs, 'EPSG:4326', geom, precision=6)
                    # Append everything to one geojson

                    allgeom.append(geom)
        return allgeom

    def clipTiffWithShapes(self, tiffLocaction, shapes):
        with rasterio.open(tiffLocaction) as src:
            outImage, out_transform = rasterio.mask.mask(
                src, shapes, crop=True)
            outMeta = src.meta.copy()

        outMeta.update({"driver": "GTiff",
                        "height": outImage.shape[1],
                        "width": outImage.shape[2],
                        "transform": out_transform})

        return outImage, outMeta
