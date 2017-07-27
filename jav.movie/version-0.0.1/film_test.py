# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 11:15:27 2017

@author: Yanchen
"""

import os
import pandas as pd

def main():
    path = os.getcwd();
    filepath = path + '\\seen.xlsx';
    seen = pd.read_excel(filepath);
    
    filepath = path + '\\test'
    filelist = os.listdir(filepath);
    
    for file in filelist:
        fname = file.replace('.jpg', '');
        if (any(seen['Film'] == fname)):
            os.remove(os.path.join(filepath, file));
            print('Remove %s' % fname);
    
    print('Remove all duplicate');

if __name__ == '__main__':
    main();