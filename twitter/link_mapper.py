import re
import pycurl
from StringIO import StringIO
from bs4 import BeautifulSoup

import core.config as config
import core.util as util


class TwitterLinkMapper(object):
    ''' Encapsulates all report generator functionality that depends on tweet parsing.
    '''
    # all attributes with hardcoded defaults are subject to change at Facebook's whim
    def __init__(self, language, upload=False
#                 verbosity=None
                 ):
        
#        AdjustableVerbosityObject.__init__(self, verbosity)
        
        self.language = language
        self.account_id = None
        
        if upload:
            self.benarnews_url_mappings = self.get_benarnews_url_mappings()
        else:
            self.benarnews_url_mappings = None
        
        #self.updates_skipped = 0
        #self.updates_attempted = 0
        #self.updates_successful = 0


    def get_page(self, url):
    
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
    
    
    def get_benarnews_url(self, soup):
        
        #def isBenarNewsLink(url):
            #if url.find("benarnews.org") != -1:
                #return True
            #return False
        
        # find the content of the Twitter page
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
    
    
    def get_link_from_tweet(self, tweet_permalink):
        
        body = self.get_page(tweet_permalink) 
        link = None
        if body:
            soup = BeautifulSoup(body, 'html.parser')
            link = self.get_benarnews_url(soup)
            
        return link
    
    
    def get_urls(self, filename="Twitter-English.csv"):
        fh = open(filename)
        lines = fh.readlines()[1:]
        fh.close()
        return [line.split(',')[3] for line in lines]
    
    
    def get_benarnews_url_mappings(self):
        
        infile = "%s/Twitter-%s.csv" % (config.CSV_INPUT_DIR, self.language)
        outfile = infile.split('.')[0]+"Out"+".csv" 
        matches = {}
        fh = open(outfile, mode='w')
        for tweet_permalink in self.get_urls(filename=infile):

            local_url = self.get_link_from_tweet(tweet_permalink)
            outline = '"%s","%s"\n' % (tweet_permalink, local_url)
            fh.write(outline)
            fh.flush()
            matches[tweet_permalink] = local_url

        fh.close()        
        return matches


    def map_posts(self, mysql_writer, report_segment):
        
        if report_segment is not None:
            permalink_rows = mysql_writer.select_twitter_permalinks(report_segment, self.language)
        else:
            permalink_rows = mysql_writer.select_all_twitter_permalinks(self.language)
        
        for row in permalink_rows:
            
            mysql_row_id = row[0]
            tw_permalink = row[2]
            benarnews_url = row[3]
            
            if benarnews_url is None or len(benarnews_url) <= 4:
                
#                self.updates_attempted += 1
                
                benarnews_url = self.get_link_from_tweet(tw_permalink)
                benarnews_url = util.sanitize_benarnews_url(benarnews_url)
                
                if benarnews_url is not None:
                    
                    mysql_writer.update_twitter_post(mysql_row_id, benarnews_url)
#                    self.updates_successful += 1
                
                #tw_postdate = row[1].strftime('%Y-%m-%d') if row[1] is not None else 'unknown'
                #self.printif("MySQL: row #%s (post date: %s) mapped to %s"
                             #% (mysql_row_id, tw_postdate, benarnews_url))
            
#            else:
                
#                self.updates_skipped += 1
#                self.printif("MySQL: row #%s skipped" % mysql_row_id)
