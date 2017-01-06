import mysql.connector
from mysql.connector import errorcode

# TODO: document api
# TODO: extend api for data analysis

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

def createSQLTable(i_config,i_tablename):
    cnx, cursor = connectSQL(i_config)

    TABLE_LAYOUT = {}
    TABLE_LAYOUT[i_tablename] = (
        "CREATE TABLE %s("
        "  CityName varchar(32) DEFAULT 0,"
        "  Date varchar(32) DEFAULT 0,"
        "  Provider TEXT,"
        "  JsonObj TEXT"
        ")" % i_tablename)

    for name, ddl in TABLE_LAYOUT.iteritems():
        try:
            print("Deleting table "+name+" on "+i_config['database'])
            cursor.execute("DROP TABLE IF EXISTS %s" % name)
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

def createEntry(i_config, i_tablename, i_dictData):
    cnx, cursor = connectSQL(i_config)
    try:
        sql_base    = "INSERT INTO"
        sql_keys    = " %s (" % i_tablename
        sql_values  = " VALUES ("
        f_cur=1
        f_end=len(i_dictData)

        for key, value in i_dictData.iteritems() :
            sql_keys = sql_keys+key
            sql_values = sql_values+"'%s'" % str(value)
            if f_cur < f_end:
                sql_keys=sql_keys+", "
                sql_values=sql_values+", "
            else:
                sql_keys=sql_keys+")"
                sql_values=sql_values+")"
            f_cur=f_cur+1

        cursor.execute(sql_base+sql_keys+sql_values)
        cnx.commit()
        print "Created weatherData entry for "+i_dictData['Date']+" of "+i_dictData['Provider']
    except mysql.connector.Error as err:
        print("SQL Error: " + err.msg)
        cnx.rollback()

    disconnectSQL(cnx,cursor)

def dateNotExists(i_config, i_tablename, i_date, i_provider):
    cnx, cursor = connectSQL(i_config)
    l_retVal=True

    cursor.execute("SELECT Date,Provider,CityName FROM %s" % i_tablename)

    row = cursor.fetchone()

    while row is not None:
        if i_date in row and i_provider in row:
                l_retVal=False
        row = cursor.fetchone()

    disconnectSQL(cnx,cursor)
    return l_retVal

def queryByDate(i_config,i_tablename,i_date,i_weatherservice):
    l_retVal=[]
    cnx, cursor = connectSQL(i_config)

    l_sqlCommand = "SELECT * FROM {} WHERE (Date LIKE \"%{}%\" AND Provider LIKE \"%{}%\")".format(i_tablename,i_date,i_weatherservice)
    cursor.execute(l_sqlCommand)

    row = cursor.fetchone()
    while row is not None:
        l_retVal.append(row)
        row = cursor.fetchone()

    disconnectSQL(cnx,cursor)
    return l_retVal
