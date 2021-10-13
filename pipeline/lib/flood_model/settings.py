######################
## COUNTRY SETTINGS ##
######################

SETTINGS = {
    "ZMB": {
        'lead_times': {
            "7-day": 7
        },
        'admin_level': 3,
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/hrsl_zmb_pop_resized_100",
                "rasterValue": 1
            }
        }
    },
    "UGA": {
        'lead_times': {
            "5-day": 5
        },
        'admin_level': 3,
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/hrsl_uga_pop_resized_100",
                "rasterValue": 1
            }
        }
    },
    "KEN": {
        'lead_times': {
            "7-day": 7
        },
        'admin_level': 3,
        'EXPOSURE_DATA_SOURCES': {
            "population": {
                "source": "population/hrsl_ken_pop_resized_100",
                "rasterValue": 1
            }
        }
    },
    "ETH": {
        'lead_times': {
            "7-day": 7
        },
        'admin_level': 3,
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
COUNTRY_CODES = ['ETH','ZMB','UGA']

# COUNTRY SETTINGS
SETTINGS_SECRET = {
    "ZMB": {
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False
    },
    "UGA": {
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False
    },
    "KEN": {
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False
    },
    "ETH": {
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False
    }
}
# Change this date only in case of specific testing purposes
from datetime import date, timedelta
CURRENT_DATE = date.today()
# CURRENT_DATE=date.today() - timedelta(1) # to use yesterday's date




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
