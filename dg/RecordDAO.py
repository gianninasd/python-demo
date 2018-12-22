from dg.AbstractDAO import AbstractDAO
from dg.CardResponse import CardResponse
from mysql.connector.pooling import MySQLConnectionPool

# DAO to interac with file records
class RecordDAO(AbstractDAO):

  # sql statement constants
  CREATE = 'insert into file_records (guid,status_cde,request_body,creation_date,modification_date) ' \
    + 'values (%(guid)s,%(status)s,%(request)s,now(),now())'
  CREATE2 = 'insert into file_records (file_id,status_cde,raw_record,creation_date,modification_date) ' \
    + 'values (%(fileId)s,%(status)s,%(rawRecord)s,now(),now())'
  UPDATE = 'update file_records set status_cde = %(status)s, response_body = %(response)s, ' \
    + 'modification_date = now() where guid = %(guid)s'
  LOAD_ALL = 'select record_id, guid, status_cde, modification_date from file_records ' \
    + 'where creation_date >= now() - interval 1 day order by modification_date asc'

  # create a new record entry
  def createInitial(self, fileId, record):
    data = {
      'fileId': fileId,
      'status': 'INITIAL',
      'rawRecord': record
    }

    self.execute(self.CREATE2, data)

  # create a new record entry
  def create(self, rec):
    data = {
      'guid': rec.guid,
      'status': 'SENT',
      'request': rec.toString()
    }

    self.execute(self.CREATE, data)

  # update an existing record
  def update(self, rec):
    data = {
      'guid': rec.guid,
      'status': rec.decision,
      'response': rec.toString()
    }

    self.execute(self.UPDATE, data)

  # returns all the records created in the last day
  def getAll(self):
    try:
      cn = self.getConn()
      cursor = cn.cursor()
      cursor.execute(self.LOAD_ALL)

      rows = cursor.fetchall()
      recs = []

      for rec in rows:
        fileRec = CardResponse('','')
        fileRec.guid = rec[1]
        fileRec.status = rec[2]
        fileRec.modificationDate = rec[3]
        recs.append(fileRec)

      return recs
    finally:
      cn.close()