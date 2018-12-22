from dg.FileService import FileService

import unittest

class TestFileService(unittest.TestCase):

  service = FileService('xxx')

  def test_Simple(self):
    s = self.service.extractFileName('sample.csv')
    self.assertEqual(s, 'sample')

  def test_DoublePeriod(self):
    s = self.service.extractFileName('sample.blue.csv')
    self.assertEqual(s, 'sample.blue')

  def test_FileNoExtension(self):
    try:
      s = self.service.extractFileName('badfile')
    except Exception as ex:
      pass
    else:
      raise Exception('Was excepting it to raise Exception')
