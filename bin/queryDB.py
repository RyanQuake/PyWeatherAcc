from mySQLAPI         import mySQLAPI
from openweatherAPI   import openweatherAPI
from wundergroundAPI  import wundergroundAPI
from config           import configUtils
from pprint           import pprint
import json

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

l_someValue = mySQLAPI.queryByDate(l_config,l_tablename,"2017-01-06","openweathermap")

for item in l_someValue:
    f_cityName = item[0]
    f_date     = item[1]
    f_provider = item[2]
    f_jsonObj  = json.loads(item[3])

    print f_Date, f_jsonObj["main"]["temp"]
