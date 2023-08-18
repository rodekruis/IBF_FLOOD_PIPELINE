import os 
from datetime import date, timedelta
#from dotenv import load_dotenv
from pathlib import Path
import ast
#from flood_model.secrets import *

##################
## LOAD SECRETS ##
##################
 
# 1. Try to load secrets from a local env-variables 

 
try:
    COUNTRY_CODES = ast.literal_eval(os.getenv("COUNTRY_CODES_LIST"))

    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")

    IBF_PASSWORD=os.getenv("IBF_PASSWORD")
    IBF_URL =os.getenv("IBF_URL")
 
    #GLOFAS_USER =os.getenv("GLOFAS_USER")
    #GLOFAS_PW =os.getenv("GLOFAS_PW")
    #GLOFAS_FTP =os.getenv("GLOFAS_FTP")
    #DATALAKE_STORAGE_ACCOUNT_NAME_IBFSYSTEM =os.getenv("DATALAKE_STORAGE_ACCOUNT_NAME_IBFSYSTEM")
    #DATALAKE_STORAGE_ACCOUNT_NAME =os.getenv("DATALAKE_STORAGE_ACCOUNT_NAME")

    #DATALAKE_STORAGE_IBFSYSTEM_ENDPOINT =os.getenv("DATALAKE_STORAGE_IBFSYSTEM_ENDPOINT")
    #DATALAKE_STORAGE_ENDPOINT =os.getenv("DATALAKE_STORAGE_ENDPOINT")

    #DATALAKE_STORAGE_ACCOUNT_KEY_IBFSYSTEM=os.getenv("DATALAKE_STORAGE_ACCOUNT_KEY_IBFSYSTEM")
    #DATALAKE_STORAGE_ACCOUNT_KEY=os.getenv("DATALAKE_STORAGE_ACCOUNT_KEY")
 
    
    

except:
     print('No environment variables found localy.')
 


# 2. Try to load secrets from env-variables (i.e. when using Github Actions)
 
try:
    #COUNTRY_CODES = ast.literal_eval(os.environ["COUNTRY_CODES"])
    GLOFAS_USER = os.environ.get("GLOFAS_USER")
    GLOFAS_PW = os.environ.get("GLOFAS_PW")
    GLOFAS_FTP = os.environ.get("GLOFAS_FTP")
    
    IBF_URL=os.environ.get("IBF_URL")
    ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN")
    IBF_PASSWORD=os.environ.get("IBF_PASSWORD")
    
    #ZMB_URL=os.environ["ZMB_URL"] 
    #ZMB_PASSWORD=os.environ["ZMB_PASSWORD"]
    


 

except:
     print('No environment variables found.')
# 3. Try to load secrets from Azure key vault (i.e. when running through Logic App) if user has access

'''

try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient

    if not os.getenv("AZURE_CLIENT_ID"):
        from flood_model.secrets import AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID
        os.environ["AZURE_CLIENT_ID"] = AZURE_CLIENT_ID
        os.environ["AZURE_CLIENT_SECRET"] = AZURE_CLIENT_SECRET
        os.environ["AZURE_TENANT_ID"] = AZURE_TENANT_ID

    az_credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url='https://ibf-training-keys.vault.azure.net', credential=az_credential)
    

    ADMIN_LOGIN = secret_client.get_secret("ADMIN-LOGIN").value
    GLOFAS_USER = secret_client.get_secret("GLOFAS-USER").value
    GLOFAS_PW = secret_client.get_secret("GLOFAS-PW").value
    GLOFAS_FTP = secret_client.get_secret("GLOFAS-FTP").value

    GOOGLE_DRIVE_DATA_URL = secret_client.get_secret("GOOGLE-DRIVE-DATA-URL").value
    IBF_URL=secret_client.get_secret("IBF-URL").value
    IBF_PASSWORD=secret_client.get_secret("IBF-PASSWORD").value
    COUNTRY_CODES=secret_client.get_secret("COUNTRY-CODES").value

except Exception as e:
    print('No access to Azure Key vault, skipping.')


# 3. If 1,2 and 3. fail, then assume secrets are loaded via secrets.py file (when running locally).
try:
    from flood_model.secrets import *
except ImportError:
    print("No secrets file found.")
# If neither of the 4 options apply, this script will fail.
'''
######################
## COUNTRY SETTINGS ##
######################
 
COUNTRY_CODES = ["ZMB"]
email='dunant@redcross.nl'
ADMIN_LOGIN = email

IBF_URL='https://ibf.grz.gov.zm/api/'
 
SETTINGS = {
    "ZMB": {
        "IBF_API_URL": IBF_URL,
        "PASSWORD": IBF_PASSWORD,
        "mock": False,
        "if_mock_trigger": False,
        "placeCodeInitial": 'ZMB',
        "glofasReturnPeriod":'rl10',
        "selectedPcode":[],
        "placecodeLen":6, #LENGTH OF CHARS IN ADMIN3 PLACECODE -LENGTH OF CHARS IN COUNTRYCODEiso
        "notify_email": True,
        'lead_times': {
            "7-day": 7
        },
        'TRIGGER_LEVELS':{"minimum": 0.6,"medium": 0.7,"maximum": 0.8},
        'eapAlertClass':{"no": 0.6,"min": 0.7,"med": 0.8,"max": 0.801},
        'admin_level': 3,
        'levels':[3,2,1],
        'GLOFAS_FTP':'aux.ecmwf.int/for_ZambiaRedcross/',
        #'GLOFAS_FTP':'aux.ecmwf.int/ZambiaRedcross_glofas_point/',
        'GLOFAS_FILENAME':'glofas_pointdata_ZambiaRedcross',   
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/hrsl_zmb_pop_resized_100",
                "rasterValue": 1
            }
        }
    }

}



####################
## OTHER SETTINGS ##
####################

# Change this date only in case of specific testing purposes

CURRENT_DATE = date.today()

#CURRENT_DATE=date.today() - timedelta(1) # to use yesterday's date
# if data folder should be downloaded from google drive 
GOOGLE_DRIVE_DATA_URL = 'https://drive.google.com/file/d/14MbG4uFPGJCduM5aLkvgSGqA8io6Gh9C/view?usp=sharing'


# Trigger probability 
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
logoPath = 'logo/SSD.png'

#########################
## INPUT DATA SETTINGS ##
#########################
#name of GLOFAS operational forecast on the FTP server of ECMWF
GLOFAS_GRID_FILENAME='glofas_areagrid_for_JBA_in_Global'

# Glofas input
#GLOFAS_FTP = 'data-portal.ecmwf.int/ZambiaRedcross_glofas_point/'
#GLOFAS_FILENAME = 'glofas_pointdata_ZambiaRedcross'


#####################
## ATTRIBUTE NAMES ##
#####################

TRIGGER_LEVEL = 'triggerLevel'
LEAD_TIME = 'leadTime'


### For PHL to reduce the task when running in logic-app run pipeline only for the flood prone areas 


Areas_With_GlofasStation=[]
