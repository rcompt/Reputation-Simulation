# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 00:15:51 2015

@author: James
"""

import csv

new_file = open("4pt_worker.csv","wb")
writer = csv.writer(new_file)
headers = ["WorkerID","Entry_date","Ability","Reputation","Like_list_len","Block_list_len","ratings","mid_thres","low_thre","quality","Tasks"]
writer.writerow(headers)
ID = 0
for work in workers:
    new_row = []
    new_row.append(ID)
    new_row.append(work.entry_date)
    new_row.append(work.ability)
    new_row.append(work.reputation)
    new_row.append(len(work.like_list))
    new_row.append(len(work.block_list))
    new_row.append(len(work.ratings))
    new_row.append(work.mid_threshold)
    new_row.append(work.low_threshold)
    new_row.append(work.quality)
    new_row.append(work.tasks_finished)
    writer.writerow(new_row)
    ID += 1
 
new_file.close()
new_file = open("4pt_requestors.csv","wb")
writer = csv.writer(new_file)
headers = ["RequestorID","Entry_date","Behavior","Reputation","Like_list_len","Block_list_len","ratings","mid_thres","low_thre"]
writer.writerow(headers)
ID = 1
for req in requestors:
    new_row = []
    new_row.append(ID)
    new_row.append(req.entry_date)
    new_row.append(req.behavior)     
    new_row.append(req.reputation)
    new_row.append(len(req.like_list))
    new_row.append(len(req.block_list))
    new_row.append(len(req.ratings))
    new_row.append(req.mid_threshold)
    new_row.append(req.low_threshold)
    writer.writerow(new_row)
    ID += 1
 
new_file.close()
 