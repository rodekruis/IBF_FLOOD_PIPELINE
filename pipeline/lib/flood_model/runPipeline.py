from flood_model.forecast import Forecast
import traceback
import time
import datetime
from flood_model.settings import *
from flood_model.secrets import *
import resource
import os
import logging
from google_drive_downloader import GoogleDriveDownloader as gdd

#GLOFAS_API_KEY = os.environ["GLOFAS_API_KEY"]
#GLOFAS_API_URL = os.environ.get("GLOFAS_API_URL")
#GLOFAS_USER = os.environ["GLOFAS_USER"]
#ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN")
#GLOFAS_PW = os.environ["GLOFAS_PW"]
#ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
#GLOFAS_FTP = os.environ["GLOFAS_FTP"]
#DATALAKE_STORAGE_ACCOUNT_NAME = os.environ["DATALAKE_STORAGE_ACCOUNT_NAME"]
#DATALAKE_STORAGE_ACCOUNT_KEY = os.environ["DATALAKE_STORAGE_ACCOUNT_KEY"]
#DATALAKE_API_VERSION = os.environ["DATALAKE_API_VERSION"]
#API_LOGIN_URL = os.environ["API_LOGIN_URL"]
#API_SERVICE_URL = os.environ["API_SERVICE_URL"]

def setup_logger():
    # Set up logger
    logging.root.handlers = []
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG, filename='ex.log')
    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

setup_logger()
logger = logging.getLogger(__name__)
 

def main():
    soft_limit,hard_limit = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (SOFT_LIMIT, hard_limit))

    startTime = time.time() 
    logger.info(str(datetime.datetime.now()))
    gdd.download_file_from_google_drive(file_id='1vptMfC_IVm4EwEC67G1Q_KoapxeQCiCc',dest_path='./data/data_flood.zip',overwrite=True,unzip=True)
    logger.info('finished data download')
    print(str(datetime.datetime.now()))
    gdd.download_file_from_google_drive(file_id='1vptMfC_IVm4EwEC67G1Q_KoapxeQCiCc',
                                    dest_path='./data/data_flood.zip',
                                    overwrite=True,
                                    unzip=True)
    print('finished data download')


    try:
        for COUNTRY_CODE in COUNTRY_CODES:
            logger.info('--------STARTING: ' + COUNTRY_CODE +
                  '--------------------------')

            COUNTRY_SETTINGS = SETTINGS[COUNTRY_CODE]
            LEAD_TIMES = COUNTRY_SETTINGS['lead_times']
            #IBF_API_URL = SETTINGS[COUNTRY_CODE]['IBF_API_URL']

            for leadTimeLabel, leadTimeValue in LEAD_TIMES.items():
                logger.info('--------STARTING: ' + leadTimeLabel +
                      '--------------------------')
                fc = Forecast(leadTimeLabel, leadTimeValue, COUNTRY_CODE,COUNTRY_SETTINGS['admin_level'])
                fc.glofasData.process()
                logger.info('--------Finished GLOFAS data Processing')
                fc.floodExtent.calculate()
                logger.info('--------Finished flood extent')
                fc.exposure.callAllExposure()
                logger.info('--------Finished exposure')
                fc.db.upload()
                logger.info('--------Finished upload')
                fc.db.sendNotification()
                logger.info('--------Finished notification')

    except Exception as e:
        print(e)
        logger.error("PIPELINE EROR")

    elapsedTime = str(time.time() - startTime)
    print(elapsedTime)

if __name__ == "__main__":
    main()
