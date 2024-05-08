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
fail = True
try:
     from flood_model.secrets import *
except:
     print('no secrets file')
else:
     fail = False

if fail:
    try:
        COUNTRY_CODES = ast.literal_eval(os.getenv("COUNTRY_CODES_LIST"))
        ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
        IBF_PASSWORD=os.getenv("IBF_PASSWORD")
        IBF_URL =os.getenv("IBF_URL")
        GLOFAS_USER=os.getenv("GLOFAS_USER")
        GLOFAS_PW=os.getenv("GLOFAS_PW")
        GLOFAS_FTP='aux.ecmwf.int'  

    except:
        print('No environment variables found localy.')
        COUNTRY_CODES = ["SSD","UGA","ETH","KEN","ZMB"]
    else:
         fail = False
 


# 2. Try to load secrets from env-variables (i.e. when using Github Actions)
if fail:
    try:
        COUNTRY_CODES = ast.literal_eval(os.environ["COUNTRY_CODES"])
        ADMIN_LOGIN = os.environ["ADMIN_LOGIN"]
        IBF_PASSWORD=os.environ["IBF_PASSWORD"]
        IBF_URL=os.environ["IBF_URL"]   
    

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


# If neither of the 2 options apply, this script will fail.
'''
######################
## COUNTRY SETTINGS (this is now definde as an enviromental variable)##
######################
 

 
SETTINGS = {
    "MWI": {
            "IBF_API_URL": IBF_URL,
            "PASSWORD": IBF_PASSWORD,
            "mock": False,
            "if_mock_trigger": False,
            "placeCodeInitial": 'MWI',
            "glofasReturnPeriod":'rl5',
            "selectedPcode":[],
            "placecodeLen":6, #LENGTH OF CHARS IN ADMIN3 PLACECODE -LENGTH OF CHARS IN COUNTRYCODEiso
            "notify_email": True,
            'lead_times': {
                "6-day": 6
            },
            'TRIGGER_LEVELS':{"minimum": 0.6,"medium": 0.7,"maximum": 0.8},
            'eapAlertClass':{"no": 0.6,"max": 0.601},
            'admin_level': 3,
            'admin_level_glofas_extr': 3,
            'levels':[3,2,1],
            'GLOFAS_FTP':'aux.ecmwf.int/for_ZambiaRedcross/',
            #'GLOFAS_FTP':'aux.ecmwf.int/ZambiaRedcross_glofas_point/',
            'GLOFAS_FILENAME':'glofas_pointdata_ZambiaRedcross',  
            'EXPOSURE_DATA_SOURCES': {
                "population": {
                    "source": "population/population_mwi",
                    "rasterValue": 1
               }
            },
            'EXPOSURE_DATA_UBR_SOURCES': {
                "pop_u18": {
                    "source": "mwi_3_population_ubr",
                    "col_name": "ubr_pop_u18"
                },
                "pop_65": {
                    "source": "mwi_3_population_ubr",
                    "col_name": "ubr_pop_65"
                }
            }
    },
    "ZMB": {
        "IBF_API_URL": IBF_URL,
        "PASSWORD": IBF_PASSWORD,
        "mock": False,
        "if_mock_trigger": False,
        "placeCodeInitial": 'ZMB',
        "glofasReturnPeriod":'rl10',
        #"selectedPcode":["ZM040205810","ZM090313001","ZM020603011","ZM040306116","ZM080310511","ZM050107302","ZM080410618","ZM090913106","ZM010501001","ZM100514502","ZM100514614","ZM070309004","ZM050207007","ZM070809202","ZM100314011","ZM100615016","ZM060208301","ZM020803202","ZM010501004","ZM030605211"],
        "selectedPcode":['ZM100213922','ZM100714701','ZM090211814','ZM090512114', 'ZM091113314','ZM070309117','ZM091013213','ZM020803213', 'ZM060104022','ZM080410622','ZM040205813','ZM100615020', 'ZM070809213','ZM090111714','ZM010501116','ZM020201710','ZM060208422','ZM021003628'],
        "placecodeLen":6, #LENGTH OF CHARS IN ADMIN3 PLACECODE -LENGTH OF CHARS IN COUNTRYCODEiso
        "notify_email": True,
        'lead_times': {
            "7-day": 7
        },
        'TRIGGER_LEVELS':{"minimum": 0.6,"medium": 0.7,"maximum": 0.8}, # VALUES ARE PROBABILITY (E.G. 60%, 70%)
        'eapAlertClass':{"no": 0.6,"min": 0.7,"med": 0.8,"max": 0.801}, # VALUES ARE PROBABILITY (E.G. 60%, 70%)
        'admin_level': 3,
        'admin_level_glofas_extr': 3,
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
    },
    "UGA": {
        "IBF_API_URL": IBF_URL,
        "PASSWORD": IBF_PASSWORD,
        "mock": False,
        "placeCodeInitial": 'UGA',
        "if_mock_trigger": False,
        "notify_email": True,
        "glofasReturnPeriod":'rl5',
        #"selectedPcode":["UG20570101","UG20270110","UG41110113","UG20360110","UG41240112","UG20350201","UG41140116","UG10180304"] , 
        "selectedPcode": ["UG20570102","UG20460106","UG41240115","UG20360112","UG20350212","UG41140114","UG10180304"] ,
        #"selectedPcode": ['UG41280109','UG20560114','UG20630312','UG41330302','UG10260604','UG30900108','UG20550109','UG41180107'],
        "placecodeLen":6, #LENGTH OF CHARS IN ADMIN3 PLACECODE -LENGTH OF CHARS IN COUNTRYCODEiso
        'lead_times': {
            "5-day": 5
            },
        'TRIGGER_LEVELS':{"minimum": 0.6,"medium": 0.7,"maximum": 0.8}, # multiple thresholds
        'eapAlertClass': { # ONLY FOR UGANDA VALUES ARE RETURN PERIODS (E.G. 1.5-YEAR RP, 2-YEAR RP)
            "no": 1.49, 
            "min": 1.5, 
            "med": 2, 
            "max": 5
            }, 
        'admin_level': 4,
        'admin_level_glofas_extr': 4,
        'levels':[4,3,2,1],
        'GLOFAS_FTP':'aux.ecmwf.int/for_ZambiaRedcross/',
        #'GLOFAS_FTP':'aux.ecmwf.int/ZambiaRedcross_glofas_point/',
        'GLOFAS_FILENAME':'glofas_pointdata_ZambiaRedcross',   
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/hrsl_uga_pop_resized_100",
                "rasterValue": 1
            }
        }
    },
    "KEN": {
        "IBF_API_URL": IBF_URL,
        "PASSWORD": IBF_PASSWORD,
        "mock": False,
        "placeCodeInitial": 'KEN', 
        "if_mock_trigger": True,
        "placecodeLen":6, #LENGTH OF CHARS IN ADMIN3 PLACECODE -LENGTH OF CHARS IN COUNTRYCODEiso
        "notify_email": True,
        "glofasReturnPeriod":'rl5',
        #"selectedPcode":["KE0392221108","KE0402301149","KE0402301150","KE0402301151","KE0402311153","KE0402311154","KE0402311155","KE0371990995","KE0030150072","KE0030150074","KE0030160075","KE0030160076","KE0030170080","KE0030170083","KE0030170084","KE0050220109","KE0060260126","KE0040180088","KE0040180089","KE0040180091","KE0040190092","KE0040190093","KE0040190094","KE0040200096"],
        "selectedPcode":['KE0050220109', 'KE0402311155', 'KE0060260126'],
        'lead_times': {
            "7-day": 7
        },
        'TRIGGER_LEVELS':{"minimum": 0.6,"medium": 0.7,"maximum": 0.8},
        'eapAlertClass':{"no": 0.85,"max": 0.851},
        'admin_level': 3,
        'admin_level_glofas_extr': 3,
        'levels':[3,2,1],
        #'GLOFAS_FTP':'aux.ecmwf.int/ZambiaRedcross_glofas_point/',
        'GLOFAS_FTP':'aux.ecmwf.int/for_ZambiaRedcross/',
        'GLOFAS_FILENAME':'glofas_pointdata_ZambiaRedcross',   
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/hrsl_ken_pop_resized_100",
                "rasterValue": 1
            }
        }
    },
    "ETH": {
        "IBF_API_URL": IBF_URL,
        "PASSWORD": IBF_PASSWORD,
        "placeCodeInitial": 'ETH',
        "mock": False,
        "if_mock_trigger": False,
        "placecodeLen":6, #LENGTH OF CHARS IN ADMIN3 PLACECODE -LENGTH OF CHARS IN COUNTRYCODEiso
        "notify_email": True,
        "glofasReturnPeriod":'rl10',
        #"selectedPcode":['ET020101','ET020103','ET020104','ET020105','ET020106','ET020301','ET020302','ET020303','ET020304','ET020402','ET020502','ET020503','ET030202','ET030203','ET030204','ET030209','ET030308','ET030422','ET030701','ET030702','ET030703','ET030704','ET040405','ET040408','ET040509','ET040701','ET040703','ET040803','ET040811','ET041007','ET041207','ET041208','ET041212','ET042101','ET042102','ET042103','ET042105','ET050101','ET050103','ET050601','ET050603','ET050604','ET050605','ET050606','ET050607','ET050805','ET050901','ET050902','ET050904','ET070111','ET070112','ET070501','ET070701','ET070704','ET070705','ET070706','ET070707','ET071011','ET071601','ET072401','ET120101','ET120102','ET120103','ET120104','ET120203','ET120204','ET120206','ET120407','ET130101'],
        "selectedPcode":['ET070501', 'ET130101', 'ET020104', 'ET120407', 'ET070112', 'ET050601', 'ET071601', 'ET030422', 'ET030703', 'ET042102', 'ET050904', 'ET120204', 'ET040408', 'ET040509', 'ET030204', 'ET050103', 'ET030704', 'ET070111', 'ET042103', 'ET072401', 'ET041212', 'ET020303', 'ET030209', 'ET050902', 'ET020503', 'ET050607', 'ET040703', 'ET050805'],
        'lead_times': {
            "7-day": 7
        },
        'TRIGGER_LEVELS':{"minimum": 0.6,"medium": 0.7,"maximum": 0.8},
        'eapAlertClass':{"no": 0.75,"max": 0.751},
        'admin_level': 3,
        'admin_level_glofas_extr': 3,
        'levels':[3,2,1],
        'GLOFAS_FTP':'aux.ecmwf.int/for_ZambiaRedcross/', 
        #'GLOFAS_FTP':'aux.ecmwf.int/ZambiaRedcross_glofas_point/', 
        'GLOFAS_FILENAME':'glofas_pointdata_ZambiaRedcross',   
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/worldpop_eth",
                "rasterValue": 1
            }
        }
    },
    "PHL": {
        "IBF_API_URL": IBF_URL,
        "PASSWORD": IBF_PASSWORD,
        "mock": False,
        "placeCodeInitial": 'PHL',
        "if_mock_trigger": False,
        "notify_email": True,
        "placecodeLen":9, #LENGTH OF CHARS IN ADMIN3 PLACECODE -LENGTH OF CHARS IN COUNTRYCODEiso
        "glofasReturnPeriod":'rl5',
        "selectedPcode":[],
        'lead_times': {
            "3-day": 3
        },
        'TRIGGER_LEVELS':{"minimum": 0.6,"medium": 0.7,"maximum": 0.8},
        'eapAlertClass':{"no": 0.7,"max": 0.701},
        'admin_level': 3,
        'admin_level_glofas_extr': 3,
        'levels':[3,2,1],
        #'GLOFAS_FTP':'aux.ecmwf.int/RedcrossPhilippines_glofas_point/', #for_RedcrossPhilippines
        'GLOFAS_FTP':'aux.ecmwf.int/for_RedcrossPhilippines/', #
        'GLOFAS_FILENAME':'glofas_pointdata_RedcrossPhilippines', 
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/hrsl_phl_pop_resized_100",
                "rasterValue": 1
            }
        }
    },
    "SSD": {
        "IBF_API_URL": IBF_URL,
        "PASSWORD": IBF_PASSWORD,
        "mock": False,
        "placeCodeInitial": 'SS',
        "if_mock_trigger": False,
        "notify_email": True,
        "glofasReturnPeriod":'rl5',
        "selectedPcode":['SS030303'],
        "placecodeLen":6, #LENGTH OF CHARS IN ADMIN3 PLACECODE -LENGTH OF CHARS IN COUNTRYCODEiso
        'lead_times': {
            "7-day": 7
        },
        'TRIGGER_LEVELS':{"minimum": 0.6,"medium": 0.7,"maximum": 0.8},
        'eapAlertClass':{"no": 0.6,"max": 0.601},
        'admin_level': 3,
        'admin_level_glofas_extr': 3,
        'levels':[3],
        'GLOFAS_FTP':'aux.ecmwf.int/for_JBA/',
        'GLOFAS_FILENAME':'glofas_areagrid_for_JBA_in_Global', 
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/ssd_ppp_2020_adjusted",
                "rasterValue": 1
            }
        }
    }
}



####################
## OTHER SETTINGS ##
####################

# Change this date only in case of specific testing purposes

noOfGlofasEnsembles = 51 # 

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

Areas_With_GlofasStation=["PH021512000","PH021513000","PH021514000","PH021515000","PH021516000","PH021502000","PH021503000","PH021504000","PH021506000","PH021508000","PH021510000","PH023101000","PH021517000","PH021519000","PH021520000","PH021521000","PH021525000","PH023103000","PH036902000","PH021526000","PH124702000","PH021527000","PH021528000","PH021529000","PH023102000","PH023104000","PH023107000","PH023108000","PH023105000","PH023106000","PH023109000","PH023116000","PH023117000","PH023112000","PH023113000","PH023114000","PH023115000","PH023118000","PH023127000","PH023119000","PH023120000","PH023122000","PH023123000","PH023124000","PH023125000","PH023126000","PH023128000","PH023129000","PH023130000","PH023131000","PH023136000","PH023132000","PH023133000","PH023134000","PH023137000","PH023135000","PH031403000","PH031416000","PH031417000","PH031407000","PH031409000","PH031410000","PH031418000","PH035402000","PH035410000","PH035412000","PH035414000","PH035417000","PH035418000","PH036904000","PH036905000","PH035421000","PH036916000","PH036918000","PH112503000","PH112505000","PH050507000","PH050508000","PH050509000","PH050510000","PH050512000","PH050513000","PH050514000","PH050516000","PH050518000","PH051718000","PH051720000","PH051727000","PH051728000","PH051731000","PH051732000","PH050502000","PH050503000","PH050504000","PH050505000","PH050506000","PH051701000","PH051702000","PH051703000","PH051704000","PH051705000","PH051706000","PH051707000","PH051708000","PH051709000","PH051710000","PH051713000","PH051716000","PH051721000","PH051722000","PH051723000","PH051724000","PH051725000","PH051726000","PH051736000","PH061901000","PH061902000","PH061903000","PH061904000","PH061905000","PH061906000","PH061907000","PH061908000","PH061909000","PH061910000","PH061911000","PH061912000","PH061913000","PH061914000","PH061915000","PH061916000","PH061917000","PH118201000","PH118210000","PH118207000","PH118208000","PH118209000","PH124703000","PH124708000","PH124711000","PH124712000","PH129804000","PH160210000","PH160211000","PH160212000","PH160208000","PH160209000","PH153807000","PH153810000","PH153812000","PH153814000","PH153822000","PH153834000","PH160201000","PH160202000","PH160203000","PH160204000","PH160205000","PH160206000","PH160207000","PH160301000","PH160302000","PH160303000","PH160304000","PH160305000","PH160306000","PH160307000","PH160308000","PH160309000","PH160310000","PH160311000","PH160312000","PH160313000","PH160314000"]
