from dg.AbstractDAO import AbstractDAO

# DAO to interac with files
class FileDAO(AbstractDAO):

  # sql statement constants
  CREATE = 'insert into file_uploads (filename,filehash,creation_date,modification_date) ' \
    + 'values (%(filename)s,%(filehash)s,now(),now())'

  # create a new record entry
  def create(self, fileName, fileHash):
    data = {
      'filename': fileName,
      'filehash': fileHash
    }

    self.execute(self.CREATE, data)