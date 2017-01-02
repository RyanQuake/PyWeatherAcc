import json
import urllib
import datetime
from pprint import pprint

OWM_TOWN="Munich,DE"
OWM_CUR_WEATHER="weather?q="+OWM_TOWN
OWM_FOR_WEATHER="forecast?q="+OWM_TOWN
OWM_BASE_URL="http://api.openweathermap.org/data/2.5/"
OWM_APPID="6b3860a31c7ef579f47505a780abed2d"
OWM_APPID_CALL="&APPID="+OWM_APPID
OWM_PARAMETERS="&units=metric"

TT_STAMP= [None] * 6
today = datetime.date.today()
for i in range(0,6):
    TODAY=today + datetime.timedelta(days=i)
    TIME=" 12:00:00"
    TT_STAMP[i]=str(TODAY)+TIME

#get forecast data
url = OWM_BASE_URL+OWM_FOR_WEATHER+OWM_APPID_CALL+OWM_PARAMETERS
response = urllib.urlopen(url)
jdata = json.loads(response.read())

# pprint(jdata)
for i in TT_STAMP:
    for element in jdata['list']:
        if i in element['dt_txt']:
            print i
            print "\tTemperature:",  element['main']['temp'], "C"
            print "\tHumidity: ", element['main']['humidity'], "%"
            print "\tPressure: ", element['main']['pressure'], "hPa"
            if 'snow' in element.keys():
                    if '3h' in element['snow'].keys():
                        print "snow: ", element['snow']['3h'], "mm"
            if 'rain' in element.keys():
                if '3h' in element['rain'].keys():
                    print "rain: ", element['rain']['3h'], "mm"
