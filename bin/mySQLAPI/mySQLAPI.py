import mysql.connector
from mysql.connector import errorcode

TABLE_LAYOUT = {}
TABLE_LAYOUT['weatherData'] = (
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
    "  `Prec. +0 [mm]` int(32) DEFAULT -255,"
    "  `Hum. +5 [%]` int(32) DEFAULT -255,"
    "  `Hum. +4 [%]` int(32) DEFAULT -255,"
    "  `Hum. +3 [%]` int(32) DEFAULT -255,"
    "  `Hum. +2 [%]` int(32) DEFAULT -255,"
    "  `Hum. +1 [%]` int(32) DEFAULT -255,"
    "  `Hum. +0 [%]` int(32) DEFAULT -255,"
    "  `Pres. +5 [hPa]` int(32) DEFAULT -255,"
    "  `Pres. +4 [hPa]` int(32) DEFAULT -255,"
    "  `Pres. +3 [hPa]` int(32) DEFAULT -255,"
    "  `Pres. +2 [hPa]` int(32) DEFAULT -255,"
    "  `Pres. +1 [hPa]` int(32) DEFAULT -255,"
    "  `Pres. +0 [hPa]` int(32) DEFAULT -255"
    ")")

def connectSQL(i_config):
    try:
        cnx = mysql.connector.connect(**i_config)
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)
    return cnx, cursor

def disconnectSQL(i_cnx, i_cursor):
    i_cursor.close()
    i_cnx.close()

def createSQLTable(i_config):
    cnx, cursor = connectSQL(i_config)

    for name, ddl in TABLE_LAYOUT.iteritems():
        try:
            print("Deleting table "+name+" on "+i_config['database'])
            cursor.execute("DROP TABLE IF EXISTS {}".format(name))
        except:
            pass
        print("OK")
        try:
            print("Creating table "+name+" on "+i_config['database'])
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    disconnectSQL(cnx,cursor)

def updateByDate(i_date,i_strName, i_value):
    pass

def createEntry(i_arrData):
    pass

def dateExists(i_config, i_date):
    cnx, cursor = connectSQL(i_config)
    l_retval=False

    cursor.execute("SELECT * FROM weatherData")

    row = cursor.fetchone()

    while row is not None:
        if i_date in row:
            l_retval=True
        row = cursor.fetchone()

    disconnectSQL(cnx,cursor)
    return l_retval
