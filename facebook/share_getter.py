import time
import re
import pycurl
from StringIO import StringIO
from bs4 import BeautifulSoup


# This code is no longer used, because Facebook no longer provides the REST API
# it relied on for share data.

def getPage(url):

    buffer = StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    #c.setopt(c.WRITEDATA, buffer)
    
    try:
        c.perform()
    except pycurl.error:
        return None
    finally:
        c.close()

    body = buffer.getvalue()
    
    return body

def getData(soup):
    try:
        soup_string = str(soup)
        share_count = re.search('share_count>\d+<', soup_string).group(0)[12:-1]
        like_count = re.search('like_count>\d+<', soup_string).group(0)[11:-1]
        comment_count = re.search('comment_count>\d+<', soup_string).group(0)[14:-1]
        click_count = re.search('click_count>\d+<', soup_string).group(0)[12:-1]
        return [share_count, like_count, comment_count, click_count]
    except IndexError:
        return None

def getDataFromUrl(url):
    body = getPage(url) 
    data = None
    if body:
        soup = BeautifulSoup(body, 'html.parser')
        data = getData(soup)
        
    return data

def getUrls(filename='csvsocial/default.csv'):
    fh = open(filename)
    filenames = fh.readlines()
    fh.close()
    return [f.rstrip() for f in filenames]

if __name__ == "__main__":
    
    infiles = ["csvsocial/FacebookShare-English.csv",
               "csvsocial/FacebookShare-Indonesian.csv",
               "csvsocial/FacebookShare-Malaysian.csv",
               "csvsocial/FacebookShare-Thai.csv",
               "csvsocial/FacebookShare-Bengali.csv",
               ]
    
    for infilename in infiles:
        outfilename = infilename.split('.')[0]+"Out"+".csv" 
        matches = {}
        fh = open(outfilename, mode='w')
        for remote_url in getUrls(filename=infilename):

            remote_url = "http://api.facebook.com/restserver.php?method=links.getStats&urls=" + remote_url
            data = getDataFromUrl(remote_url)
            outline = '"%s","%s","%s","%s","%s"\n' % (remote_url, data[0], data[1], data[2], data[3])
            fh.write(outline)
            fh.flush()
            matches[remote_url] = data
        
        fh.close()