import json
import urllib
import datetime
from pprint import pprint

# TODO: remove magic numbers

global_TT_STAMP= [None] * 6

def getData(i_apiKey, i_townKey, i_countryKey, i_timeKey):
    OWM_TOWN=i_townKey+","+i_countryKey
    OWM_CUR_WEATHER="weather?q="+i_townKey
    OWM_FOR_WEATHER="forecast?q="+i_townKey
    OWM_BASE_URL="http://api.openweathermap.org/data/2.5/"
    OWM_APPID=str(i_apiKey)
    OWM_APPID_CALL="&APPID="+OWM_APPID
    OWM_PARAMETERS="&units=metric"

    TT_STAMP= [None] * 6
    today = datetime.date.today()
    for i in range(0,6):
        TODAY=today + datetime.timedelta(days=i)
        TIME=" "+i_timeKey
        TT_STAMP[i]=str(TODAY)+TIME
        global_TT_STAMP[i]=str(TODAY)

    retVal_dict = {}

    #get forecast data
    url = OWM_BASE_URL+OWM_FOR_WEATHER+OWM_APPID_CALL+OWM_PARAMETERS
    response = urllib.urlopen(url)
    jdata = json.loads(response.read())

    # pprint(jdata)
    iterator=0
    for i in TT_STAMP:
        for element in jdata['list']:
            if i in element['dt_txt']:
                retVal_dict["`Temp. +"+str(iterator)+" [C]`"] = element['main']['temp']
                retVal_dict["`Pres. +"+str(iterator)+" [hPa]`"] = element['main']['pressure']
                retVal_dict["`Hum. +"+str(iterator)+" [%]`"] = element['main']['humidity']
                if 'snow' in element.keys():
                        if '3h' in element['snow'].keys():
                            retVal_dict["`Prec. +"+str(iterator)+" [mm]`"] = element['snow']['3h']
                if 'rain' in element.keys():
                    if '3h' in element['rain'].keys():
                            retVal_dict["`Prec. +"+str(iterator)+" [mm]`"] = element['rain']['3h']
        iterator=iterator+1

    return retVal_dict
