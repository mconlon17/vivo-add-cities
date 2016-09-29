#!/usr/bin/env/python
"""
    cities2rdf.py -- From a data file consisting of cities, make a data package for VIVO

    Version 0.1 MC 2016-09-28
    --  First draft

"""

from rdflib import Graph, URIRef, Namespace, RDF, RDFS, Literal, XSD

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"
__version__ = "0.1"

#   Constants

uri_prefix = "http://openvivo.org/a/city"
dbpedia_prefix = "http://dbpedia.org/resource/"
vivo_prefix = "http://vivoweb.org/ontology/core#"
foaf_prefix = "http://xmlns.com/foaf/0.1/"
vcard_prefix = "http://www.w3.org/2006/vcard/ns#"

VIVO = Namespace(vivo_prefix)
FOAF = Namespace(foaf_prefix)
VCARD = Namespace(vcard_prefix)
OBO = Namespace('http://purl.obolibrary.org/obo/')

names = {}


def add_city(g, label, state_label, latlong):
    """
    Create a city entity
    """

    #   uri is city name if the name is first use, otherwise add a digit to the name
    #   corresponding to duplicate use.  Eg. A, A1, A2

    if name not in names:
        names[name] = 0
        uri = URIRef(uri_prefix + '_'.join(name.split(' ')))

    else:
        names[name] += 1
        uri = URIRef(uri_prefix + str('_'.join(name.split(' ')) + str(names[name])))

    g.add((uri, RDF.type, VIVO.PopulatedPlace))
    g.add((uri, RDFS.label, Literal(label, lang='en')))
    state_uri = URIRef(dbpedia_prefix + '_'.join(state_label.split(' ')))
    g.add((uri, OBO.BFO_0000050, URIRef(state_uri)))

    #   create a vcard with the geolocation

    vcard_uri = URIRef(str(uri)+'-vcard')
    g.add((vcard_uri, RDF.type, VCARD.Individual))
    g.add((uri, OBO.ARG_2000028, vcard_uri))
    vcard_geo_uri = URIRef(str(vcard_uri) + '-geo')
    g.add((vcard_geo_uri, RDF.type, VCARD.Geo))
    g.add((vcard_uri, VCARD.hasGeo, vcard_geo_uri))
    g.add((vcard_geo_uri, VCARD.geo, Literal('geo:'+latlong, datatype=XSD.string)))
    return

#   Main starts here

if __name__ == '__main__':
    city_graph = Graph()

    #   Read the City data

    city_file = open('cities.txt')
    for line in city_file:
        name, state, location = line.strip().split('\t')
        add_city(city_graph, name, state, location)

    #   Generate the RDF file

    triples_file = open('cities.n3', 'w')
    print >>triples_file, city_graph.serialize(format='n3')
    triples_file.close()

