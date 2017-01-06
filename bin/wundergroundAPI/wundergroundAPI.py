import json
import urllib
import datetime
import time
from pprint       import pprint
from timestampGEN import timestampGEN

# TODO: document api
# TODO: extend api for data analysis

def getData(i_apiKey, i_townkey):
    WUG_BASE="http://api.wunderground.com/api/"
    WUG_FOR_WEATHER="/hourly10day/"
    WUG_FORMAT=".json"

    retVal_dict = {}
    buffer_dict = {}

    # get forecast data
    url = WUG_BASE+i_apiKey+WUG_FOR_WEATHER+i_townkey+WUG_FORMAT
    response = urllib.urlopen("%s" % url)
    jdata = json.loads(response.read())

    # remove not needed information
    for element in jdata['hourly_forecast']:
        f_hour=int(element['FCTTIME']['hour'])
        f_minute=int(element['FCTTIME']['hour'])
        if 0 == f_hour%timestampGEN.TT_INTERVAL:
            timekey=element['FCTTIME']['epoch']
            timestamp=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timekey)))
            # this will save the data in the specified format
            buffer_dict[timestamp]=element
            del buffer_dict[timestamp]['FCTTIME']

    for key, value in buffer_dict.iteritems():
        for element in timestampGEN.TT_STAMPS:
            if key in element:
                retVal_dict[element]=value

    return retVal_dict
