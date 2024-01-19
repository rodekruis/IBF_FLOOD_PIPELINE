from flood_model.forecast import Forecast
import traceback
import time
import datetime
from flood_model.settings import *
#from flood_model.dynamicDataDb import DatabaseManager as dbm
try:
    from flood_model.secrets import *
except ImportError:
    print('No secrets file found.')
from flood_model.exposure import Exposure 
import resource
import os
import logging
import zipfile
from flood_model.googledrivedata import downloaddatalack 

            
        
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


logger = logging.getLogger(__name__)



def main():
    startTime = time.time() 
    logger.info(str(datetime.datetime.now()))
    ## download data from Datalack  
    logger.info(IBF_URL)

    
    if len(COUNTRY_CODES)==1:
        countryCode=COUNTRY_CODES[0].lower()
        filename=f'data_{countryCode}.zip'
        if not os.path.exists(filename):
            downloaddatalack(countryCode)
            
            path_to_zip_file='./'+filename 
            with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                zip_ref.extractall('./data') 
    else:
        countryCode=None
        filename='data.zip'
        if not os.path.exists(filename):
            downloaddatalack(countryCode)        
            path_to_zip_file='./'+filename 
            with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                zip_ref.extractall('./data') 
    
    #gdd.download_file_from_google_drive(file_id=GOOGLE_DRIVE_DATA_URL,dest_path='./data/data_flood.zip',overwrite=True,unzip=True)
    logger.info('finished data download')
 
    logger.info(str(datetime.datetime.now()))


    try:
        for COUNTRY_CODE in COUNTRY_CODES:
            logger.info(f'--------STARTING: {COUNTRY_CODE}' + '--------------------------')
            COUNTRY_SETTINGS = SETTINGS[COUNTRY_CODE]
            LEAD_TIMES = COUNTRY_SETTINGS['lead_times']

            for leadTimeLabel, leadTimeValue in LEAD_TIMES.items():
                logger.info(f'--------STARTING: {leadTimeLabel}' + '--------------------------')
                fc = Forecast(leadTimeLabel, leadTimeValue, COUNTRY_CODE,COUNTRY_SETTINGS['admin_level'])
                fc.glofasData.process()
                logger.info('--------Finished GLOFAS data Processing')
                fc.floodExtent.calculate()
                logger.info('--------Finished flood extent')
                fc.exposure.callAllExposure()
                logger.info('--------Finished exposure')
                if COUNTRY_CODE =='SSD':
                    fc.exposure.makeMaps()
                    logger.info('--------Finished make maps')                
                fc.db.upload()                
                logger.info('--------Finished upload')
                fc.db.sendNotification()
                logger.info('--------Finished notification')
    except Exception as e:
        logger.error("Flood Data PIPELINE ERROR")
        logger.error(e)
    elapsedTime = str(time.time() - startTime)
    logger.info(str(elapsedTime))


if __name__ == "__main__":
    main()
