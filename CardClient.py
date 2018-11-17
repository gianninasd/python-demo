import json
import uuid
import requests

# @author Dimitrios Gianninas
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
  def purchase(self, accountId):
    url = self.cardUrl + accountId + '/auths'
    headers = {'content-type': 'application/json'}

    cardReq = {
      "merchantRefNum": uuid.uuid1().hex,
      "amount": 1500,
      "settleWithAuth": True,
      "card": {
        "cardNum": "4111111111111111",
        "cardExpiry": {
          "month": "10",
          "year": "2020"
        }
      },
      "billingDetails": {
        "zip": "H8P1K1"
      }
    }

    # send the request
    #print('Sending: ' + json.dumps(cardReq))
    print('Sending reference ' + cardReq['merchantRefNum'] + ' with amount ' + str(cardReq['amount']))
    resp = requests.post(url, headers=headers, auth=(self.apiUser, self.apiPass), data=json.dumps(cardReq))

    # process response
    print('Status: ' + str(resp.status_code) )

    if resp.status_code == 200:
      #print('response body: ' + str(resp.json()) )
      print('--- SUCCESSFUL ---')
      print('id: ' + str(resp.json()['id']) )
      print('status: ' + str(resp.json()['status']) )
      print('authCode: ' + str(resp.json()['authCode']) )
      print('avsResponse: ' + str(resp.json()['avsResponse']) )
      print('cvvVerification: ' + str(resp.json()['cvvVerification']) )
    elif resp.status_code == 400:
      errorObj = resp.json()['error']
      print('--- BAD REQUEST ---')
      print('Failed with error code: ' + errorObj['code'] + ' with message: ' + errorObj['message'])
      print('Details: ' + str(errorObj['details']))
    elif resp.status_code == 500:
      print('--- OOPS, SERVER ERROR! ---')