# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 19:17:12 2015

@author: James
"""

import csv
import scipy
import pylab as P

def getIndex(elem):
    entry = int(elem["Entry_date"])
    if entry == 0:
        return 0
    elif entry < 11:
        return 1
    elif entry < 21:
        return 2
    elif entry < 31:
        return 3
    elif entry < 41:
        return 4
    elif entry < 51:
        return 5
    elif entry < 61:
        return 6
    elif entry < 71:
        return 7
    elif entry < 81:
        return 8
    elif entry < 91:
        return 9
    else:
        return 10
    

file_name = "cascade_worker.csv"
file_p = open(file_name,"rb")
reader = csv.reader(file_p)

headers = reader.next()

data = {}

for row in reader:
    ID = row[0]
    data[ID] = {}
    for elem in headers:
        if elem != headers[0]:
            data[ID][elem] = row[headers.index(elem)]

tasks = []
for x in xrange(11):
    tasks.append([])
all_tasks = []
for elem in data:
    tasks[getIndex(data[elem])].append(int(data[elem]['Tasks']))
    all_tasks.append(int(data[elem]['Tasks']))
    
new_file_name = file_name.split(".")[0] + "_avg.csv"
new_file = open(new_file_name,"wb")
writer = csv.writer(new_file)

new_headers = ["Entry","Average"]
writer.writerow(new_headers)
bins =["0","1-10","11-20","21-30","31-40","41-50","51-60","61-70","71-80","81-90","91-100"]
for elem in tasks:
    new_row = []
    new_row.append(bins[tasks.index(elem)])
    new_row.append(scipy.average(elem))
    writer.writerow(new_row)
    
new_file.close()
file_p.close()

n, bins, patches = P.hist(all_tasks,10)