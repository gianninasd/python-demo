import json
import requests
from dg.CardRequest import CardRequest
from dg.CardResponse import CardResponse

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
      "profile": {
        "firstName": cardRequest.firstName,
        "lastName": cardRequest.lastName,
        "email": cardRequest.email,
      },
      "billingDetails": {
        "zip": cardRequest.zipCode
      }
    }

    # send the request
    resp = requests.post(url, headers=headers, auth=(self.apiUser, self.apiPass), data=json.dumps(cardReq))

    # process response
    if resp.status_code == 200:
      obj = resp.json()
      result = CardResponse('SUCCESS', cardRequest.ref)
      result.txnId = str(obj['id'])
      result.ref = str(obj['merchantRefNum'])
      result.status = str(obj['status'])
    elif resp.status_code >= 400 or resp.status_code < 500:
      result = CardResponse('FAILED', cardRequest.ref)
      result.txnId = str(resp.json()['id'])
      result.ref = str(resp.json()['merchantRefNum'])
      errorObj = resp.json()['error']
      result.errorCode = errorObj['code']
      result.message = errorObj['message']
    elif resp.status_code == 500:
      result = CardResponse('ERROR', cardRequest.ref)

    return result