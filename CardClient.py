import json
import uuid
import requests
import datetime
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
    dt = datetime.datetime.now()
    dtAsStr = dt.strftime("%x %X:%f")
    print(dtAsStr + ' Sending reference ' + cardReq['merchantRefNum'] + ' with amount ' + str(cardReq['amount']))
    resp = requests.post(url, headers=headers, auth=(self.apiUser, self.apiPass), data=json.dumps(cardReq))

    # process response
    dt = datetime.datetime.now()
    dtAsStr = dt.strftime("%x %X:%f")
    result = ''

    if resp.status_code == 200:
      obj = resp.json()
      print(dtAsStr + ' ' + cardReq['merchantRefNum'] + ' --- SUCCESSFUL id: ' + str(obj['id']) + ' status: ' + str(obj['status']) + ' authCode: ' + str(obj['authCode']))
      result = 'SUCCESS'
    elif resp.status_code >= 400 or resp.status_code < 500:
      errorObj = resp.json()['error']
      print(dtAsStr + ' ' + cardReq['merchantRefNum'] + ' --- FAILED (' + str(resp.status_code) + ') Error code: ' + errorObj['code'] + ' - ' + errorObj['message'])
      #print('Details: ' + str(errorObj['details']))
      result = 'FAILED'
    elif resp.status_code == 500:
      print(dtAsStr + ' ' + cardReq['merchantRefNum'] + ' --- OOPS, SERVER ERROR! ---')
      result = 'ERROR'

    return result