from dg.FileDAO import FileDAO
from dg.RecordDAO import RecordDAO
from cryptography.fernet import Fernet

import hashlib

# Exception thrown when the file was previously uploaded in the last 24 hrs
class DupeFileException(Exception):
  pass

# Service class for all file operations
class FileService:
  secretKey = b''

  fileDAO = FileDAO()
  recordDAO = RecordDAO()

  # constructor
  def __init__(self, secretKey):
    self.secretKey = secretKey

  # creates a file record in the DB
  # raises DupeFileException if file was previously uploaded in the last 24 hrs
  def create(self, fileName):
    fileHash = self.__calculateHash(fileName)
    cnt = self.fileDAO.countInLast24hrs(fileHash)

    fileId = self.fileDAO.create(fileName, fileHash)

    if cnt > 0:
      raise DupeFileException()

    return fileId

  # store the raw record in encrypted format
  def storeRecord(self, fileId, record):
    fernet = Fernet(self.secretKey)
    recordAsBytes = bytes(record,'utf-8')
    token = fernet.encrypt(recordAsBytes)
    
    self.recordDAO.createInitial(fileId, token)

  # generates the hash value of the file contents
  def __calculateHash(self, fileName):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(fileName, 'rb') as afile:
      buf = afile.read(BLOCKSIZE)
      while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)

    return hasher.hexdigest()