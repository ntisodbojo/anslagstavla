import sys,os
from glob import glob
import os
from flask import Flask, render_template, jsonify, make_response



basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))


sys.path.append(os.path.join(basepath,"matsedel"))
import thisweek

app = Flask(__name__)

def pages():
    basedir=os.path.dirname(os.path.realpath(__file__))
    os.chdir(os.path.join(basedir,"templates"))
    p=glob('*.html')
    p.remove("index.html")
    return p

def pictures():
    basedir=os.path.dirname(os.path.realpath(__file__))
    os.chdir(os.path.join(basedir,'static'))
    p=glob('pages/*.*')
    return p


@app.route('/')

def index():
    return render_template("index.html", pages=pages(),pictures=pictures())

@app.route('/api/v1/matsedel')
def matsedel():


    return make_response(jsonify(thisweek.weekmenu()))


    # hostname = "192.168.80.150"
    # response = os.system("ping -c 1 -W 1" + hostname)
    # print response
    # if response == 0:
    #     print "bosse is on the school"
    #     return "bosse is on the school"
    # else:
    #     print "bosse has leave the building"
    #     return "bosse has leave the building"



@app.route('/api/v1/busstop')
def busstop():
    import random
    return str(random.randint(1,100))

@app.route('/api/v1/train')
def train():
    #todo coonect to sl
    import random
    return str(random.randint(1,100))



@app.route('/api/v1/menu')
def menu():
    return "{'huvudalternativ':'korv','Vehet':'curry'}"

# router status 1 is off, status 2 is on, 0 means just return status
router_status=2
switch_status=2
infrastruktur_status=2
@app.route('/api/v1/<powerswitch>')
@app.route('/api/v1/<powerswitch>/<int:status>')
def messages(powerswitch,status=0):


    global router_status
    print "status",status
    if status <> 0:
        router_status=status


    print router_status


    powerswitches={'router':1,'switch':2}

    rest_json = []
    for rest in ["bosse","hasse"]:
        rest_json.append(rest)


    #return make_response(jsonify({'count':len(rest_json),'rests':rest_json}))

    return make_response(jsonify({'router':router_status,'switch':switch_status,"infrastruktur":infrastruktur_status}))






if __name__ == '__main__':
    app.run(port=5000, debug=True)
