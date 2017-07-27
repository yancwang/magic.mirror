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

def remove_depulicate():
    # open seen.xlsx file
    path = os.getcwd();
    filepath = os.path.join(path, 'seen.xlsx');
    seen = pd.read_excel(filepath);
    # scan test file
    filepath = os.path.join(path, 'test');
    filelist = os.listdir(filepath);
    # remove duplicates
    for file in filelist:
        fname = file.replace('.jpg', '');
        if (any(seen['Film'] == fname)):
            os.remove(os.path.join(filepath, file));
            print('Remove %s' % fname);
    print('Remove all duplicate');
    pass
    
def main():
    # get film list
    path = os.getcwd();
    filelist = os.listdir(os.path.join(path, 'test'));
    filelist = map(remove_sub , filelist);
    # get internet explorer and pirate bay url
    opener = getOpener();
    url = 'https://thepiratebay.org/search/';
    # print out search result
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
    print("Search finished");
    
if __name__ == '__main__':
    main();    