#!/usr/bin/python

from scapy.all import Dot11, Dot11Beacon, sniff
import requests
import json
import uuid
from time import sleep
from urlparse import urljoin

URL = "http://localhost:5000/"

def add(name, ap=False, assoc_with=None):
    radio = {'name': name, 'ap': ap}
    if assoc_with:
        radio['assoc_with'] = assoc_with
    post("/api/merge_radio", radio)


def post(stem, data):
    url = urljoin(URL, stem)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)


post("/api/blank_radios", None)
def add_ap(mac, ssid):
    ap_name=mac
    add(ap_name, ap=True)

def add_sta(mac, ap_name):
    add(mac, assoc_with=ap_name)
    sleep(2)

def add_sta_alone(mac):
    add(mac, ap=False)

interface = "mon0"

def interpret_packet(packet):
    if packet.haslayer(Dot11):
        print "ap-> %s client-> %s | %s | %s" \
              % (packet.addr1, packet.addr2, packet.type, packet.subtype)
        if packet.type == 0 and packet.subtype == 8:
            add_ap(packet.addr2, packet.info)
            print "ap! %s ssid-> %s" % (packet.addr2, packet.info)

sniff(iface='mon0', prn=lambda x:interpret_packet(x), store=0)

