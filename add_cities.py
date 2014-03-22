#!/usr/bin/env/python
"""
    add-citys.py -- From a data file consisting of UF citys
    add missing citys to VIVO

    Version 0.0 MC 2014-01-14
    --  First draft

"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"

__harvest_text__ = "Python citys " + __version__

from vivotools import vivo_sparql_query
from vivotools import get_vivo_uri
from vivotools import assert_resource_property
from vivotools import assert_data_property
from vivotools import update_data_property
from vivotools import read_csv
from vivotools import rdf_header
from vivotools import rdf_footer
from vivotools import get_vivo_value

from datetime import datetime

def make_state_dict(debug=False):
    """
    Extract all the states in VIVO and organize them into a dictionary
    keyed by name with value URI.
    """
    query = """
    SELECT ?uri ?name
    WHERE {
        ?uri a http://vivoweb.org/ontology/core#StateOrProvince .
        ?uri rdfs:label ?name .
    }"""
    result = vivo_sparql_query(query)
    state_dict = {}
    if 'results' in result and 'bindings' in result['results']:
        rows = result["results"]["bindings"]
    else:
        return state_dict
    if debug:
        print query
        if len(rows) >= 2:
            print rows[0],rows[1]
        elif len(rows) == 1:
            print rows[0]
    for row in rows:
        name = row['name']['value']
        uri = row['uri']['value']
        state_dict[name] = uri
    if debug:
        print state_dict.items()[1:3]
    return state_dict

def make_city_dict(debug=False):
    """
    Extract all the citys in VIVO and organize them into a dictionary
    keyed by name with value URI.
    """
    query = """
    SELECT ?uri ?name
    WHERE {
        ?uri a vivo:PopulatedPlace .
        ?uri rdfs:label ?name .
    }"""
    result = vivo_sparql_query(query)
    city_dict = {}
    if 'results' in result and 'bindings' in result['results']:
        rows = result["results"]["bindings"]
    else:
        return city_dict
    if debug:
        print query
        if len(rows) >= 2:
            print rows[0],rows[1]
        elif len(rows) == 1:
            print rows[0]
    for row in rows:
        name = row['name']['value']
        uri = row['uri']['value']
        city_dict[name] = uri
    if debug:
        print city_dict.items()[1:3]
    return city_dict

def add_city():
    """
    Create a city entity.  Use update_city to set attributes
    """
    ardf = ""
    city_uri = get_vivo_uri()
    add = assert_resource_property(city_uri, "rdf:type",
        "http://vivoweb.org/ontology/core#PopulatedPlace")
    return [ardf, city_uri]

def update_city(city_uri, vivo_data, source_data):
    """
    Loop over properties
    """
    data_properties = [
        "http://www.w3.org/2000/01/rdf-schema#label",
        "http://vivoweb.org/ontology/core#longitude",
        "http://vivoweb.org/ontology/core#latitude"
    ]
    resource_properties = [
        "http://vivoweb.org/ontology/core#geographicallyWithin"
        ]
    ardf = ""
    srdf = ""
    for data_property in data_properties:
        vivo = vivo_data[data_property]
        source = source_data[data_property]
        [add, sub] = update_data_property(city_uri, data_property, vivo, source)
        ardf = ardf + add
        srdf = srdf + sub

    for resource_property in resource_properties:
        vivo = vivi_data[resource_property]
        source = source_data[resource_property]
        [add, sub] = update_resource_property(city_uri, resource_property,\
                                              vivo, source)
        ardf = ardf + add
        srdf = srdf + sub
    return [ardf, srdf]

class StateNotFound(Exception):
    pass

print datetime.now(), "Start"
print datetime.now(), "Make state dictionary"
state_dict = make_city_dict(debug=True)
print datetime.now(), "State dictionary has ", len(state_dict), "entries"
print datetime.now(), "Make city dictionary"
city_dict = make_city_dict(debug=True)
print datetime.now(), "City dictionary has ", len(city_dict), "entries"
print datetime.now(), "Read city file"
cities_data = read_csv("cities.csv")
print datetime.now(), "city file has ", len(cities.items()), "entries"
cities = {}
for row in cities_data:
    name = row['Name']
    if name in city_dict:
        row['city_uri'] = city_dict[name]
    else
        row['city_uri'] = None
    state = row['State']
    if state in state_dict:
        row['state_uri'] = state_dict[name]
    else
        raise StateNotFound(state)
    cities[name] = row
    

print datetime.now(), "Begin processing"
ardf = rdf_header()
srdf = rdf_header()
city_found = 0
city_not_found = 0
for city in cities:
    if city['city_uri'] is None:
        city_not_found = city_not_found + 1
        [add, city_uri] = add_city()
        ardf = ardf + add
        vivo_data = {
        "http://www.w3.org/2000/01/rdf-schema#label": None,
        "http://vivoweb.org/ontology/core#longitude": None,
        "http://vivoweb.org/ontology/core#latitude": None,
        "http://vivoweb.org/ontology/core#geographicallyWithin": None
        }
        city['city_uri'] = city_uri
    else
        city_found = city_found + 1
        vivo_data = {
            "http://www.w3.org/2000/01/rdf-schema#label":vivo_get_value(city_uri,"http://vivoweb.org/ontology/core#label"), 
            "http://vivoweb.org/ontology/core#longitude":vivo_get_value(city_uri,"http://vivoweb.org/ontology/core#latitude"),
            "http://vivoweb.org/ontology/core#latitude":vivo_get_value(city_uri,"http://vivoweb.org/ontology/core#longitude"),
            "http://vivoweb.org/ontology/core#geographicallyWithin":vivo_get_value(city_uri,"http://vivoweb.org/ontology/core#geographicallyWithin"),
            }
#   Found or not, the source data is from the CSV and we're ready for update

    source_data = {
        "http://www.w3.org/2000/01/rdf-schema#label":city['name'],
        "http://vivoweb.org/ontology/core#longitude":city['longitude'],
        "http://vivoweb.org/ontology/core#latitude":city['latitude'],
        "http://vivoweb.org/ontology/core#geographicallyWithin":city['state_uri']
        }
    [add, sub] = update_city(city_uri, vivo_data, source_data)
    ardf = ardf + add
    srdf = srdf + sub
        
print datetime.now(), "Not Found in VIVO, will be added = ", city_not_found
print datetime.now(), "Found in UF data, will be updated = ", city_found
print datetime.now(), "Write files"
adrf = ardf + rdf_footer()
srdf = srdf + rdf_footer()
add_file = open("city_add.rdf", "w")
sub_file = open("city_sub.rdf", "w")
print >>add_file, adrf
print >>sub_file, srdf
add_file.close()
sub_file.close()
print datetime.now(), "Finished"
