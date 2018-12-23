# Sample Python script for reading a file and calling an external REST API

from dg.CardClient import CardClient
from dg.LineParser import LineParser
from dg.CardResponse import CardResponse
from dg.RecordDAO import RecordDAO
from config import config
from cryptography.fernet import Fernet
from dg.FileService import SecretKeyNotFoundException

import platform
import concurrent.futures
import uuid
import datetime
import time
import os
import logging
import logging.config

# decrypts the raw record data for processing
def decryptRec(secretKey, record):
  fernet = Fernet(secretKey)
  dataAsBytes = bytes(record.rawData,'utf-8')
  token = fernet.decrypt(dataAsBytes)
  return token.decode('utf-8')

# function for processing a single record
def processReq(recordId, line):
  guid = str(uuid.uuid4())

  try:
    parser = LineParser()
    lineReq = parser.parse(recordId, line)
    lineReq.guid = guid
    lineReq.ref = guid # we do this to make sure records work due to test data, not needed in PROD

    logging.info('Sending reference ' + lineReq.ref + ' with amount ' + lineReq.amount)
    dao.updateSent(lineReq)

    return client.purchase(config['accountId'], lineReq)
  except Exception as ex:
    logging.warning(guid + ' Line processing failed: ' + str(ex))
    resp = CardResponse(recordId, 'ERROR', guid)
    resp.message = str(ex)
    return resp

# function for processing the record response
def processRes(result):
  logging.info(result.toString())
  dao.updateResponse(result)

# ------------- APPLICATION START -------------
# setup application logging
logging.config.fileConfig('logging.conf')

logging.info('Python ' + platform.python_version() + ' File Processor running on ' + str(platform.system()) + ' ' + str(platform.release()))

try:
  secretKey = str(os.getenv('DG_SECRET_KEY')).encode()
  if secretKey == None:
    raise SecretKeyNotFoundException()

  maxThreads = config['maxThreads']

  # create client instance with some config
  client = CardClient(config['url'], config['apiUser'], config['apiPass'])
  dao = RecordDAO()

  while True:
    startTime = datetime.datetime.now()

    # get next records to process and reset statistics
    recs = dao.getAllWithStatusInitial()
    logging.info('Processing ' + str(len(recs)) + ' record(s)')
    logging.info('-------------------------------')
    requestCnt = 0
    successCnt = 0
    failedCnt = 0

    # start thread pool with maximum number of threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxThreads) as executor:
      allFutures = []

      # loop thru each record and submit to the pool for execution
      for rec in recs:
        line = decryptRec(secretKey, rec)
        future = executor.submit(processReq, rec.recordId, line)
        allFutures.append(future)

      # loop thru each completed thread and handle result
      for future in concurrent.futures.as_completed(allFutures):
        if future.result().decision == 'SUCCESS':
          successCnt += 1
        elif future.result().decision == 'FAILED':
          failedCnt += 1

        processRes(future.result())
        requestCnt += 1

    endTime = datetime.datetime.now()
    logging.info('-------------------------------')
    logging.info('Processed ' + str(requestCnt) + ' record(s) in ' + str(endTime - startTime) \
      + ' - ' + str(successCnt) + ' succeeded, ' + str(failedCnt) + ' failed')
    time.sleep(60)

except SecretKeyNotFoundException as ex:
  logging.error('Encryption key not found in environment variable DG_SECRET_KEY')
except Exception as ex:
  logging.exception('Unknown error occured!?')