# Sample Python script for reading a file and calling an external REST API

from dg.CardClient import CardClient
from dg.LineParser import LineParser
from dg.CardResponse import CardResponse
from dg.RecordDAO import RecordDAO
from config import config

import platform
import concurrent.futures
import uuid
import datetime
import sys
import logging
import logging.config

# define custom exception
class InvalidArguments(Exception):
  pass

# validates that the command line has the neccesary arguments
def validateCommandLine(args):
  if len(args) != 2:
    raise InvalidArguments()

# function for processing a single record
def processReq(line):
  guid = str(uuid.uuid4())

  try:
    parser = LineParser()
    lineReq = parser.parse(line)
    lineReq.guid = guid
    lineReq.ref = guid # we do this to make sure records work due to test data, not needed in PROD

    logging.info('Sending reference ' + lineReq.ref + ' with amount ' + lineReq.amount)
    dao.create(lineReq)

    return client.purchase(config['accountId'], lineReq)
  except Exception as ex:
    logging.warning(guid + ' Line processing failed: ' + str(ex))
    resp = CardResponse('ERROR', guid)
    resp.message = str(ex)
    return resp

# function for processing the record response
def processRes(result):
  logging.info(result.toString())
  dao.update(result)

# ------------- APPLICATION START -------------
# setup application logging
logging.config.fileConfig('logging.conf')

logging.info('Python ' + platform.python_version() + ' File Processor running on ' + str(platform.system()) + ' ' + str(platform.release()))

try:
  validateCommandLine(sys.argv)
except InvalidArguments as ex:
  logging.warning('Missing or too many arguments, should be fileProc.py <filename>')
  sys.exit(1)

requestCnt = 0
successCnt = 0
failedCnt = 0
fileName = sys.argv[1]

# create client instance with some config
client = CardClient(config['url'], config['apiUser'], config['apiPass'])
dao = RecordDAO()

logging.info('Processing file [' + fileName + ']')
logging.info('-------------------------------')

try:
  startTime = datetime.datetime.now()

  # open file and loop for each line
  srcFile = open(fileName,'rt')

  # start thread pool with maximum number of threads
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    allFutures = []

    # loop thru each record and submit to the pool for execution
    for line in srcFile:
      future = executor.submit(processReq, line)
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

except FileNotFoundError as ex:
  logging.error('File [' + fileName + '] not found')
except Exception as ex:
  logging.exception('Unknown error occured!?')