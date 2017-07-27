# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 10:28:51 2017

@author: Yanchen
"""

from film import getOpener
from bs4 import BeautifulSoup
import pandas as pd
import os
import datetime

filepath = os.path.join(os.getcwd(), 'test');
filelist = os.listdir(filepath);

opener = getOpener();

today = datetime.date.today();
time_line = today - datetime.timedelta(365);

def film(fname):
    name = fname.split('.')[0];
    url = 'http://www.javlibrary.com/cn/vl_searchbyid.php?keyword=';
    try:
        text = opener.open(url + name).read();
        soup = BeautifulSoup(text, "lxml");
        if (soup is not None):
            video_jacket = soup.find("table", {"id": "video_jacket_info"});
            if (video_jacket is not None):
                info = video_jacket.find_all("div");
                video_info = info[1].find_all("div");
                if (video_info is not None):
                    video_date = video_info[1];
                    if (video_date is not None):
                        date = video_date.find("td", {"class": "text"}).contents;
                        if (date is not None):
                            date = date[0].encode('utf-8');
                            video_date_info = datetime.datetime.strptime(date, '%Y-%m-%d').date();
                            if (time_line > video_date_info):
                                os.remove(os.path.join(filepath, fname));
                                print('Remove file %s' % name);
                        else:
                            print('Unable to find %s' % name);
                    else:
                        print('Unable to find %s' % name);
                else:
                    print('Unable to find %s' % name);
            else:
                print('Unable to find %s' % name);
        else:
            print('Unable to find %s' % name);
        
    except Exception as e:
        print('Unable to process the website:', e);
        raise

for fname in filelist:
    film(fname);