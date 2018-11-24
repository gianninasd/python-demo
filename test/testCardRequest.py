from dg.CardRequest import CardRequest

import unittest

class TestCardRequest(unittest.TestCase):

  def test_parse(self):
    req = CardRequest()
    req.parse('ref1,15.00,4111222233334444,10,2020,90210')
    self.assertEqual(req.ref, 'ref1')
    self.assertEqual(req.amount, '15.00')
    self.assertEqual(req.cardNbr, '4111222233334444')
    self.assertEqual(req.cardExpMth, '10')
    self.assertEqual(req.cardExpYear, '2020')
    self.assertEqual(req.zipCode, '90210')