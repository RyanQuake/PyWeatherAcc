import mysql.connector
from mysql.connector import errorcode

# TODO: Table Layout has to be reworked
# TODO: remove hard coded db name

TABLE_LAYOUT = {}
TABLE_LAYOUT['weatherData'] = (
    "CREATE TABLE weatherData("
    "  CityName varchar(32) DEFAULT 0,"
    "  Date varchar(32) DEFAULT 0,"
    "  `Temp. +5 [C]` float(32) DEFAULT -255,"
    "  `Temp. +4 [C]` float(32) DEFAULT -255,"
    "  `Temp. +3 [C]` float(32) DEFAULT -255,"
    "  `Temp. +2 [C]` float(32) DEFAULT -255,"
    "  `Temp. +1 [C]` float(32) DEFAULT -255,"
    "  `Temp. +0 [C]` float(32) DEFAULT -255,"
    "  `Prec. +5 [mm]` float(32) DEFAULT -255,"
    "  `Prec. +4 [mm]` float(32) DEFAULT -255,"
    "  `Prec. +3 [mm]` float(32) DEFAULT -255,"
    "  `Prec. +2 [mm]` float(32) DEFAULT -255,"
    "  `Prec. +1 [mm]` float(32) DEFAULT -255,"
    "  `Prec. +0 [mm]` float(32) DEFAULT -255,"
    "  `Hum. +5 [%]` int(8) DEFAULT -255,"
    "  `Hum. +4 [%]` int(8) DEFAULT -255,"
    "  `Hum. +3 [%]` int(8) DEFAULT -255,"
    "  `Hum. +2 [%]` int(8) DEFAULT -255,"
    "  `Hum. +1 [%]` int(8) DEFAULT -255,"
    "  `Hum. +0 [%]` int(8) DEFAULT -255,"
    "  `Pres. +5 [hPa]` float(32) DEFAULT -255,"
    "  `Pres. +4 [hPa]` float(32) DEFAULT -255,"
    "  `Pres. +3 [hPa]` float(32) DEFAULT -255,"
    "  `Pres. +2 [hPa]` float(32) DEFAULT -255,"
    "  `Pres. +1 [hPa]` float(32) DEFAULT -255,"
    "  `Pres. +0 [hPa]` float(32) DEFAULT -255"
    ")")

def connectSQL(i_config):
    try:
        cnx = mysql.connector.connect(**i_config)
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("SQL Error: " + "Something is wrong with your user name or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("SQL Error: " + "Database does not exist.")
        else:
            print("SQL Error: " + err)
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
            print("SQL Error: " + err.msg)
        else:
            print("OK")
    disconnectSQL(cnx,cursor)

def updateByDate(i_config, i_date, i_strName, i_value):
    cnx, cursor = connectSQL(i_config)
    try:
        sql = "UPDATE weatherData"+" SET "+i_strName+"= '"+str(i_value)+"' WHERE Date = "+"'"+i_date+"'"
        # print sql
        cursor.execute(sql)
        cnx.commit()
    except mysql.connector.Error as err:
        print("SQL Error: " + err.msg)
        cnx.rollback()
    disconnectSQL(cnx,cursor)

def createEntry(i_config, i_dictData):
    cnx, cursor = connectSQL(i_config)
    try:
        sql_base    = "INSERT INTO"
        sql_keys    = " weatherData ("
        sql_values  = " VALUES ("
        f_cur=1
        f_end=len(i_dictData)

        for key, value in i_dictData.iteritems() :
            sql_keys = sql_keys+key
            sql_values = sql_values+"'"+str(value)+"'"
            if f_cur < f_end:
                sql_keys=sql_keys+", "
                sql_values=sql_values+", "
            else:
                sql_keys=sql_keys+")"
                sql_values=sql_values+")"
            f_cur=f_cur+1

        cursor.execute(sql_base+sql_keys+sql_values)
        cnx.commit()
    except mysql.connector.Error as err:
        print("SQL Error: " + err.msg)
        cnx.rollback()

    disconnectSQL(cnx,cursor)

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
