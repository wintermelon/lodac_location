#!/usr/bin/env python
# encoding: utf-8

import os
import cgi
import cgitb
import httplib
import urllib

cgitb.enable()
form = cgi.FieldStorage()
method = os.environ['REQUEST_METHOD']

url_header = "www.geocoding.jp"
conn = httplib.HTTPConnection(url_header)

print "Content-type: text/xml; charset=utf-8"  
print

if(method == 'GET' and form.has_key('new_center')):
    new_center = form['new_center'].value;
    url = "/api/?v=1.1&q="+new_center
    conn.request("GET", url)
    res = conn.getresponse()
    data = res.read()
    print data


