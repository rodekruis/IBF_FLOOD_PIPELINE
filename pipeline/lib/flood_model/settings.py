
##################
## LOAD SECRETS ##
##################

# 1. Try to load secrets from Azure key vault (i.e. when running through Logic App) if user has access
 
try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    az_credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url='https://ibf-flood-keys.vault.azure.net', credential=az_credential)

    ADMIN_LOGIN = secret_client.get_secret("ADMIN-LOGIN").value
    GLOFAS_USER = secret_client.get_secret("GLOFAS-USER").value
    GLOFAS_PW = secret_client.get_secret("GLOFAS-PW").value
    
    #GOOGLE_DRIVE_DATA_URL = secret_client.get_secret("GOOGLE-DRIVE-DATA-URL").value
    IBF_URL=secret_client.get_secret("IBF-URL").value
    IBF_PASSWORD=secret_client.get_secret("IBF-PASSWORD").value
  
    DATALAKE_STORAGE_ACCOUNT_NAME = secret_client.get_secret("DATALAKE-STORAGE-ACCOUNT-NAME").value
    DATALAKE_STORAGE_ACCOUNT_KEY = secret_client.get_secret("DATALAKE-STORAGE-ACCOUNT-KEY").value
    DATALAKE_API_VERSION = '2018-11-09'

except Exception as e:
    print('No access to Azure Key vault, skipping.')

# 2. Try to load secrets from env-variables (i.e. when using Github Actions)
try:
    import os    
    ADMIN_LOGIN = os.environ['ADMIN_LOGIN']
    GLOFAS_USER = os.environ['GLOFAS_USER']
    GLOFAS_PW = os.environ['GLOFAS_PW']
    IBF_URL=os.environ['IBF_API_URL']
    IBF_PASSWORD=os.environ['IBF_PASSWORD']
    DATALAKE_STORAGE_ACCOUNT_NAME = os.environ['DATALAKE-STORAGE-ACCOUNT-NAME']
    DATALAKE_STORAGE_ACCOUNT_KEY = os.environ['DATALAKE-STORAGE-ACCOUNT-KEY']
    DATALAKE_API_VERSION = '2018-11-09'

except:
     print('No environment variables found.')

# 3. If 1. and 2. both fail, then assume secrets are loaded via secrets.py file (when running locally). If neither of the 3 options apply, this script will fail.
try:
    from flood_model.secrets import *
except ImportError:
    print('No secrets file found.')


######################
## COUNTRY SETTINGS ##
######################

# Countries to include
#COUNTRY_CODES = ['ETH','ZMB','KEN','UGA'] #
COUNTRY_CODES = ['PHL'] #
SETTINGS = {
    "PHL": {
        "IBF_API_URL": IBF_URL,
        "PASSWORD": IBF_PASSWORD,
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": True,
        'lead_times': {
            "3-day": 3
        },
        'admin_level': 3,
        'levels':[3,2,1],
        'GLOFAS_FTP':'aux.ecmwf.int/RedcrossPhilippines_glofas_point/',
        'GLOFAS_FILENAME':'glofas_pointdata_RedcrossPhilippines', 
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/hrsl_phl_pop_resized_30",
                "rasterValue": 1
            }
        }
    }
}





# Change this date only in case of specific testing purposes
from datetime import date, timedelta
CURRENT_DATE = date.today()
#CURRENT_DATE=date.today() - timedelta(1) # to use yesterday's date




####################
## OTHER SETTINGS ##
####################
GOOGLE_DRIVE_DATA_URL = 'https://drive.google.com/file/d/14MbG4uFPGJCduM5aLkvgSGqA8io6Gh9C/view?usp=sharing'

TRIGGER_LEVELS = {
    "minimum": 0.6,
    "medium": 0.7,
    "maximum": 0.8
}



