# @author Dimitrios Gianninas
# Sample Python script for calling an external REST API

from CardClient import CardClient
from config import config

# create client instance with some config
client = CardClient(config['url'], config['apiUser'], config['apiPass'])

# make purchase request
client.purchase(config['accountId'])
