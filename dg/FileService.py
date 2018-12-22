from dg.FileDAO import FileDAO

import hashlib

# Exception thrown when the file was previously uploaded in the last 24 hrs
class DupeFileException(Exception):
  pass

# Service class for all file operations
class FileService:

  fileDAO = FileDAO()

  # creates a file record in the DB
  # raises DupeFileException if file was previously uploaded in the last 24 hrs
  def create(self, fileName):
    fileHash = self.__calculateHash(fileName)
    cnt = self.fileDAO.countInLast24hrs(fileHash)

    self.fileDAO.create(fileName, fileHash)

    if cnt > 0:
      raise DupeFileException()

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