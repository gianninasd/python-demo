from dg.CardResponse import CardResponse

import unittest

class TestCardResponse(unittest.TestCase):

  def test_ToString_Success(self):
    res = CardResponse(0,'SUCCESS','guid1234')
    res.txnId = '0011'
    self.assertEqual(res.toString(), 'guid1234 SUCCESS id: 0011')
  
  def test_ToString_Failed(self):
    res = CardResponse(0,'FAILED','guid1234')
    res.txnId = '0011'
    res.errorCode = '1007'
    res.message = 'insufficient funds'
    self.assertEqual(res.toString(), 'guid1234 FAILED id: 0011 Error code: 1007 - insufficient funds')