#!/usr/bin/python

from color import *
from netaddr import EUI
from scapy.all import *
from dnslib import DNSRecord # for mdns/bonjour name parsing
from django.utils import timezone
from django.core.exceptions import *
from datetime import datetime #for utcfromtimestamp
from collections import defaultdict

import re

interface = "mon0"

def ascii_printable(s):
	return ''.join(i for i in s if ord(i)>31 and ord(i)<128)

def get_manuf(m):
	try:
		mac = EUI(m)
		manuf = mac.oui.records[0]['org'].split(' ')[0].replace(',','')
		#.replace(', Inc','').replace(' Inc.','')
	except:
		manuf='unknown'
	return ascii_printable(manuf)

probeReqs = []

def jims(packet):
    p = packet
    if p.haslayer(Dot11ProbeReq):
        netName = p.getlayer(Dot11ProbeReq).info
        if netName not in probeReqs:
            probeReqs.append(netName)
            msg= "mac=%s manuf=%s network='%s'" % (p.addr2, get_manuf(p.addr2),
                                                   netName)
            print ascii_printable(msg)

sniff(iface='mon0', prn=lambda x:jims(x), store=0)

