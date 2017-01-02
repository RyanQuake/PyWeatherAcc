from mySQLAPI import mySQLAPI
from openweatherAPI import openweatherAPI
from config import configUtils

# TODO: remove magic numbers

# control/debug variables
create_SQL_table=False # do create a sql table

# local variables
l_sqlData = [None] * 6

# get SQL settings
l_username  = configUtils.ConfigSectionMap("sql")['user']
l_password  = configUtils.ConfigSectionMap("sql")['password']
l_host      = configUtils.ConfigSectionMap("sql")['host']
l_database  = configUtils.ConfigSectionMap("sql")['database']
l_row       = configUtils.ConfigSectionMap("sql")['raise_on_warnings']

config      = {
              'user': l_username,
              'password': l_password,
              'host': l_host,
              'database': l_database,
              'raise_on_warnings': bool(l_row)
              }

# get openweathermap settings
l_apiKey      = configUtils.ConfigSectionMap("openweathermap")['apikey']
l_townKey     = configUtils.ConfigSectionMap("openweathermap")['townkey']
l_countryKey  = configUtils.ConfigSectionMap("openweathermap")['countrykey']
l_timeKey     = configUtils.ConfigSectionMap("openweathermap")['time']

# get data from openweatherAPI
l_dictOWMData = openweatherAPI.getData(l_apiKey,l_townKey,l_countryKey,l_timeKey)

# layout data for sql write
for i in range(0,6):
  l_sqlData[i]={}
  l_sqlData[i]["CityName"]=l_townKey
for i in range(0,6):
  l_sqlData[i]["Date"]=openweatherAPI.global_TT_STAMP[i]

for it in range(0,6):
  l_strIt="+"+str(it)
  for key, value in l_dictOWMData.iteritems():
    if l_strIt in key:
      l_sqlData[it][key]=value

# set up sql table, this will delete existing tables
if create_SQL_table:
  mySQLAPI.createSQLTable(config)

for element in l_sqlData:
# check for create date or update
  if mySQLAPI.dateExists(config,element["Date"]):
    # update
    for key,value in element.iteritems():
      mySQLAPI.updateByDate(config, element["Date"], key, value)
  else:
    # create entry
    mySQLAPI.createEntry(config, element)
