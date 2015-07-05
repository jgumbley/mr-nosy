#!/usr/bin/python

from scapy.all import Dot11, Dot11Beacon, sniff

interface = "mon0"

def interpret_packet(packet):
    if packet.haslayer(Dot11):
        # print "ap-> %s client-> %s | %s | %s" \
        #       % (packet.addr1, packet.addr2, packet.addr3, packet.type)
        if packet.type == 0 and packet.subtype == 8:
            print "ap! %s ssid-> %s" % (packet.addr2, packet.info)

sniff(iface='mon0', prn=lambda x:interpret_packet(x), store=0)