###################
## PATH SETTINGS ##
###################
RASTER_DATA = 'data/raster/'
RASTER_INPUT = RASTER_DATA + 'input/'
RASTER_OUTPUT = RASTER_DATA + 'output/'
PIPELINE_DATA = 'data/other/'
PIPELINE_INPUT = PIPELINE_DATA + 'input/'
PIPELINE_OUTPUT = PIPELINE_DATA + 'output/'
TRIGGER_DATA_FOLDER='data/trigger_data/triggers_rp_per_station/'
TRIGGER_DATA_FOLDER_TR='data/trigger_data/glofas_trigger_levels/'
STATION_DISTRICT_MAPPING_FOLDER='data/trigger_data/station_district_mapping/'

#########################
## INPUT DATA SETTINGS ##
#########################

# Glofas input
#GLOFAS_FTP = 'data-portal.ecmwf.int/ZambiaRedcross_glofas_point/'
#GLOFAS_FILENAME = 'glofas_pointdata_ZambiaRedcross'


#####################
## ATTRIBUTE NAMES ##
#####################

TRIGGER_LEVEL = 'triggerLevel'
LEAD_TIME = 'leadTime'

### to reduce logicapp task run only for flood prone areas 
Areas_With_GlofasStation=["PH021512000","PH021513000","PH021514000","PH021515000","PH021516000","PH021502000","PH021503000","PH021504000",
                          "PH021506000","PH021508000","PH021510000","PH023101000","PH021517000","PH021519000","PH021520000","PH021521000",
                          "PH021525000","PH023103000","PH036902000","PH021526000","PH124702000","PH021527000","PH021528000","PH021529000",
                          "PH023102000","PH023104000","PH023107000","PH023108000","PH023105000","PH023106000","PH023109000","PH023116000",
                          "PH023117000","PH023112000","PH023113000","PH023114000","PH023115000","PH023118000","PH023127000","PH023119000",
                          "PH023120000","PH023122000","PH023123000","PH023124000","PH023125000","PH023126000","PH023128000","PH023129000",
                          "PH023130000","PH023131000","PH023136000","PH023132000","PH023133000","PH023134000","PH023137000","PH023135000",
                          "PH031403000","PH031416000","PH031417000","PH031407000","PH031409000","PH031410000","PH031418000","PH035402000",
                          "PH035410000","PH035412000","PH035414000","PH035417000","PH035418000","PH036904000","PH036905000","PH035421000",
                          "PH036916000","PH036918000","PH112503000","PH112505000","PH050507000","PH050508000","PH050509000","PH050510000",
                          "PH050512000","PH050513000","PH050514000","PH050516000","PH050518000","PH051718000","PH051720000","PH051727000",
                          "PH051728000","PH051731000","PH051732000","PH050502000","PH050503000","PH050504000","PH050505000","PH050506000",
                          "PH051701000","PH051702000","PH051703000","PH051704000","PH051705000","PH051706000","PH051707000","PH051708000",
                          "PH051709000","PH051710000","PH051713000","PH051716000","PH051721000","PH051722000","PH051723000","PH051724000",
                          "PH051725000","PH051726000","PH051736000","PH061901000","PH061902000","PH061903000","PH061904000","PH061905000",
                          "PH061906000","PH061907000","PH061908000","PH061909000","PH061910000","PH061911000","PH061912000","PH061913000",
                          "PH061914000","PH061915000","PH061916000","PH061917000","PH118201000","PH118210000","PH118207000","PH118208000",
                          "PH118209000","PH124703000","PH124708000","PH124711000","PH124712000","PH129804000","PH160210000","PH160211000",
                          "PH160212000","PH160208000","PH160209000","PH153807000","PH153810000","PH153812000","PH153814000","PH153822000",
                          "PH153834000","PH160201000","PH160202000","PH160203000","PH160204000","PH160205000","PH160206000","PH160207000",
                          "PH160301000","PH160302000","PH160303000","PH160304000","PH160305000","PH160306000","PH160307000","PH160308000",
                          "PH160309000","PH160310000","PH160311000","PH160312000","PH160313000","PH160314000"]
