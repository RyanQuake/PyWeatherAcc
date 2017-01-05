import json
import urllib
import datetime
from pprint       import pprint
from timestampGEN import timestampGEN

# TODO: document api
# TODO: extend api for data analysis

def getData(i_apiKey, i_townKey):
    OWM_FOR_WEATHER="forecast?id="+i_townKey
    OWM_BASE_URL="http://api.openweathermap.org/data/2.5/"
    OWM_APPID=str(i_apiKey)
    OWM_APPID_CALL="&APPID="+OWM_APPID
    OWM_PARAMETERS="&units=metric"

    retVal_dict = {}

    # get forecast data
    url = OWM_BASE_URL+OWM_FOR_WEATHER+OWM_APPID_CALL+OWM_PARAMETERS
    response = urllib.urlopen(url)
    jdata = json.loads(response.read())

    for timestamp in timestampGEN.TT_STAMPS:
        for element in jdata['list']:
            if element['dt_txt'] in timestamp:
                retVal_dict[timestamp] = element

    return retVal_dict
