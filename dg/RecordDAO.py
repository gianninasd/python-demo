from mysql.connector.pooling import MySQLConnectionPool

import datetime

# DAO to interac with file records
class RecordDAO:

  # sql statement constants
  CREATE = 'insert into file_records (guid,status_cde,request_body,created_date,modification_date) ' \
    + 'values (%(guid)s,%(status)s,%(request)s,%(createdDate)s,%(modificationDate)s)'
  UPDATE = 'update file_records set status_cde = %(status)s, response_body = %(response)s, modification_date = now() ' \
    + 'where guid = %(guid)s'

  dbPool = None

  # return an available database connection from the pool
  def getConn(self):
    if self.dbPool is None:
      dbConfig = {
        'host': 'localhost',
        'port': '3306',
        'user': 'root',
        'password': 'root',
        'database': 'fileproc'
      }
      
      dbPool = MySQLConnectionPool(pool_name = "mypool", pool_size = 10, **dbConfig)

    return dbPool.get_connection()

  # create a new record entry
  def create(self, rec):
    currTime = datetime.datetime.now()
    data = {
      'guid': rec.guid,
      'status': 'SENT',
      'request': rec.toString(),
      'createdDate': currTime.strftime("%Y-%m-%d %H:%M:%S"),
      'modificationDate': currTime.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
      cn = self.getConn()
      cursor = cn.cursor()
      cursor.execute(self.CREATE, data)
      cn.commit()
    finally:
      cn.close()

  # update an existing record
  def update(self, rec):
    currTime = datetime.datetime.now()
    data = {
      'guid': rec.guid,
      'status': rec.decision,
      'response': rec.toString()
    }
    
    try:
      cn = self.getConn()
      cursor = cn.cursor()
      cursor.execute(self.UPDATE, data)
      cn.commit()
    finally:
      cn.close()