import os
#API_LOGIN_URL = os.environ["API_LOGIN_URL"]
#API_SERVICE_URL = os.environ["API_SERVICE_URL"]
#IBF_API_URL=os.environ["IBF_API_URL"]
ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
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

# COUNTRY SETTINGS
SETTINGS_SECRET = {
    "ZMB": {
        "IBF_API_URL":'https://ibf-test.510.global/api/',
        "mock": True,
        "if_mock_trigger": True,
        "notify_email": False
    },
    "UGA": {
        "IBF_API_URL":'https://ibf-test.510.global/api/',
        "mock": True,
        "if_mock_trigger": True,
        "notify_email": False
    },
    "KEN": {
        "IBF_API_URL":'https://ibf-test.510.global/api/',
        "mock": True,
        "if_mock_trigger": False,
        "notify_email": False,
        
    },
    "ETH": {
        "IBF_API_URL":'https://ibf-test.510.global/api/',
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False
    }
}
