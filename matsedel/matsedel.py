import json
import requests
from icalendar import Calendar

ics = requests.get("https://sms.schoolsoft.se/nti/jsp/public/right_public_teacher_ical.jsp?key=603ac057aa0b349b11259713b4bc774e")

cal=Calendar.from_ical(ics.text)

matsedel={}

for event in cal.walk('vevent'):

    if  event['Summary'] <> "Matsedel":
        continue
    description=unicode(event['DESCRIPTION'])

    menu_type = description.split("\n")[0].encode('utf-8')
    menu = description.split("\n")[1].encode('utf-8')

    date = str(event['DTSTART'].dt)
    if date in matsedel:
        matsedel[date][menu_type] =  menu
    else:
        matsedel[date]= {menu_type: menu}


with open('menu.json', 'w') as fp:
    json.dump(matsedel, fp,ensure_ascii=False)


