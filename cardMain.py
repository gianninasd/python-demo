# Sample Python script for calling an external REST API

from CardClient import CardClient
from CardRequest import CardRequest
from config import config

import platform
import concurrent.futures
import uuid

requestCnt = 0

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
  client.purchase(config['accountId'], lineReq)

ex = concurrent.futures.ThreadPoolExecutor(max_workers=5)

# loop thru each record and submit to the pool for execution
for line in srcFile:
  ex.submit(processReq, line)
  requestCnt = requestCnt + 1

print('Submitted ' + str(requestCnt) + ' record(s) for processing')