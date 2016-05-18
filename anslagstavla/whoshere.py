#! /usr/bin/env python
import yaml
import os
import json
import nmap
import socket
import time
import datetime
import sys
from  pprint import pprint

# you can not get macaddress from your own device
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(("8.8.8.8", 80))
    this_ip = s.getsockname()[0]
except:
    this_ip = ""

timestamp = int(time.time())  # this is now
# this is midnight today if last_seen < today, last_seen i yesterday
today = timestamp - (
    datetime.datetime.now() - datetime.datetime.combine(datetime.datetime.now().date(), datetime.time(0))).seconds


# todo make a better logging
def unknown_logger(host, mac="-", vendor="-"):
    print "ip", host, "mac", mac, "vendor", vendor


def find_whoshere(network, config_file="teachers.yaml", whoshere_file='whoshere2.json'):
    # read in the settings to a known_host dict
    try:
        with open(config_file, 'r') as f:
            device_list = yaml.load(f)
    except IOError:
        device_list = {}

    # set some default if teachers or skip list is empty
    if device_list is None:
        device_list = {}

    if not 'teachers' in device_list or device_list['teachers'] is None:
        device_list['teachers'] = {}

    if not 'skip' in device_list or device_list['skip'] is None:
        device_list['skip'] = []

    # sort it by macaddress
    devices = {}

    for key, values in device_list['teachers'].iteritems():
        for value in values:
            devices[value] = key

    for value in device_list['skip']:
        devices[value] = 'skip'

    # if output file exist open and load the dict  it else create new dict
    if os.path.exists(whoshere_file):
        with open(whoshere_file) as f:
            whoshere = json.load(f)

            # changed saved whosherefile to match configfile
            teachers_configfile= set( device_list['teachers'].keys())

            # add teachers that missing in whoshere file
            teachers_in_whoshere = set([teacher['name'] for teacher in  whoshere['teachers']])
            add = list(teachers_configfile -teachers_in_whoshere)

            for name in add:
                whoshere['teachers'].append({'name': name, 'status': 0, "lastseen": 0})

            #  remove teachers that no longer should be tracked
            teachers_in_whoshere = set([teacher['name'] for teacher in  whoshere['teachers']])
            remove = list(teachers_in_whoshere-teachers_configfile)
            whoshere['teachers']= [ x for x in whoshere['teachers'] if x['name'] not in remove ]

    else:
        whoshere = {'teachers': [{'name': name, 'status': 0, "lastseen": 0} for name in device_list['teachers'].keys()]}

    #print whoshere

    # scan the network and find active teachers
    nma = nmap.PortScanner()
    nma.scan(hosts=network, arguments='-sP')

    active = set()

    # counter for unknown hosts
    untracked = 0

    for host in nma.all_hosts():
        # skip if this host is host
        if this_ip == host:
            continue

        try:
            mac = nma[host]['addresses']['mac']
        except:
            untracked += 1
            unknown_logger(host)
            continue

        if mac in devices:
            if devices[mac] <> "skip":
                active.add(devices[mac])
        else:
            untracked += 1
            try:
                vendor = nma[host]['vendor'][mac]
            except KeyError:
                vendor = "unknown"

            unknown_logger(host, mac, vendor)

    # update whoshere
    for teacher in whoshere['teachers']:
        if teacher['lastseen'] <= timestamp:
            if teacher['name'] in active:  # change status
                teacher['status'] = 2
            elif teacher['lastseen'] < today:  # its a new day, away becomes not here
                print "today"
                teacher['status'] = 0  # set status to not here
            elif teacher['status'] == 2:  # the  person  was here earlier
                teacher['status'] = 1  # set status to away
            teacher['lastseen'] = timestamp

    whoshere['status'] = {"untracked": untracked, "timestamp": timestamp}

    with open(whoshere_file, 'w') as fp:
        json.dump(whoshere, fp)

    pprint(whoshere)


if __name__ == "__main__":
    find_whoshere(*sys.argv[1:])
