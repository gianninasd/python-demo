from mysql.connector.pooling import MySQLConnectionPool

# base class for all DAO with re-usable methods
class AbstractDAO:

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

  # either executes an INSERT or UPDATE database operation 
  # using the SQL statement and data provided
  def execute(self, sqlStmt, data):
    try:
      cn = self.getConn()
      cursor = cn.cursor()
      cursor.execute(sqlStmt, data)
      cn.commit()
    finally:
      cn.close()