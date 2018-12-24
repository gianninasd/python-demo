from dg.LineParser import LineParser
from dg.LineParser import MissingTokensException

import unittest

class TestLineParser(unittest.TestCase):

  parser = LineParser()

  def test_GoodLine(self):
    try:
      self.parser.parse(0,'jim7025,1500,4111111111111111,10,2020,Rick,Hunter,rick@sdf3.com,M5H 2N2')
    except Exception as ex:
      raise Exception('Was not excepting it to raise an Exception')
    else:
      pass

  def test_missingTokens(self):
    try:
      self.parser.parse(0,'jim7025,1500,4111111111111111')
    except MissingTokensException as ex:
      pass
    else:
      raise Exception('Was excepting it to raise MissingTokensException')

  def test_missingRef(self):
    try:
      self.parser.parse(0,',1500,4111111111111111,10,2020,Rick,Hunter,rick@sdf3.com,M5H 2N2')
    except ValueError as ex:
      pass
    else:
      raise Exception('Was excepting it to raise ValueError')

  def test_badAmount(self):
    try:
      self.parser.parse(0,'jim22,xx,4111111111111111,10,2020,Rick,Hunter,rick@sdf3.com,M5H 2N2')
    except ValueError as ex:
      pass
    else:
      raise Exception('Was excepting it to raise ValueError')

  def test_badCardNbr(self):
    try:
      self.parser.parse(0,'jim22,1500,xxxxxx,10,2020,Rick,Hunter,rick@sdf3.com,M5H 2N2')
    except ValueError as ex:
      pass
    else:
      raise Exception('Was excepting it to raise ValueError')

  def test_badCardExpMth(self):
    try:
      self.parser.parse(0,'jim22,1500,4111111111111111,15,2020,Rick,Hunter,rick@sdf3.com,M5H 2N2')
    except ValueError as ex:
      pass
    else:
      raise Exception('Was excepting it to raise ValueError')

  def test_badCardExpYear(self):
    try:
      self.parser.parse(0,'jim22,1500,4111111111111111,10,1995,Rick,Hunter,rick@sdf3.com,M5H 2N2')
    except ValueError as ex:
      pass
    else:
      raise Exception('Was excepting it to raise ValueError')

  def test_badFirstName(self):
    try:
      self.parser.parse(0,'jim22,1500,4111111111111111,10,2020,,Hunter,rick@sdf3.com,M5H 2N2')
    except ValueError as ex:
      pass
    else:
      raise Exception('Was excepting it to raise ValueError')

  def test_badLastName(self):
    try:
      self.parser.parse(0,'jim22,1500,4111111111111111,10,2020,Rick,,rick@sdf3.com,M5H 2N2')
    except ValueError as ex:
      pass
    else:
      raise Exception('Was excepting it to raise ValueError')

  def test_badEmail(self):
    try:
      self.parser.parse(0,'jim22,1500,4111111111111111,10,2020,Rick,Hunter,,M5H 2N2')
    except ValueError as ex:
      pass
    else:
      raise Exception('Was excepting it to raise ValueError')

  def test_badZipCode(self):
    try:
      self.parser.parse(0,'jim22,1500,4111111111111111,10,2020,Rick,Hunter,rick@sdf3.com,')
    except ValueError as ex:
      pass
    else:
      raise Exception('Was excepting it to raise ValueError')