# Sample Python script for calling an external REST API

from CardClient import CardClient
from CardRequest import CardRequest
from config import config

import platform
import concurrent.futures
import uuid
import datetime

requestCnt = 0
successCnt = 0
failedCnt = 0

print('Python File Processor running on ' + str(platform.system()) + ' ' + str(platform.release()))
print('-------------------------------')

# create client instance with some config
client = CardClient(config['url'], config['apiUser'], config['apiPass'])

# function for processing a single record
def processReq(line):
  lineReq = CardRequest()
  lineReq.parse(line)
  lineReq.guid = uuid.uuid1().hex
  lineReq.ref = lineReq.guid # we do this to make sure records works due to test data

  dt = datetime.datetime.now()
  dtAsStr = dt.strftime("%x %X:%f")
  print(dtAsStr + ' Sending reference ' + lineReq.ref + ' with amount ' + lineReq.amount)

  return client.purchase(config['accountId'], lineReq)

# function for processing the record response
def processRes(result):
  dt = datetime.datetime.now()
  dtAsStr = dt.strftime("%x %X:%f")
  print(dtAsStr + ' ' + result.toString())

try:
  startTime = datetime.datetime.now()

  # open file and loop for each line
  srcFile = open('sample.csv','rt')

  # start thread pool with maximum number of threads
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
    allFutures = []

    # loop thru each record and submit to the pool for execution
    for line in srcFile:
      future = ex.submit(processReq, line)
      allFutures.append(future)

    # loop thru each completed thread and handle result
    for f in concurrent.futures.as_completed(allFutures):
      if f.result().decision == 'SUCCESS':
        successCnt += 1
      elif f.result().decision == 'FAILED':
        failedCnt += 1

      processRes(f.result())
      requestCnt += 1

  endTime = datetime.datetime.now()
  print('-------------------------------')
  print('Processed ' + str(requestCnt) + ' record(s) in ' + str(endTime - startTime) \
    + ' - ' + str(successCnt) + ' succeeded, ' + str(failedCnt) + ' failed')

except FileNotFoundError as e:
  print('File not found')
except Exception as e:
  print('Unknown error occured: ' + str(e))