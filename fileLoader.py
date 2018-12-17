# Sample Python script for reading a file and storing the records in a DB
from dg.FileDAO import FileDAO

import platform
import logging
import logging.config
import hashlib

#
def calculateHash(fileName):
  BLOCKSIZE = 65536
  hasher = hashlib.sha1()
  with open(fileName, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
      hasher.update(buf)
      buf = afile.read(BLOCKSIZE)

  return hasher.hexdigest()

# ------------- APPLICATION START -------------
# setup application logging
logging.config.fileConfig('logging.conf')

logging.info('Python ' + platform.python_version() + ' File Loader running on ' + str(platform.system()) + ' ' + str(platform.release()))

try:
  fileName = 'sample.csv'
  hash = calculateHash(fileName)
  logging.info('hash>> ' + hash)

  dao = FileDAO()
  dao.create(fileName,hash)

  # open file and loop for each line
  with open(fileName,'rt') as srcFile:
    # TODO save records and encrypt
    # TODO move files from incoming to outgoing??
    # TODO check for dupe files in last 24 hrs
    # TODO look into folder every 2 mins indefinitly

    for line in srcFile:
      pass

except FileNotFoundError as ex:
  logging.error('File [' + fileName + '] not found')
except Exception as ex:
  logging.exception('Unknown error occured!?')