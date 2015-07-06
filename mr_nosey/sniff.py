#!/usr/bin/python

from scapy.all import Dot11, Dot11Beacon, sniff
from redis_api import RadioAPI
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_api = RadioAPI(r)

redis_api.blank_radios()

def add(name, ap=False, assoc_with=None, ssid=None):
    radio = {'name': name, 'ap': ap}
    if assoc_with:
        radio['assoc_with'] = assoc_with
    if ssid:
        radio['ssid'] = ssid
    redis_api.merge_radio(radio)

def add_ap(mac, ssid):
    ap_name=mac
    add(ap_name, ap=True, ssid=ssid)

def add_sta(mac, ap_name):
    add(mac, assoc_with=ap_name)

def add_sta_alone(mac):
    add(mac, ap=False)

interface = "mon0"

def interpret_packet(packet):
    if packet.haslayer(Dot11):
        if packet.type == 0 and packet.subtype == 8:
            add_ap(packet.addr2, packet.info)
        elif packet.type == 1 and packet.subtype == 11:
            add_sta(packet.addr1, packet.addr2)
        elif packet.type == 2 and packet.subtype == 8:
            add_sta(packet.addr1, packet.addr2)
        elif packet.type == 2 and packet.subtype == 0:
            add_sta(packet.addr1, packet.addr2)
        elif packet.type == 2 and packet.subtype == 4:
            add_sta(packet.addr2, packet.addr1)
        else:
            print "ap-> %s client-> %s | %s | %s" \
                  % (packet.addr1, packet.addr2, packet.type, packet.subtype)

sniff(iface='mon0', prn=lambda x:interpret_packet(x), store=0)

