import requests

# config
accountId = '1001289630'
cardUrl = 'https://api.test.paysafe.com/cardpayments/v1/accounts/' + accountId + '/auths'

apiUser = 'test_assl1'
apiPass = 'B-qa2-0-5be8832c-0-302c02146cd8d52ddcca8ee8ce57845505ce80cfcab23c6202140fb0300b0bf9a8cc63fc0b7d58e2c0c1b6724130'
apiKey = 'dGVzdF9hc3NsMTpCLXFhMi0wLTViZTg4MzJjLTAtMzAyYzAyMTQ2Y2Q4ZDUyZGRjY2E4ZWU4Y2U1Nzg0NTUwNWNlODBjZmNhYjIzYzYyMDIxNDBmYjAzMDBiMGJmOWE4Y2M2M2ZjMGI3ZDU4ZTJjMGMxYjY3MjQxMzA='
headers = {'content-type': 'application/json'}

# send the request
resp = requests.post(cardUrl, headers=headers, auth=(apiUser, apiPass), data={}) 
# auth=(apiUser, apiPass)
#.get('https://google.ca')

# process response
print('status: ' + str(resp.status_code) )

if resp.status_code == 200:
  print('response body: ' + resp.json() )