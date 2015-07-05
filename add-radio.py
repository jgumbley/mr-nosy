#!/bin/python

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


def rand_uid():
    return str(uuid.uuid1())

post("/api/blank_radios", None)
def drip_net():
    ap_name=rand_uid()
    add(ap_name, ap=True)
    for a in range(10):
        add(rand_uid(), assoc_with=ap_name)
        sleep(2)

for a in range(100):
    drip_net()
