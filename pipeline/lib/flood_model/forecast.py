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
import logging
logger = logging.getLogger(__name__)



class Forecast:
    def __init__(self, leadTimeLabel, leadTimeValue, countryCodeISO3, admin_level):
        self.leadTimeLabel = leadTimeLabel
        self.leadTimeValue = leadTimeValue
        self.countryCodeISO3=countryCodeISO3
        self.admin_level = admin_level
        self.db = DatabaseManager(leadTimeLabel, countryCodeISO3,admin_level)
        self.DistrictMappingFolder = STATION_DISTRICT_MAPPING_FOLDER
        self.TriggersFolder = TRIGGER_DATA_FOLDER_TR
        self.levels = SETTINGS[countryCodeISO3]['levels']
        self.PIPELINE_INPUT_COD=PIPELINE_INPUT+'cod/'
        self.ADMIN_AREA_GDF_PATH= os.path.join(self.PIPELINE_INPUT_COD,f"{countryCodeISO3}_admin_areas.geojson")

        self.POPULATION_PATH= os.path.join(self.PIPELINE_INPUT_COD,f"{countryCodeISO3}_{self.admin_level}_population.json") 
        
        # download admin boundary data 
        
        if not os.path.exists(self.ADMIN_AREA_GDF_PATH):
            admin_area_json = self.db.apiGetRequest('admin-areas/raw',countryCodeISO3=countryCodeISO3)

            for index in range(len(admin_area_json)):
                admin_area_json[index]['geometry'] = admin_area_json[index]['geom']
                admin_area_json[index]['properties'] = {
                    'placeCode': admin_area_json[index]['placeCode'], 
                    'placeCodeParent': admin_area_json[index]['placeCodeParent'],                   
                    'name': admin_area_json[index]['name'],
                    'adminLevel': admin_area_json[index]['adminLevel']
                    }
               
            Admin_DF=geopandas.GeoDataFrame.from_features(admin_area_json)      
            Admin_DF.to_file(self.ADMIN_AREA_GDF_PATH,driver='GeoJSON')        
  
        df_admin1=geopandas.read_file(self.ADMIN_AREA_GDF_PATH)
        df_admin2=df_admin1.filter(['adminLevel','placeCode','placeCodeParent'])
        
        df_admin=pd.DataFrame(df_admin1)

        df_list={}       
        max_iteration=self.admin_level+1
        for adm_level in self.levels:
            df_=df_admin2.query(f"adminLevel == {adm_level}")
            df_.rename(columns={"placeCode": f"placeCode_{adm_level}","placeCodeParent": f"placeCodeParent_{adm_level}"},inplace=True)            
            df_list[adm_level]=df_            
        
        df=df_list[self.admin_level]        

        ################# Create a dataframe with pcodes for each admin level   
        
        df=df_list[list(df_list.keys())[0]]

        for adm_level in list(df_list.keys())[1:]:
            df2=df_list[adm_level].drop('adminLevel', axis=1)
            df=pd.merge(df,df2,  how='left',left_on=f'placeCodeParent_{adm_level+1}' , right_on =f'placeCode_{adm_level}')

        self.pcode_df=df[[f"placeCode_{i}" for i in list(df_list.keys())]]

   
        #for adm_level in self.levels:
        #    j=adm_level-1
        #    if j >0 and len(self.levels)>1:
        #        df=pd.merge(df.copy(),df_list[j],  how='left',left_on=f'placeCodeParent_{j+1}' , right_on =f'placeCode_{j}')
     
        #df=df[[f"placeCode_{i}" for i in self.levels]]      
        #self.pcode_df=df[[f"placeCode_{i}" for i in self.levels]]           
       
        df_admin=df_admin.query(f'adminLevel == {self.admin_level}')
        
 
 
        # download population data 
        for level in self.levels:
            POPULATION_PATH= os.path.join(self.PIPELINE_INPUT_COD,f"{self.countryCodeISO3}_{level}_population.json") 
            if not os.path.exists(POPULATION_PATH):
                population_df = self.db.apiGetRequest('admin-area-data/{}/{}/{}'.format(countryCodeISO3, level, 'populationTotal'), countryCodeISO3='')
                with open(POPULATION_PATH, "w") as fp:
                    json.dump(population_df, fp) 
   
 
        with open(self.POPULATION_PATH) as fp:
            population_df=json.load(fp)
        
        population_df=pd.DataFrame(population_df) 

        
        #self.admin_area_gdf2 = df_admin1
        
        self.admin_area_gdf=df_admin1.query(f'adminLevel == {self.admin_level}')
            
        df_admin=df_admin.filter(['placeCode','placeCodeParent','name'])#,'geometry'])

     

        district_mapping_df = pd.read_csv(self.DistrictMappingFolder + f'{countryCodeISO3}_district_mapping.csv', index_col=False,dtype={'placeCode': str, 'ADM2_PCODE': str,'ADM3_PCODE': str}) 
        district_mapping_df=district_mapping_df.filter(['placeCode','glofasStation'])
        district_mapping_df = pd.merge(district_mapping_df,df_admin,  how='left',left_on='placeCode', right_on = 'placeCode')
        district_mapping_df['placeCode'] = district_mapping_df['placeCode'].astype(str)
        self.district_mapping = district_mapping_df.to_dict(orient='records')
        df_admin=df_admin.filter(['placeCode','placeCodeParent'])
        population_df = pd.merge(population_df,df_admin,  how='left',left_on='placeCode', right_on = 'placeCode')
        #print(population_df)
        
        population_df=population_df.to_dict(orient='records')
        self.population_total =population_df

        #read glofas trigger levels from file
        glofas_stations = self.db.apiGetRequest('glofas-stations',countryCodeISO3=countryCodeISO3)
        
        df=pd.read_csv(self.TriggersFolder + f'{countryCodeISO3}_glofas_stations.csv', index_col=False)
                      
        df_glofas_stations= pd.DataFrame(glofas_stations)        
        df_glofas_stations = df_glofas_stations.filter(['id', 'stationCode','geom'])
        
        df_glofas_stations = pd.merge(df_glofas_stations, df,  how='left', left_on=['stationCode'], right_on = ['stationCode'])
        dic_glofas_stations = df_glofas_stations.to_dict(orient='records')
        self.glofas_stations = dic_glofas_stations
     
        self.glofasData = GlofasData(leadTimeLabel, leadTimeValue, countryCodeISO3, self.glofas_stations, self.district_mapping,self.admin_area_gdf)
        self.floodExtent = FloodExtent(leadTimeLabel, leadTimeValue, countryCodeISO3, self.district_mapping, self.admin_area_gdf)
        self.exposure = Exposure(leadTimeLabel, countryCodeISO3, self.admin_area_gdf, self.population_total, self.admin_level, self.district_mapping,self.pcode_df)

        stationNAmesfile=PIPELINE_INPUT +'glofasStaions.json'
        with open(stationNAmesfile, 'w') as fp:
            json.dump(dic_glofas_stations, fp)
 
        
    def pcode1(self,x):
        len_x=len(x)-2
        if x.startswith('ZM'):
            pcoded=x[0:4] 
  
        elif x.startswith('0'):
            pcoded='ZM'+x[1:3]
 
        else:
            pcoded='ZM'+x[0:3]
                     
        return x[:-len_x]
    def pcode2(self,x):
        len_x=len(x)-4
        if x.startswith('ZM'):
            pcoded=x
        elif x.startswith('0'):
            pcoded='ZM'+x[1:5]
        else:
            pcoded='ZM'+x[0:5]
            pcoded=x[:-2]
        return x[:-len_x]
    def pcode(self,x):
        return 'ZM'+x
