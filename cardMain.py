# Sample Python script for calling an external REST API

from CardClient import CardClient
from CardRequest import CardRequest
from config import config

import platform
import concurrent.futures
import uuid

requestCnt = 0
successCnt = 0
failedCnt = 0

print('Python File Processor running on ' + str(platform.system()) + ' ' + str(platform.release()))
print('-------------------------------')

# create client instance with some config
client = CardClient(config['url'], config['apiUser'], config['apiPass'])

# open file and loop for each line
srcFile = open('sample.csv','rt')

# function for processing a single record
def processReq(line):
  lineReq = CardRequest()
  lineReq.parse(line)
  lineReq.ref = uuid.uuid1().hex
  return client.purchase(config['accountId'], lineReq)

ex = concurrent.futures.ThreadPoolExecutor(max_workers=5)
allFutures = []

# loop thru each record and submit to the pool for execution
for line in srcFile:
  future = ex.submit(processReq, line)
  allFutures.append(future)

# loop thru each completed thread and handle result
for f in concurrent.futures.as_completed(allFutures):
  if f.result() == 'SUCCESS':
    successCnt += 1
  elif f.result() == 'FAILED':
    failedCnt += 1
  
  requestCnt += 1

print('-------------------------------')
print('Completed processing ' + str(requestCnt) + ' record(s) - ' + str(successCnt) + ' succeeded, ' + str(failedCnt) + ' failed')