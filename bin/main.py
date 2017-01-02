from mySQLAPI import mySQLAPI
from openweatherAPI import openweatherAPI
from config import configUtils

# debug variables
create_SQL_table=False # do create a sql table

# local variables

# get SQL settings
l_username  = configUtils.ConfigSectionMap("SQLSettings")['user']
l_password  = configUtils.ConfigSectionMap("SQLSettings")['password']
l_host      = configUtils.ConfigSectionMap("SQLSettings")['host']
l_database  = configUtils.ConfigSectionMap("SQLSettings")['database']
l_row       = configUtils.ConfigSectionMap("SQLSettings")['raise_on_warnings']

config = {
  'user': l_username,
  'password': l_password,
  'host': l_host,
  'database': l_database,
  'raise_on_warnings': bool(l_row)
}

# set up sql table, this will delete existing tables
if create_SQL_table:
  mySQLAPI.createSQLTable(config)

# check for create date or update
if mySQLAPI.dateExists(config,"2017-01-02"):
  # update
  pass
else:
  # create entry
  pass
