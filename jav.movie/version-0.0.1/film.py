# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 10:28:51 2017

@author: Yanchen
"""

import urllib2
from bs4 import BeautifulSoup
import pandas as pd
from urllib import urlretrieve
import os
import datetime

class File():
    def __init__(self):
        path = os.getcwd();
        #open seen.xlsx file
        filepath = os.path.join(path, 'seen.xlsx');
        self.seen = pd.read_excel(filepath);
        #open viewed.xlsx file
        filepath = os.path.join(path, 'view.xlsx');
        self.viewed = pd.read_excel(filepath);
    
    #check whether film name is in seen.xlsx    
    def inSeen(self, vname):
        if any(self.seen['Film'] == vname):
            return True;
        else:
            return False;
    
    #check whether film name is in viewed.xlsx    
    def inView(self, vname):
        if any(self.viewed['Film'] == vname):
            return True;
        else:
            return False;
    
    #save viewed film name to viewed array
    def saveViewFilmName(self, vname):
        self.viewed.loc[self.viewed.size] = vname;
    
    #save viewed array to viewed.xlsx        
    def saveView(self):
        self.viewed = self.viewed.drop_duplicates();
        self.viewed = self.viewed.sort_values('Film');
        self.viewed.index = range(0, self.viewed.shape[0]);
        path = os.getcwd();
        filepath = path + '\\view.xlsx';
        self.viewed.to_excel(filepath);

#check if date of film is within one year
def check_date(soup):
    today = datetime.date.today();
    time_line = today - datetime.timedelta(365);
    
    video_jacket = soup.find("table", {"id": "video_jacket_info"});
    info = video_jacket.find_all("div");
    video_info = info[1].find_all("div");
    video_date = video_info[1];
    if (video_date is not None):
        date = video_date.find("td", {"class": "text"}).contents;
        if (date is not None):
            date = date[0].encode('utf-8');
            video_date_info = datetime.datetime.strptime(date, '%Y-%m-%d').date();
            if (time_line > video_date_info):
                return False;             
            else:
                return True;
        else:
            return True;
    else:
        return True;

#return the web browser
def getOpener():
    opener = urllib2.build_opener();
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')];
    return opener;

#save image function
#parameters: url - url of the website; i - pages; f - file;  
def saveImage(url, i, f):
    opener = getOpener();
    u = url + str(i);
    
    try:
        text = opener.open(u).read();
        soup = BeautifulSoup(text, "lxml");
        videos = soup.find("div", {"class": "videos"});
        video = videos.findAll('div', attrs={'class':'video'});

        for v in video:
            vname = v.find("div", {"class": "id"});
            vname = vname.contents;
            vname = vname[0].encode('utf-8');

            href = v.find('a', href=True);
            href = href['href'];
            link = 'http://www.javlibrary.com/cn/';
            if (f.inSeen(vname) == False and f.inView(vname) == False):
                try:
                    text = opener.open(link + href).read();
                    soup = BeautifulSoup(text, "lxml");
                    if (check_date(soup)):
                        img = soup.find('img', {"id": "video_jacket_img"});
                        imgUrl = img['src'];
                        filename = os.path.join(os.getcwd() + '\\film', vname + '.jpg');
                        urlretrieve(imgUrl, filename);
                        f.saveViewFilmName(vname);
                        print('Saving file : %s' % vname);

                except Exception as e:
                    print('Unable to save file %s' % vname);
                    continue;

    except Exception as e:
        print('Unable to process the website', ':', e);

def main():
    #url list
    ulist = ['http://www.javlibrary.com/cn/vl_update.php?&mode=&page=', 
             'http://www.javlibrary.com/cn/vl_newrelease.php?&mode=&page=', 
             'http://www.javlibrary.com/cn/vl_newentries.php?&mode=&page=',
             'http://www.javlibrary.com/cn/vl_mostwanted.php?&mode=&page=',
             'http://www.javlibrary.com/cn/vl_bestrated.php?&mode=&page='];
    
    try:
        f = File();
        for url in ulist:
            for i in range(1, 11):
                saveImage(url, i, f);

        f.saveView();

    except Exception as e:
        f.saveView();
        print('Unable to load file:', e);
            
    print("Hit return to exit");

if __name__ == "__main__":
    main();