from mySQLAPI         import mySQLAPI
from openweatherAPI   import openweatherAPI
from wundergroundAPI  import wundergroundAPI
from config           import configUtils
import json

# TODO: cleanup and documentation

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
l_OWM_apiKey      = configUtils.ConfigSectionMap("openweathermap")['apikey']
l_OWM_provider    = configUtils.ConfigSectionMap("openweathermap")['provider']
l_OWM_townName    = configUtils.ConfigSectionMap("openweathermap")['townname']
l_OWM_countryKey  = configUtils.ConfigSectionMap("openweathermap")['countrykey']
l_OWM_header      = {}
l_OWM_header["CityName"] = l_OWM_townName
l_OWM_header["Provider"] = l_OWM_provider

# get wunderground settings
l_WG_apiKey      = configUtils.ConfigSectionMap("wunderground")['apikey']
l_WG_provider    = configUtils.ConfigSectionMap("wunderground")['provider']
l_WG_townName    = configUtils.ConfigSectionMap("wunderground")['townname']
l_WG_townKey     = configUtils.ConfigSectionMap("wunderground")['townkey']
l_WG_header      = {}
l_WG_header["CityName"] = l_WG_townName
l_WG_header["Provider"] = l_WG_provider

# set up sql table, this will delete existing tables
if create_SQL_table:
  mySQLAPI.createSQLTable(l_config,l_tablename)

# get data from openweatherAPI
l_OWM_Data = openweatherAPI.getData(l_OWM_apiKey,l_OWM_townName,l_OWM_countryKey)
# get data from wundergroundAPI
l_WG_Data  = wundergroundAPI.getData(l_WG_apiKey,l_WG_townKey)

# generating arrays which for data upload
l_headerArray = [l_OWM_header , l_WG_header]
l_fetchArray  = [l_OWM_Data , l_WG_Data]

# upload data to sql for defined data
for dataElement, headerElement in zip(l_fetchArray,l_headerArray):

  l_sqlData = [None] * len(dataElement.keys())

  # layout data for sql write, append header
  iterator=0
  for key, value in dataElement.iteritems():
    l_sqlData[iterator]={}
    l_sqlData[iterator]["CityName"]=headerElement['CityName']
    l_sqlData[iterator]["Date"]=key
    l_sqlData[iterator]["Provider"]=headerElement['Provider']
    l_sqlData[iterator]["JsonObj"]=json.dumps(value)
    iterator=iterator+1

  for element in l_sqlData:
  # check for create date or update
    if mySQLAPI.dateNotExists(l_config,l_tablename,element["Date"],element["Provider"]):
      mySQLAPI.createEntry(l_config,l_tablename,element)
    else:
      print "Data for %s of %s already present." % (element["Date"], element["Provider"])
