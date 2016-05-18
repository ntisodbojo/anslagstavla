from datetime import datetime, timedelta
import json


from pprint import pprint

import os,sys

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
menufile=os.path.join(basepath,"menu.json")



def weekmenu():

    with open(menufile, 'r') as f:
        menus = json.load(f)


    today=datetime.now().weekday()



    theweek={}

    firstdayoftheweek= (datetime.now() - timedelta(days=today))
    dayofweek   = [ 'monday', 'tuesday','wednesday', 'thursday', 'friday']

    themenu={}
    themenu["Huvudalternativ"] = "Dataavbrott"
    themenu["Vegetariskt alternativ"] = "Dataavbrott"


    theweekmenu={'today': dayofweek[today]}

    for counter,day  in enumerate(dayofweek):

        date = (firstdayoftheweek + timedelta(days=counter)).strftime("%Y-%m-%d")
        #print counter,day,date,menus[date]
        theweekmenu[day]=themenu.copy()
        if date in menus:
            theweekmenu[day]=menus[date]


    return theweekmenu


pprint(weekmenu())
