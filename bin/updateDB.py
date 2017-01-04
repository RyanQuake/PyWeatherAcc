from mySQLAPI import mySQLAPI
from openweatherAPI import openweatherAPI
from config import configUtils
import json

# control/debug variables
create_SQL_table=False # do create a sql table

# get SQL settings
l_username  = configUtils.ConfigSectionMap("sql")['user']
l_password  = configUtils.ConfigSectionMap("sql")['password']
l_host      = configUtils.ConfigSectionMap("sql")['host']
l_database  = configUtils.ConfigSectionMap("sql")['database']
l_row       = configUtils.ConfigSectionMap("sql")['raise_on_warnings']
l_tablename = configUtils.ConfigSectionMap("sql")['tablename']

l_config      = {
              'user': l_username,
              'password': l_password,
              'host': l_host,
              'database': l_database,
              'raise_on_warnings': bool(l_row),
              }

# get openweathermap settings
l_apiKey      = configUtils.ConfigSectionMap("openweathermap")['apikey']
l_provider    = configUtils.ConfigSectionMap("openweathermap")['provider']
l_townKey     = configUtils.ConfigSectionMap("openweathermap")['townkey']
l_countryKey  = configUtils.ConfigSectionMap("openweathermap")['countrykey']

# get data from openweatherAPI
l_dictOWMData = openweatherAPI.getData(l_apiKey,l_townKey,l_countryKey)

l_sqlData = [None] * len(l_dictOWMData.keys())

# layout data for sql write
iterator=0
for key, value in l_dictOWMData.iteritems():
  l_sqlData[iterator]={}
  l_sqlData[iterator]["CityName"]=l_townKey
  l_sqlData[iterator]["Date"]=key
  l_sqlData[iterator]["Provider"]=l_provider
  l_sqlData[iterator]["JsonObj"]=json.dumps(value)
  iterator=iterator+1

# set up sql table, this will delete existing tables
if create_SQL_table:
  mySQLAPI.createSQLTable(l_config,l_tablename)

for element in l_sqlData:
# check for create date or update
  if mySQLAPI.dateNotExists(l_config,l_tablename,element["Date"]):
    # pass
    mySQLAPI.createEntry(l_config,l_tablename,element)
  else:
    print "Data for date already present."
