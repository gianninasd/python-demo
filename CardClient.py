import json
import uuid
import requests
from CardRequest import CardRequest

# Client class used to call an external REST API for transaction processing
class CardClient:
  cardUrl = ''
  apiUser = ''
  apiPass = ''

  # constructor
  def __init__(self, cardUrl, apiUser, apiPass):
    self.cardUrl = cardUrl
    self.apiUser = apiUser
    self.apiPass = apiPass

  # sends a purchase request to a remote REST API
  def purchase(self, accountId, cardRequest):
    url = self.cardUrl + accountId + '/auths'
    headers = {'content-type': 'application/json'}

    cardReq = {
      "merchantRefNum": cardRequest.ref,
      "amount": cardRequest.amount,
      "settleWithAuth": True,
      "card": {
        "cardNum": cardRequest.cardNbr,
        "cardExpiry": {
          "month": cardRequest.cardExpMth,
          "year": cardRequest.cardExpYear
        }
      },
      "billingDetails": {
        "zip": cardRequest.zipCode
      }
    }

    # send the request
    #print('Sending: ' + json.dumps(cardReq))
    print('Sending reference ' + cardReq['merchantRefNum'] + ' with amount ' + str(cardReq['amount']))
    resp = requests.post(url, headers=headers, auth=(self.apiUser, self.apiPass), data=json.dumps(cardReq))

    # process response
    if resp.status_code == 200:
      obj = resp.json()
      print('--- SUCCESSFUL id: ' + str(obj['id']) + ' status: ' + str(obj['status']) + ' authCode: ' + str(obj['authCode']))
    elif resp.status_code >= 400 or resp.status_code < 500:
      errorObj = resp.json()['error']
      print('--- BAD REQUEST (' + str(resp.status_code) + ') Error code: ' + errorObj['code'] + ' with message: ' + errorObj['message'])
      #print('Details: ' + str(errorObj['details']))
    elif resp.status_code == 500:
      print('--- OOPS, SERVER ERROR! ---')