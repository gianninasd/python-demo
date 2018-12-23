from dg.AbstractDAO import AbstractDAO
from dg.CardResponse import CardResponse
from mysql.connector.pooling import MySQLConnectionPool

# Holds data for a raw record
class Record:
  recordId = 0
  rawData = ''

# DAO to interac with file records
class RecordDAO(AbstractDAO):

  # sql statement constants
  CREATE = 'insert into file_records (file_id,status_cde,raw_record,creation_date,modification_date) ' \
    + 'values (%(fileId)s,%(status)s,%(rawRecord)s,now(),now())'
  UPDATE_SENT = 'update file_records set status_cde = %(status)s, modification_date = now(), ' \
    + 'guid = %(guid)s, request_body = %(request)s where record_id = %(recordId)s'
  UPDATE_RESPONSE = 'update file_records set status_cde = %(status)s, response_body = %(response)s, ' \
    + 'modification_date = now() where record_id = %(recordId)s'
  LOAD_ALL = 'select record_id, guid, status_cde, modification_date from file_records ' \
    + 'where creation_date >= now() - interval 1 day order by modification_date asc'
  LOAD_ALL_INITIAL = 'select record_id, creation_date, raw_record from fileproc.file_records ' \
    + 'where status_cde = "INITIAL" order by creation_date asc limit 10'

  # create a new record entry
  def createInitial(self, fileId, record):
    data = {
      'fileId': fileId,
      'status': 'INITIAL',
      'rawRecord': record
    }

    self.execute(self.CREATE, data)

  # update an existing record status
  def updateSent(self, rec):
    data = {
      'recordId': rec.recordId,
      'status': 'SENT',
      'guid': rec.guid,
      'request': rec.toString()
    }

    self.execute(self.UPDATE_SENT, data)

  # update an existing record
  def updateResponse(self, rec):
    data = {
      'recordId': rec.recordId,
      'status': rec.decision,
      'response': rec.toString()
    }

    self.execute(self.UPDATE_RESPONSE, data)

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

  # returns all the records in an initial status
  def getAllWithStatusInitial(self):
    try:
      cn = self.getConn()
      cursor = cn.cursor()
      cursor.execute(self.LOAD_ALL_INITIAL)

      rows = cursor.fetchall()
      recs = []

      for rec in rows:
        rawRec = Record()
        rawRec.recordId = rec[0]
        rawRec.rawData = rec[2]
        recs.append(rawRec)

      return recs
    finally:
      cn.close()