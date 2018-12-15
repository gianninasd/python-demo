# Python script calling an external REST API using concurrency running for a maximum X minutes

from dg.CardClient import CardClient
from dg.CardRequest import CardRequest
from dg.CardResponse import CardResponse
from config import config

import logging
import logging.config
import datetime
import concurrent.futures
import uuid
import platform

# setup application logging
logging.config.fileConfig('logging.conf')

# create client instance with some config
client = CardClient(config['url'], config['apiUser'], config['apiPass'])

# function for processing a single record
def processReq(line):
  lineReq = CardRequest()
  lineReq.parse(line)
  lineReq.guid = str(uuid.uuid1())
  lineReq.ref = lineReq.guid # we do this to make sure records work due to test data

  logging.info('Sending reference ' + lineReq.ref + ' with amount ' + lineReq.amount)

  return client.purchase(config['accountId'], lineReq)

# function for processing the record response
def processRes(result):
  logging.info(result.toString())

requestCnt = 0
successCnt = 0
failedCnt = 0
startTime = datetime.datetime.now()
rightnow = datetime.datetime.now()
maxThreads = int(config['maxThreads'])
fileName = 'runner_sample.csv'
sampleData = []

logging.info('Python ' + platform.python_version() + ' File Processor running on ' + str(platform.system()) + ' ' + str(platform.release()))
logging.info('Load test running for ' + str(config['runnerMins']) + ' with ' + str(config['maxRequests']) + ' threads')

try:
  # open file and load each record into memory
  srcFile = open(fileName,'rt')
  for line in srcFile:
    sampleData.append(line)

  # start thread pool with maximum number of threads
  with concurrent.futures.ThreadPoolExecutor(max_workers=maxThreads) as executor:
    allFutures = []

    while ((rightnow - startTime).total_seconds() / 60) < int(config['runnerMins']) and requestCnt < int(config['maxRequests']):
      for i in range(100):
        for rec in sampleData:
          future = executor.submit(processReq, rec)
          allFutures.append(future)

      # loop thru each completed thread and handle result
      for future in concurrent.futures.as_completed(allFutures):
        if future.result().decision == 'SUCCESS':
          successCnt += 1
        elif future.result().decision == 'FAILED':
          failedCnt += 1

        processRes(future.result())
        requestCnt += 1

      rightnow = datetime.datetime.now()

  endTime = datetime.datetime.now()
  elapsedMins = (endTime - startTime).total_seconds() / 60
  pctSuccess = round((successCnt / (successCnt + failedCnt))*100)

  logging.info('startTime: ' + str(startTime))
  logging.info('endTime: ' + str(endTime))
  logging.info('elapsed time: ' + str(elapsedMins))

  logging.info('Processed ' + str(requestCnt) + ' record(s) in ' + str(endTime - startTime) \
      + ' - ' + str(successCnt) + ' succeeded (' + str(pctSuccess) + '%), ' + str(failedCnt) + ' failed')

except FileNotFoundError as ex:
  logging.error('File [' + fileName + '] not found')
except Exception as ex:
  logging.exception('Unknown error occured!?')