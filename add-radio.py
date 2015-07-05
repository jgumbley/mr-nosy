#!/bin/python

import requests
import json

url = "http://localhost:5000/api/merge_radio"
radio = {'name': 'shoop'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(radio), headers=headers)
