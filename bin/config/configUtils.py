import ConfigParser
import os

Config  = ConfigParser.ConfigParser()
pathfile= os.path.join("config","config.ini")
Config.read(pathfile)

def ConfigSectionMap(section):
    dict1 = {}
    try:
        options = Config.options(section)
    except:
        print "Error: Config file not according exsample."
        print "Please read README for further details."
        exit(1)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
