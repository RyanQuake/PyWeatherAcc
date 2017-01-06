from mySQLAPI         import mySQLAPI
from openweatherAPI   import openweatherAPI
from wundergroundAPI  import wundergroundAPI
from config           import configUtils
from pprint           import pprint
import json

# TODO: cleanup and documentation

# control/debug variables
create_SQL_table=False # do create a sql table

# Verify config file
try:
  configUtils.validateConfigFile()
except configUtils.validationError as exception:
  print exception.message
  exit(1)

# get SQL settings
l_config, l_tablename = configUtils.getSQLData()

# get weatherServices
l_weatherServices = configUtils.getWeatherServices()

# init arrays for data
l_headerArray = [None] * len(l_weatherServices.keys())
l_fetchArray  = [None] * len(l_weatherServices.keys())

# fetch data
iterator = 0
for weatherService, configValues in l_weatherServices.iteritems():
  l_headerArray[iterator]={}
  l_headerArray[iterator]["CityName"] = configValues['townname']
  l_headerArray[iterator]["Provider"] = configValues['provider']
  if "openweathermap" in weatherService:
    l_fetchArray[iterator] = openweatherAPI.getData(configValues['apikey'],configValues['townkey'])
  if "wunderground" in weatherService:
    l_fetchArray[iterator]  = wundergroundAPI.getData(configValues['apikey'],configValues['townkey'])

  iterator = iterator + 1

# set up sql table, this will delete existing tables
if create_SQL_table:
  mySQLAPI.createSQLTable(l_config,l_tablename)

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
