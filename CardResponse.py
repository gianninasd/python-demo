# Holds data for card response
class CardResponse:
  ref = ''
  txnId = ''
  status = ''
  errorCode = ''
  message = ''

  # constructor
  def __init__(self, status, ref):
    self.status = status
    self.ref = ref

  def toString(self):
    if self.status == 'SUCCESS':
      return self.ref + ' SUCCESS id: ' + self.txnId
    else:
      return self.ref + ' FAILED Error code: ' + self.errorCode + ' - ' + self.message
