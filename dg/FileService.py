from dg.FileDAO import FileDAO
from dg.RecordDAO import RecordDAO
from cryptography.fernet import Fernet

import hashlib

# Exception thrown when the file was previously uploaded in the last 24 hrs
class DupeFileException(Exception):
  pass

# Exception thrown when the secret key is not an environment variable
class SecretKeyNotFoundException(Exception):
  pass

# Service class for all file operations
class FileService:
  secretKey = b''

  fileDAO = FileDAO()
  recordDAO = RecordDAO()

  # constructor
  def __init__(self, secretKey):
    self.secretKey = secretKey

  # extracts only the filename without the extension
  def extractFileName(self, fullFileName):
    idx = fullFileName.index('.csv')
    return fullFileName[:idx]

  # generates an ack file in the folder specified
  def createAck(self, path, fileName, responseCode, responseMessage):
    with open(path + '/' + fileName + '.ack.csv', 'w') as ackFile:
      ackFile.write('ACK,' + responseCode + ',' + responseMessage)

  # creates a file record in the DB
  # raises DupeFileException if file was previously uploaded in the last 24 hrs
  def create(self, workingDir, fileName):
    fileHash = self._calculateHash(workingDir, fileName)
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
  def _calculateHash(self, workingDir, fileName):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(workingDir + '/' + fileName, 'rb') as afile:
      buf = afile.read(BLOCKSIZE)
      while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)

    return hasher.hexdigest()