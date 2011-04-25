#!/opt/local/bin/python
# encoding: utf-8

import os
import cgi
import atexit
from SPARQLWrapper import SPARQLWrapper, JSON

import cgitb
cgitb.enable()

NE_lat = NE_long = SW_lat = SW_long = 0

form = cgi.FieldStorage()
method = os.environ['REQUEST_METHOD']

if(method == 'GET' and form.has_key('NE_lat') and form.has_key('NE_long') and form.has_key('SW_lat') and form.has_key('SW_long')):
    NE_lat = form['NE_lat'].value
    NE_long = form['NE_long'].value
    SW_lat = form['SW_lat'].value
    SW_long = form['SW_long'].value

sparql = SPARQLWrapper("http://location.lod.ac/sparql")
query = """
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX omgeo: <http://www.ontotext.com/owlim/geo#>
    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    SELECT distinct ?link ?title ?lat ?long
    WHERE{
        ?link omgeo:within(%(NE_lat)s %(NE_long)s %(SW_lat)s %(SW_long)s);
        dct:title ?title;
        geo:lat ?lat;
        geo:long ?long;
        .
    }
    """ % locals()

# ?type <http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing>
# ?type <http://lod.ac/ns/location#PostalCode>; 

sparql.setQuery(query)
sparql.setReturnFormat(JSON)

print "Content-type: text/javascript; charset=utf-8"  
print

results = str(sparql.query().convert())
results = results.replace("'", "\"")
results = results.replace("u\"", "\"")
print results


