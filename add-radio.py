#!/bin/python

import requests
import json
import uuid
from time import sleep

def add(ap=False):
    url = "http://localhost:5000/api/merge_radio"
    radio = {'name':  str(uuid.uuid1()), 'ap': ap}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(radio), headers=headers)

add(ap=True)
for a in range(300):
    add()
    sleep(2)
