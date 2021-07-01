import os
import datetime
import logging

import azure.functions as func
import pyodbc

driver = '{ODBC Driver 17 for SQL Server}'
server = os.environ['AZURE_SQL_SERVER_URI']
database = os.environ['AZURE_DB_NAME']
username = os.environ['AZURE_DB_USERNAME']
password = os.environ['AZURE_DB_PASSWORD']

connection_str = 'DRIVER=%s;SERVER=%s;PORT=1433;DATABASE=%s;UID=%s;PWD=%s' % (
	driver,
	server,
	database,
	username,
	password
)


def main(mytimer: func.TimerRequest) -> None:
  print(connection_str)

  conn = pyodbc.connect(connection_str)
  cur = conn.cursor()
  # url = 'https://eytpihuslnyiiffw.blob.core.windows.net/sqlbackup_%s.bacpac'
  url = './%s.bacpac' % datetime.datetime.now().strftime("%m%d%Y%H%M%S")
  # url = url % datetime.datetime.now().strftime("%m%d%Y%H%M%S")
  backup_sql = "BACKUP DATABASE [%s] TO DISK = N'%s'"
  backup_sql = backup_sql % (database, url)
  cur = cur.execute(backup_sql)
  # row = cur.fetchone()

  while cur.nextset():
    pass

  # while row:
  #     print(str(row[0]) + " " + str(row[1]))
  #     row = cur.fetchone()

  utc_timestamp = datetime.datetime.utcnow().replace(
      tzinfo=datetime.timezone.utc).isoformat()

  if mytimer.past_due:
        logging.info('The timer is past due!')

  logging.info('Python timer trigger function ran at %s', utc_timestamp)
