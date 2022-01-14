######################
## COUNTRY SETTINGS ##
######################

SETTINGS = {
    "ZMB": {
        'IBF_API_URL': 'https://ibf-test.510.global/api/',
        'PASSWORD': 'password',
        'mock': False,
        'if_mock_trigger': False,
        'notify_email': True,
        'lead_times': {
            "7-day": 7
        },
        'admin_level': 3,
        'levels':[3,2,1],
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/hrsl_zmb_pop_resized_100",
                "rasterValue": 1
            }
        }
    },
    "UGA": {
        'IBF_API_URL': 'https://ibf-test.510.global/api/',
        'PASSWORD': 'password',
        'mock': False,
        'if_mock_trigger': False,
        'notify_email': True,
        'lead_times': {
            "5-day": 5
        },
        'admin_level': 4,
        'levels':[4,3,2,1],
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/hrsl_uga_pop_resized_100",
                "rasterValue": 1
            }
        }
    },
    "KEN": {
        'IBF_API_URL': 'https://ibf-test.510.global/api/',
        'PASSWORD': 'password',
        'mock': False,
        'if_mock_trigger': False,
        'notify_email': True,
        'lead_times': {
            "7-day": 7
        },
        'admin_level': 1,
        'levels':[3,2,1],
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/hrsl_ken_pop_resized_100",
                "rasterValue": 1
            }
        }
    },
    "ETH": {
        'IBF_API_URL': 'https://ibf-test.510.global/api/',
        'PASSWORD': 'password',
        'mock': False,
        'if_mock_trigger': False,
        'notify_email': True,
        'lead_times': {
            "7-day": 7
        },
        'admin_level': 3,
        'levels':[3],
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/worldpop_eth",
                "rasterValue": 1
            }
        }
    }
}

##################
## RUN SETTINGS ##
##################
 
# Countries to include

COUNTRY_CODES = ['ZMB', 'ETH', 'UGA'] #['ZMB','ETH','UGA',

GOOGLE_DRIVE_DATA_URL = 'https://drive.google.com/file/d/1vptMfC_IVm4EwEC67G1Q_KoapxeQCiCc/view?usp=sharing'


# Change this date only in case of specific testing purposes
from datetime import date, timedelta
CURRENT_DATE = date.today()
#CURRENT_DATE=date.today() - timedelta(1) # to use yesterday's date




####################
## OTHER SETTINGS ##
####################

# Nr. of max open files, when pipeline is ran from cronjob.
# Should be larger then the nr of admin-areas on the relevant admin-level handled (e.g. 1040 woreda's in ETH)
SOFT_LIMIT = 10000

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
GLOFAS_FILENAME = 'glofas_pointdata_ZambiaRedcross'


#####################
## ATTRIBUTE NAMES ##
#####################

TRIGGER_LEVEL = 'triggerLevel'
LEAD_TIME = 'leadTime'
