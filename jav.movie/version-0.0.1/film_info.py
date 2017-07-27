# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 21:22:45 2017

@author: Yanchen
"""

from film import getOpener
from bs4 import BeautifulSoup
import pandas as pd
import os

path = os.getcwd();
filepath = os.path.join(path, '\\seen.xlsx');
seen = pd.read_excel(filepath);

opener = getOpener();
url = 'http://www.javlibrary.com/en/vl_searchbyid.php?keyword=';

def info(video_jacket):
    info = video_jacket.find_all("div");
    video_info = info[1].find_all("div");
    if (video_info is not None and video_info.__len__() == 9):
        
    else:
        print('Unable to find %s' % name);

for index, row in seen.iterrows():
    name = row['Film'].encode('utf-8');
    text = opener.open(url + name).read();
    soup = BeautifulSoup(text, "lxml");
    if (soup is not None):
        video_jacket = soup.find("table", {"id": "video_jacket_info"});
        if (video_jacket is not None):
            info(video_jacket);
        else:
            video_list = soup.find("div", {"class": "videos"});
            if (video_list is not None):
                vlist = video_list.find_all("div", {"class": "video"});
                for v in vlist:
                    link = v.find('a');
                    title = a.find('div', {"class": "id"}).contents[0].encode('utf-8');
                    if (name == title):
                        
                        break;
            else:
                print('Unable to find %s' % name);    
    else:
        print('Unable to find %s' % name);
