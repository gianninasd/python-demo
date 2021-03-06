# Sample Python script for reading a file and storing the records in a DB

from dg.FileService import FileService, DupeFileException, SecretKeyNotFoundException
from config import config

import time
import os
import platform
import logging
import logging.config

# ------------- APPLICATION START -------------
# setup application logging
logging.config.fileConfig('logging.conf')

logging.info('Python ' + platform.python_version() + ' File Loader running on ' + str(platform.system()) + ' ' + str(platform.release()))

try:
  secretKey = str(os.getenv('DG_SECRET_KEY')).encode()
  if secretKey == None:
    raise SecretKeyNotFoundException()
  
  cnt = 0
  workingDir = config['workingDir']
  service = FileService(secretKey)

  while True:
    logging.info('Processing files in ' + workingDir)

    # loop for each file in the working directory
    for fullFileName in os.listdir(workingDir):
      if os.path.isfile(workingDir + '/' + fullFileName):
        try:
          fileName = service.extractFileName(fullFileName)
          fileId = service.create(workingDir, fullFileName)
          logging.info('Processing [' + fullFileName + '] records with file id ' + str(fileId))
          cnt = 0

          # open file and loop for each line
          with open(workingDir + '/' + fullFileName,'rt') as srcFile:
            for line in srcFile:
              service.storeRecord(fileId, line)
              cnt += 1

          logging.info('Finished storing ' + str(cnt) + ' records for file id ' + str(fileId))
          service.createAck(workingDir,fileName,'0','File received')
        
        except FileNotFoundError as ex:
          logging.warning('File [' + fullFileName + '] not found')
        except DupeFileException as ex:
          logging.warning('File [' + fullFileName + '] already uploaded in the last 24 hrs')
          service.createAck(workingDir,fileName,'-1','Duplicate file')
    
    logging.info('Going to sleep for 120s...')
    time.sleep(120) 

except SecretKeyNotFoundException as ex:
  logging.error('Encryption key not found in environment variable DG_SECRET_KEY')
except Exception as ex:
  logging.exception('Unknown error occured!?')
  service.createAck(workingDir,fileName,'-99','Unknown error')