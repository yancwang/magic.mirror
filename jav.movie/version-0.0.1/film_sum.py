# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 10:28:51 2017

@author: Yanchen
"""

import os
import pandas as pd

filepath = os.path.join(os.getcwd(), "seen.xlsx");
seen = pd.read_excel(filepath);
dictionary = {};

for index, row in seen.iterrows():
    name = row['Film'].encode('utf-8').split('-')[0];
    if (name in dictionary):
        dictionary[name] = dictionary[name] + 1;
    else:
        dictionary[name] = 1;
        
summary = pd.DataFrame(dictionary.items(), columns = ['Film', 'Number']);
summary = summary.sort_values(by = ['Number'], ascending = False);
summary.index = range(0, summary.shape[0]);

print(summary.head(20));

filepath = os.path.join(os.getcwd(), "sum.xlsx");
summary.to_excel(filepath);