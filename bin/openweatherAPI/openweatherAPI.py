import json
import urllib
import datetime
from pprint import pprint

gl_TT_DAYS=6
gl_TT_INTERVAL=3
gl_TT_MESSPOINTS=(24/gl_TT_INTERVAL)
gl_TT_STAMPS = [None] * (gl_TT_DAYS*gl_TT_MESSPOINTS)

def getData(i_apiKey, i_townKey, i_countryKey):
    OWM_TOWN=i_townKey+","+i_countryKey
    OWM_CUR_WEATHER="weather?q="+i_townKey
    OWM_FOR_WEATHER="forecast?q="+i_townKey
    OWM_BASE_URL="http://api.openweathermap.org/data/2.5/"
    OWM_APPID=str(i_apiKey)
    OWM_APPID_CALL="&APPID="+OWM_APPID
    OWM_PARAMETERS="&units=metric"

    TT_TODAY  = datetime.date.today()
    iterator=0
    for i in range(0,gl_TT_DAYS):
        TODAY = TT_TODAY + datetime.timedelta(days=i)
        TIME  = datetime.datetime(100,1,1,00,00,00)
        for j in range(0,gl_TT_MESSPOINTS):
            gl_TT_STAMPS[iterator] = str(TODAY)+" "+str(TIME.time())
            TIME = TIME + datetime.timedelta(hours=gl_TT_INTERVAL)
            iterator=iterator+1

    retVal_dict = {}

    # get forecast data
    url = OWM_BASE_URL+OWM_FOR_WEATHER+OWM_APPID_CALL+OWM_PARAMETERS
    response = urllib.urlopen(url)
    jdata = json.loads(response.read())

    for timestamp in gl_TT_STAMPS:
        for element in jdata['list']:
            if timestamp in element['dt_txt']:
                retVal_dict[timestamp] = element

    return retVal_dict
