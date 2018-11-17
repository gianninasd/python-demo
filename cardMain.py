# Sample Python script for calling an external REST API

from CardClient import CardClient
from CardRequest import CardRequest
from config import config

# create client instance with some config
client = CardClient(config['url'], config['apiUser'], config['apiPass'])

# open file and loop for each line
srcFile = open('sample.csv','rt')

for line in srcFile:
  #print(line)
  lineReq = CardRequest()
  lineReq.parse(line)

  # make purchase request
  client.purchase(config['accountId'], lineReq)
  print() # empty line