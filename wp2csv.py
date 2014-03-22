#!/usr/bin/env/python
"""
    wp2csv.py -- read wikipedia data and write a csv

    Version 0.1 MC 2014-03-21
    --  works as expected

"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"

from datetime import datetime

print datetime.now(), "Start"
w_file = open("cities.txt","r")
csv_file = open("cities.csv","w")
i = 0
for line in w_file:
    i = i + 1
    if i % 3 == 1:
        data = []
        a = line.split(' ')
        data.append(a[1].replace('_',' '))
        data.append(a[2].replace('_',' '))
    elif i %3 == 2:
        pass
    else:
        line = line.strip('\n')
        a = line.split(' ')
        data.append(a[3])
        data.append(a[4])
        print >>csv_file,"|".join(data)
w_file.close()
csv_file.close()
print datetime.now(), "Finished"
