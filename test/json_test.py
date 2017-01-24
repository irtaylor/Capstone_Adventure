#!/usr/bin/env python

import json
from pprint import pprint

with open('person.json') as json_data:
    d = json.load(json_data)
    #print(d)
    print(d["first_name"])
