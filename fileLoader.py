# Sample Python script for reading a file and storing the records in a DB

from dg.FileService import FileService, DupeFileException, SecretKeyNotFoundException
from config import config

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
  #print(secretKey)
  if secretKey == None:
    raise SecretKeyNotFoundException()
  
  cnt = 0
  fullFileName = 'sample.csv'
  
  service = FileService(secretKey)
  fileName = service.extractFileName(fullFileName)
  fileId = service.create(fullFileName)
  logging.info('Processing records for file id ' + str(fileId))

  # open file and loop for each line
  with open(fullFileName,'rt') as srcFile:
    # TODO move files from incoming to outgoing??
    # TODO look into folder every 2 mins indefinitly

    for line in srcFile:
      service.storeRecord(fileId, line)
      cnt += 1

  logging.info('Finished storing ' + str(cnt) + ' records for file ' + str(fileId))
  service.createAck('test',fileName,'0','File received')

except SecretKeyNotFoundException as ex:
  logging.error('Encryption key not found in environment variable DG_SECRET_KEY')
except FileNotFoundError as ex:
  logging.error('File [' + fullFileName + '] not found')
except DupeFileException as ex:
  logging.error('File [' + fullFileName + '] already uploaded in the last 24 hrs')
  service.createAck('test',fileName,'-1','Duplicate file')
except Exception as ex:
  logging.exception('Unknown error occured!?')
  service.createAck('test',fileName,'-99','Unknown error')