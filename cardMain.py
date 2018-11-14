import requests
import json
import uuid

# config
accountId = '1001289630'
cardUrl = 'https://api.test.paysafe.com/cardpayments/v1/accounts/' + accountId + '/auths'

apiUser = 'test_assl1'
apiPass = 'B-qa2-0-5be8832c-0-302c02146cd8d52ddcca8ee8ce57845505ce80cfcab23c6202140fb0300b0bf9a8cc63fc0b7d58e2c0c1b6724130'
headers = {'content-type': 'application/json'}

cardReq = {
  "merchantRefNum": uuid.uuid1().hex,
  "amount": 100,
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
print('Sending: ' + json.dumps(cardReq))
resp = requests.post(cardUrl, headers=headers, auth=(apiUser, apiPass), data=json.dumps(cardReq)) 

# process response
print('Status: ' + str(resp.status_code) )

if resp.status_code == 200:
  print('response body: ' + str(resp.json()) )