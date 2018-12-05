from dg.AbstractDAO import AbstractDAO
from mysql.connector.pooling import MySQLConnectionPool

# DAO to interac with file records
class RecordDAO(AbstractDAO):

  # sql statement constants
  CREATE = 'insert into file_records (guid,status_cde,request_body,created_date,modification_date) ' \
    + 'values (%(guid)s,%(status)s,%(request)s,now(),now())'
  UPDATE = 'update file_records set status_cde = %(status)s, response_body = %(response)s, ' \
    + 'modification_date = now() where guid = %(guid)s'

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