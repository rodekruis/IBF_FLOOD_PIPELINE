import os
#API_LOGIN_URL = os.environ["API_LOGIN_URL"]
#API_SERVICE_URL = os.environ["API_SERVICE_URL"]
#IBF_API_URL=os.environ["IBF_API_URL"]
ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN")
#ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
##glofas
GLOFAS_USER = os.environ["GLOFAS_USER"]
GLOFAS_API_KEY=os.environ["GLOFAS_API_KEY"]
GLOFAS_API_URL=os.environ["GLOFAS_API_URL"]
GLOFAS_FTP = os.environ["GLOFAS_FTP"]
GLOFAS_PW = os.environ["GLOFAS_PW"]
##google
GOOGLE_DRIVE_DATA_URL=os.environ["GOOGLE_DRIVE_DATA_URL"]
##datalake
DATALAKE_STORAGE_ACCOUNT_NAME = os.environ["DATALAKE_STORAGE_ACCOUNT_NAME"]
DATALAKE_STORAGE_ACCOUNT_KEY = os.environ["DATALAKE_STORAGE_ACCOUNT_KEY"]
DATALAKE_API_VERSION = os.environ["DATALAKE_API_VERSION"]
UGA_PASSWORD=os.environ["UGA_PASSWORD"]
ZMB_PASSWORD=os.environ["ZMB_PASSWORD"]
ETH_PASSWORD=os.environ["ETH_PASSWORD"]
KEN_PASSWORD=os.environ["KEN_PASSWORD"]
# COUNTRY SETTINGS
SETTINGS_SECRET = {
    "ZMB": {
        "IBF_API_URL":'https://ibf-zambia.510.global/api/',
        "PASSWORD": os.environ["ZMB_PASSWORD"],
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False
    },
    "UGA": {
        "IBF_API_URL":'https://ibf-uganda.510.global/api/',
        "PASSWORD": os.environ["UGA_PASSWORD"],
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False
    },
    "KEN": {
        "IBF_API_URL":'https://ibf-kenya.510.global/api/',
        "PASSWORD": os.environ["KEN_PASSWORD"],
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False,
        
    },
    "ETH": {
        "IBF_API_URL":'https://ibf-ethiopia.510.global/api/',
        "PASSWORD": os.environ["ETH_PASSWORD"],
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False
    }
}
