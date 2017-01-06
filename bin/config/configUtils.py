import ConfigParser
import os

# TODO: cleanup and documentation

Config  = ConfigParser.ConfigParser()
pathfile= os.path.join("config","config.ini")
Config.read(pathfile)

class validationError(Exception):
    pass

def validateConfigFile():
    # check if config file is present
    if 0 >= len(Config.sections()):
        raise validationError("Error: Config file is missing or empty.")

    # verify sql data
    if "sql" not in Config.sections():
        raise validationError("Error: SQL config is missing.")
    try:
        Config.get("sql","user")
        Config.get("sql","password")
        Config.get("sql","host")
        Config.get("sql","database")
        Config.get("sql","tablename")
    except:
        raise validationError("Error: SQL settings are incorrect. See example file.")

    # verify weather services
    if 1 >= len(Config.sections()):
        raise validationError("Error: Config file is corrupt. See example file.")
    for item in Config.sections():
        if "sql" not in item:
            try:
                Config.get(item,"apikey")
                Config.get(item,"provider")
                Config.get(item,"townname")
                Config.get(item,"townkey")
            except:
                raise validationError("Error: WeatherService config is incorrect. See example file.")

def configSectionMap(section):
    dict1 = {}
    try:
        options = Config.options(section)
    except:
        print "Error: Config file not according exsample."
        print "Please read README for further details."
        exit(1)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def getWeatherServices():
    buffer_dict={}
    retVal_dict={}

    for item in Config.sections():
        if "sql" not in item:
            buffer_dict[item]=Config.options(item)

    for weatherService, options in buffer_dict.iteritems():
        retVal_dict[weatherService]={}
        for option in options:
            retVal_dict[weatherService][option]=Config.get(weatherService, option)

    return retVal_dict

def getSQLData():
    retVal_dict={}
    retVal_tableName=""

    # get SQL settings
    l_username  = configSectionMap("sql")['user']
    l_password  = configSectionMap("sql")['password']
    l_host      = configSectionMap("sql")['host']
    l_database  = configSectionMap("sql")['database']
    l_row       = configSectionMap("sql")['raise_on_warnings']
    l_tablename = configSectionMap("sql")['tablename']

    retVal_dict = {
                  'user': l_username,
                  'password': l_password,
                  'host': l_host,
                  'database': l_database,
                  'raise_on_warnings': bool(l_row),
                  }
    retVal_tableName = l_tablename

    return retVal_dict, retVal_tableName
