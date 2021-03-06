#!/usr/bin/env python
# encoding: utf-8

from copy import deepcopy
import os
import cgi
import atexit
import json
from SPARQLWrapper import SPARQLWrapper, JSON

import cgitb
cgitb.enable()

endpoint = []
NE_lat = NE_long = SW_lat = SW_long = 0

form = cgi.FieldStorage()
method = os.environ['REQUEST_METHOD']

if(method == 'GET' and form.has_key('endpoint') and form.has_key('NE_lat') and form.has_key('NE_long') and form.has_key('SW_lat') and form.has_key('SW_long')):
    endpoint = form['endpoint'].value.split(",") 
    NE_lat = form['NE_lat'].value
    NE_long = form['NE_long'].value
    SW_lat = form['SW_lat'].value
    SW_long = form['SW_long'].value

ep_lodac = SPARQLWrapper("http://lod.ac/sparql")
q_lodac = """
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

ep_dbpedia = SPARQLWrapper("http://dbpedia.org/sparql")
ep_jadbpedia = SPARQLWrapper("http://ja.dbpedia.org/sparql")
q_dbpedia = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    SELECT DISTINCT ?link ?title ?lat ?long WHERE {
        ?link rdfs:label ?title;
        geo:lat ?lat;
        geo:long ?long.
        FILTER (
            ?lat > %(SW_lat)s &&
            ?lat < %(NE_lat)s &&
            ?long > %(SW_long)s &&
            ?long < %(NE_long)s &&
            lang(?title) = "ja"
        ).
    }
""" % locals()

ep_lgd = SPARQLWrapper("http://linkedgeodata.org/sparql")
q_lgd = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    SELECT DISTINCT ?link ?title ?lat ?long WHERE {
        ?link rdfs:label ?title;
        geo:lat ?lat;
        geo:long ?long.
        FILTER (
            ?lat > %(SW_lat)s &&
            ?lat < %(NE_lat)s &&
            ?long > %(SW_long)s &&
            ?long < %(NE_long)s &&
            lang(?title) = "ja"
        ).
    }
""" % locals()

ep_wiki = SPARQLWrapper("http://lod.ac/joseki/sparql")
q_wiki = """
    BASE <http://lod.ac/wiki/>
    PREFIX article: <http://lod.ac/wiki/>
    PREFIX a: <http://lod.ac/wiki/>
    PREFIX property: <http://lod.ac/wiki/Property:>
    PREFIX prop: <http://lod.ac/wiki/Property:>
    PREFIX category: <http://lod.ac/wiki/Category:>
    PREFIX cat: <http://lod.ac/wiki/Category:>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX fn: <http://www.w3.org/2005/xpath-functions#>
    PREFIX afn: <http://jena.hpl.hp.com/ARQ/function#>
    SELECT ?link ?title ?lat ?long
    WHERE {
            ?src <http://lod.ac/wiki/Property-3ATitle> ?title;
            <http://lod.ac/wiki/Property-3ALat> ?lat;
            <http://lod.ac/wiki/Property-3ALong> ?long;
            <http://lod.ac/wiki/Property-3ALink> ?link;
            FILTER (
                ?lat > %(SW_lat)s &&
                ?lat < %(NE_lat)s &&
                ?long > %(SW_long)s &&
                ?long < %(NE_long)s
            ).
    }
""" % locals()
 
ep_array = {
    'lodac': {'endpoint':ep_lodac, 'query':q_lodac}, 
    'dbpedia': {'endpoint':ep_dbpedia, 'query':q_dbpedia},
    'jadbpedia': {'endpoint':ep_jadbpedia, 'query':q_dbpedia},
    'lgd': {'endpoint':ep_lgd, 'query':q_lgd},
    'wiki': {'endpoint':ep_wiki, 'query':q_wiki}
}

print "Content-type: text/javascript; charset=utf-8"  
print

result_dict = {}

for e in endpoint:
    sparql_wrapper = ep_array[e]['endpoint']
    sparql = ep_array[e]['query']
    sparql_wrapper.setQuery(sparql)
    sparql_wrapper.setReturnFormat(JSON)
    result_dict[e] = sparql_wrapper.query().convert()

result_json = json.dumps(result_dict, ensure_ascii=False).encode("utf-8")
print result_json
