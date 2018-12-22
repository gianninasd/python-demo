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
  secretKey = os.getenv('DG_SECRET_KEY')
  if secretKey == None:
    raise SecretKeyNotFoundException()
  
  fileName = 'sample.csv'
  service = FileService(secretKey)
  fileId = service.create(fileName)
  logging.info('Processing records for file id ' + str(fileId))

  # open file and loop for each line
  with open(fileName,'rt') as srcFile:
    # TODO move files from incoming to outgoing??
    # TODO look into folder every 2 mins indefinitly
    # TODO generate ack file?

    for line in srcFile:
      service.storeRecord(fileId, line)

except SecretKeyNotFoundException as ex:
  logging.error('Encryption key not found in environment variable DG_SECRET_KEY')
except FileNotFoundError as ex:
  logging.error('File [' + fileName + '] not found')
except DupeFileException as ex:
  logging.error('File [' + fileName + '] already uploaded in the last 24 hrs')
except Exception as ex:
  logging.exception('Unknown error occured!?')