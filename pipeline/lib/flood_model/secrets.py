import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


#API_LOGIN_URL = os.environ["API_LOGIN_URL"]
#API_SERVICE_URL = os.environ["API_SERVICE_URL"]
#IBF_API_URL=os.environ["IBF_API_URL"]

#ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
##glofas


##datalake
#DATALAKE_STORAGE_ACCOUNT_NAME = os.environ["DATALAKE_STORAGE_ACCOUNT_NAME"]
#DATALAKE_STORAGE_ACCOUNT_KEY = os.environ["DATALAKE_STORAGE_ACCOUNT_KEY"]
#DATALAKE_API_VERSION = os.environ["DATALAKE_API_VERSION"]

az_credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url='https://ibf-flood-keys.vault.azure.net', credential=az_credential)

ADMIN_LOGIN = secret_client.get_secret("ADMIN-LOGIN").value
GLOFAS_USER = secret_client.get_secret("GLOFAS-USER").value
GLOFAS_FTP = secret_client.get_secret("GLOFAS-FTP").value
GLOFAS_PW = secret_client.get_secret("GLOFAS-PW").value
UGA_PASSWORD=secret_client.get_secret("UGA-PASSWORD").value
ZMB_PASSWORD=secret_client.get_secret("ZMB-PASSWORD").value
ETH_PASSWORD=secret_client.get_secret("ETH-PASSWORD").value
KEN_PASSWORD=secret_client.get_secret("KEN-PASSWORD").value


# COUNTRY SETTINGS
SETTINGS_SECRET = {
    "ZMB": {
        "IBF_API_URL":'https://ibf-zambia.510.global/api/',
        "PASSWORD": ZMB_PASSWORD,
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False
    },
    "UGA": {
        "IBF_API_URL":'https://ibf-uganda.510.global/api/',
        "PASSWORD": UGA_PASSWORD,
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False
    },
    "KEN": {
        "IBF_API_URL":'https://ibf-kenya.510.global/api/',
        "PASSWORD": KEN_PASSWORD,
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False,
        
    },
    "ETH": {
        "IBF_API_URL":'https://ibf-ethiopia.510.global/api/',
        "PASSWORD": ETH_PASSWORD, 
        "mock": False,
        "if_mock_trigger": False,
        "notify_email": False
    }
}
