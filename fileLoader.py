# Sample Python script for reading a file and storing the records in a DB

from dg.FileService import FileService, DupeFileException

import platform
import logging
import logging.config

# ------------- APPLICATION START -------------
# setup application logging
logging.config.fileConfig('logging.conf')

logging.info('Python ' + platform.python_version() + ' File Loader running on ' + str(platform.system()) + ' ' + str(platform.release()))

try:
  fileName = 'sample.csv'
  service = FileService()
  service.create(fileName)

  # open file and loop for each line
  with open(fileName,'rt') as srcFile:
    # TODO save records and encrypt
    # TODO move files from incoming to outgoing??
    # TODO look into folder every 2 mins indefinitly

    for line in srcFile:
      pass

except FileNotFoundError as ex:
  logging.error('File [' + fileName + '] not found')
except DupeFileException as ex:
  logging.error('File [' + fileName + '] already uploaded in the last 24 hrs')
except Exception as ex:
  logging.exception('Unknown error occured!?')