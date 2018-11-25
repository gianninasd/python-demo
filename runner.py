# Python script calling an external REST API using concurrency running for a maximum X minutes

from CardClient import CardClient
from dg.CardRequest import CardRequest
from dg.CardResponse import CardResponse
from config import config

import logging
import logging.config
import datetime
import concurrent.futures
import uuid

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

somedata = ['jim7025,1500,4111111111111111,10,2020,Rick,Hunter,rick@sdf3.com,M5H 2N2',
  'jim7025,5,4111111111111111,10,2020,Rick,Hunter,rick@sdf3.com,M5H 2N2',
  'jim7025,1500,4111111111111111,10,2020,Rick,Hunter,rick@sdf3.com,M5H 2N2',
  'jim7025,1500,4111111111111111,10,2020,Rick,Hunter,rick@sdf3.com,M5H 2N2']

requestCnt = 0
successCnt = 0
failedCnt = 0
startTime = datetime.datetime.now()
rightnow = datetime.datetime.now()

# start thread pool with maximum number of threads
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
  allFutures = []

  while ((rightnow - startTime).total_seconds() / 60) < 2 and requestCnt < 2500:
    for i in range(100):
      for rec in somedata:
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

x = endTime - startTime

logging.info('startTime: ' + str(startTime))
logging.info('endTime: ' + str(endTime))
logging.info('elapsed time: ' + str(x.total_seconds() / 60))

logging.info('Processed ' + str(requestCnt) + ' record(s) in ' + str(endTime - startTime) \
    + ' - ' + str(successCnt) + ' succeeded, ' + str(failedCnt) + ' failed')