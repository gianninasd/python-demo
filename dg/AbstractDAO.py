from dbConfig import dbConfig
from mysql.connector.pooling import MySQLConnectionPool

# base class for all DAO with re-usable methods
class AbstractDAO:

  dbPool = None

  # return an available database connection from the pool
  def getConn(self):
    if self.dbPool is None:
      self.dbPool = MySQLConnectionPool(pool_name = "mypool", pool_size = 10, **dbConfig)

    return self.dbPool.get_connection()

  # either executes an INSERT or UPDATE database operation 
  # using the SQL statement and data provided
  def execute(self, sqlStmt, data):
    id = 0
    try:
      cn = self.getConn()
      cursor = cn.cursor()
      cursor.execute(sqlStmt, data)
      cn.commit()
      id = cursor.lastrowid
    finally:
      cn.close() # returns connection to the pool

    return id