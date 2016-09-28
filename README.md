# Add US Cities to VIVO

Create a data package of cities for VIVO.

Each city has a name, a state, a latitude and a longitude.

Look up the state in VIVO.  All the states need to be in VIVO.  Will link to the
default states as provided in a VIVO distribution (dbpedia URLs)


## Notes

There's nothing US specific about this code.  The data file contains US cities.  Edit the data file
to add cities of interest in provinces or regions of interest.

When more than one city has the same name, the first one has a URL of its name, the second one has
the same URL with a '1' at the end.  Third city with the same name has a '2' at the end and so on.

The file cities.n3 is a data package that can be loaded into VIVO.  See the VIVO documentation regarding the
maintenance of data packages.

## Data citation

Wikipedia  (2016): List of United States Cities by Population. Wikipedia. 
https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population Retrieved: 28, SEP 16, 2016
