import mysql.connector
from mysql.connector import errorcode
import time

config = {
  'user': 'winter',
  'password': 'winterRules',
  'host': '127.0.0.1',
  'database': 'testing',
  'raise_on_warnings': True,
}

TABLES = {}
TABLES['weatherData'] = (
    "CREATE TABLE weatherData("
    "  CityName varchar(32) DEFAULT 0,"
    "  Date date DEFAULT 0,"
    "  `Temp. +5 [C]` int(16) DEFAULT -255,"
    "  `Temp. +4 [C]` int(16) DEFAULT -255,"
    "  `Temp. +3 [C]` int(16) DEFAULT -255,"
    "  `Temp. +2 [C]` int(16) DEFAULT -255,"
    "  `Temp. +1 [C]` int(16) DEFAULT -255,"
    "  `Temp. +0 [C]` int(16) DEFAULT -255,"
    "  `Prec. +5 [mm]` int(32) DEFAULT -255,"
    "  `Prec. +4 [mm]` int(32) DEFAULT -255,"
    "  `Prec. +3 [mm]` int(32) DEFAULT -255,"
    "  `Prec. +2 [mm]` int(32) DEFAULT -255,"
    "  `Prec. +1 [mm]` int(32) DEFAULT -255,"
    "  `Prec. +0 [mm]` int(32) DEFAULT -255"
    ")")

try:
  cnx = mysql.connector.connect(**config)
  cursor = cnx.cursor()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

for name, ddl in TABLES.iteritems():
    try:
        cursor.execute("DROP TABLE IF EXISTS {}".format(name))
    except:
        pass

    try:
        print("Creating table {}: ".format(name))
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
try:
    sql = "INSERT INTO weatherData(CityName, \
       Date, `Temp. +5 [C]` ) \
       VALUES ('%s', '%s', '%d')" % \
       ('Munich', time.strftime("%Y%m%d"), 10)
    cursor.execute(sql)
    cnx.commit()
except mysql.connector.Error as err:
    print(err.msg)
    cnx.rollback()

try:
    sql = "INSERT INTO weatherData(\
        `Temp. +5 [C]`, Date, `Temp. +4 [C]` ) \
       VALUES ('%d', '%s', '%d')" % \
       (1 ,time.strftime("%Y%m%d"), 10)
    cursor.execute(sql)
    cnx.commit()
except mysql.connector.Error as err:
    print(err.msg)
    cnx.rollback()

cursor.close()
cnx.close()
