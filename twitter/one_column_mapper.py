import pycurl
from StringIO import StringIO

from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs

import time
import re

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

def getLink(soup):
    
    #def isBenarNewsLink(url):
        #if url.find("benarnews.org") != -1:
            #return True
        #return False
    
    #facebook 'buries' the content of the news feed inside a comment we find with....:
    code = soup.find_all('a', class_="twitter-timeline-link")
    if not code:
        return None
    
    try:
        soup_string = str(code)
        benar_url = re.search('url="\S*', soup_string).group(0)
        benar_url = benar_url[5:-1]
        return benar_url
    except:  # TODO: make this catch only IndexError and AttributeError
        return None

def getLinkFromTweet(tweet_permalink):
    body = getPage(tweet_permalink) 
    link = None
    if body:
        soup = BeautifulSoup(body, 'html.parser')
        link = getLink(soup)
        
    return link

def getUrls(filename='Twitter-English.csv'):
    fh = open(filename)
    filenames = fh.readlines()
    fh.close()
    return [f.rstrip() for f in filenames]

if __name__ == "__main__":
    
    infiles = [
#               "Twitter-Korean.csv",
               "Twitter-Bengali.csv",
               "Twitter-English.csv",
               "Twitter-Indonesian.csv",
               "Twitter-Malaysian.csv",
               "Twitter-Philippines.csv",
               "Twitter-Thai.csv",
               ]
    
    for infilename in infiles:
        print "Processing file %s..." % infilename
        outfilename = infilename.split('.')[0]+"Out"+".csv" 
        matches = {}
        fh = open(outfilename, mode='w')
        for tweet_permalink in getUrls(filename=infilename):

            local_url = getLinkFromTweet(tweet_permalink)
            outline = '"%s","%s"\n' % (tweet_permalink, local_url)
            fh.write(outline)
            fh.flush()
            matches[tweet_permalink] = local_url
        
fh.close()