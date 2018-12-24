from dg.CardRequest import CardRequest

import unittest

class TestCardRequest(unittest.TestCase):

  def test_ToString(self):
    req = CardRequest(0)
    req.ref = 'ref1'
    req.amount = '1500'
    req.firstName = 'Rick'
    req.lastName = 'Hunter'
    req.email = 'rick@sdf3.com'
    req.cardNbr = '4111222233334444'
    self.assertEqual(req.toString(), 'ref=ref1,amount=1500,firstName=Rick,lastName=Hunter,email=rick@sdf3.com,cardNbr=XXXX4444')