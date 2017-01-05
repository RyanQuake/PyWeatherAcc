import datetime

# configuration
TT_DAYS=6
TT_INTERVAL=3
TT_MESSPOINTS=(24/TT_INTERVAL)
TT_STAMPS = [None] * (TT_DAYS*TT_MESSPOINTS)

# generate TT_STAMPS array
TT_TODAY  = datetime.date.today()
iterator=0
for i in range(0,TT_DAYS):
    TODAY = TT_TODAY + datetime.timedelta(days=i)
    TIME  = datetime.datetime(100,1,1,00,00,00)
    for j in range(0,TT_MESSPOINTS):
        TT_STAMPS[iterator] = str(TODAY)+" "+str(TIME.time())+" +"+str(i)
        TIME = TIME + datetime.timedelta(hours=TT_INTERVAL)
        iterator=iterator+1
