# Holds data for card response
class CardResponse:
  recordId = 0
  guid = ''
  decision = ''
  ref = ''
  txnId = ''  
  status = ''
  errorCode = ''
  message = ''
  modificationDate = ''

  # constructor
  def __init__(self, recordId, decision, guid):
    self.recordId = recordId
    self.decision = decision
    self.guid = guid

  def toString(self):
    if self.decision == 'SUCCESS':
      return self.guid + ' SUCCESS id: ' + self.txnId
    else:
      return self.guid + ' FAILED id: ' + self.txnId + ' Error code: ' + self.errorCode + ' - ' + self.message
