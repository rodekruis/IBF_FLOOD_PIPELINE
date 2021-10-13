from flood_model.glofasdata import GlofasData
from flood_model.floodExtent import FloodExtent
from flood_model.exposure import Exposure
from flood_model.dynamicDataDb import DatabaseManager
from flood_model.settings import *
import pandas as pd
import json
from shapely import wkb, wkt
import geopandas
import os


class Forecast:
    def __init__(self, leadTimeLabel, leadTimeValue, countryCodeISO3, admin_level):
        self.leadTimeLabel = leadTimeLabel
        self.leadTimeValue = leadTimeValue
        self.admin_level = admin_level
        self.db = DatabaseManager(leadTimeLabel, countryCodeISO3)
        self.DistrictMappingFolder = STATION_DISTRICT_MAPPING_FOLDER
        self.TriggersFolder = TRIGGER_DATA_FOLDER_TR

        admin_area_json = self.db.apiGetRequest('admin-areas/raw',countryCodeISO3=countryCodeISO3)
        for index in range(len(admin_area_json)):
            admin_area_json[index]['geometry'] = admin_area_json[index]['geom']
            admin_area_json[index]['properties'] = {
                'placeCode': admin_area_json[index]['placeCode'],
                'name': admin_area_json[index]['name']
            }
        self.admin_area_gdf = geopandas.GeoDataFrame.from_features(admin_area_json)
        self.population_total = self.db.apiGetRequest('admin-area-data/{}/{}/{}'.format(countryCodeISO3, self.admin_level, 'populationTotal'), countryCodeISO3='')
        
        #read glofas trigger levels from file
        glofas_stations = self.db.apiGetRequest('glofas-stations',countryCodeISO3=countryCodeISO3)
        df=pd.read_csv(self.TriggersFolder + f'{countryCodeISO3}_glofas_stations.csv', index_col=False)
        df_glofas_stations= pd.DataFrame(glofas_stations)        
        df_glofas_stations = df_glofas_stations.filter(['id', 'stationCode','geom'])
        df_glofas_stations = pd.merge(df_glofas_stations, df,  how='left', left_on=['stationCode'], right_on = ['stationCode'])
        dic_glofas_stations = df_glofas_stations.to_dict(orient='records')
        self.glofas_stations = dic_glofas_stations

        #self.glofas_trigger_lveles = pd.read_csv(self.DistrictMappingFolder + f'/{countryCodeISO3}_trigger_levels.csv', index_col=False) 
        #read district mapping
        district_mapping_df = pd.read_csv(self.DistrictMappingFolder + f'{countryCodeISO3}_district_mapping.csv', index_col=False) 
        self.district_mapping = district_mapping_df.to_dict(orient='records')
        #self.district_mapping = self.db.apiGetRequest('admin-areas/raw',countryCodeISO3=countryCodeISO3)
        self.glofasData = GlofasData(leadTimeLabel, leadTimeValue, countryCodeISO3, self.glofas_stations, self.district_mapping)
        self.floodExtent = FloodExtent(leadTimeLabel, leadTimeValue, countryCodeISO3, self.district_mapping, self.admin_area_gdf)
        self.exposure = Exposure(leadTimeLabel, countryCodeISO3, self.admin_area_gdf, self.population_total, self.admin_level, self.district_mapping)
