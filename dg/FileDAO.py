from dg.AbstractDAO import AbstractDAO

# DAO to interac with files
class FileDAO(AbstractDAO):

  # sql statement constants
  CREATE = 'insert into file_uploads (filename,filehash,creation_date,modification_date) ' \
    + 'values (%(filename)s,%(filehash)s,now(),now())'
  FIND_LAST24HRS = 'select count(1) from fileproc.file_uploads where filehash = %(filehash)s ' \
    + 'and creation_date >= NOW() - INTERVAL 1 DAY'

  # create a new file record entry, returning the file ID
  def create(self, fileName, fileHash):
    data = {
      'filename': fileName,
      'filehash': fileHash
    }

    return self.execute(self.CREATE, data)

  # returns the number of times the filehash occurs in the last 24 hrs
  def countInLast24hrs(self, fileHash):
    data = {
      'filehash': fileHash
    }

    cnt = 0
    cn = self.getConn()
    
    try:
      cursor = cn.cursor()
      cursor.execute(self.FIND_LAST24HRS, data)
      rez = cursor.fetchone()
      cnt = rez[0] # get the first value in the tuple
    finally:
      cursor.close()
      cn.close() # returns connection to the pool

    return cnt