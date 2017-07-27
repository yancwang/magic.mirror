# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 11:15:27 2017

@author: Yanchen
"""

import os
from film import getOpener
from bs4 import BeautifulSoup

def remove_sub(fname):
    return fname.replace('.jpg', '');
    
def main():
    path = os.getcwd();
    filelist = os.listdir(path + '\\test\\');
    filelist = map(remove_sub , filelist);

    opener = getOpener();
    url = 'https://thepiratebay.org/search/';

    for f in filelist:
        try:
            text = opener.open(url + f).read();
            soup = BeautifulSoup(text, "lxml");
            result = soup.find("table", {"id": "searchResult"});
            if (result != None):
                results = result.find_all("div", {"class": "detName"});
                for r in results:
                    link = r.find("a");
                    title = link.get('title');
                    print title.encode('utf-8');

        except Exception as e:
            print('Unable to process website')
            raise
        
    print("Hit return to exit");
    
if __name__ == '__main__':
    main();    