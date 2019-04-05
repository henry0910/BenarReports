import requests
import httplib
import pycurl
import json
import ast
from StringIO import StringIO
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs

import core.util as util
import core.config as config
from facebook.connector import FacebookConnector
from core.adjustable_verbosity import AdjustableVerbosityObject
import core.vocabulary as v
from core.vocabulary import NotInVocabularyError


class FacebookLinkMapper(AdjustableVerbosityObject, FacebookConnector):
    ''' Encapsulates all report generator functionality that depends on 
        Facebook APIs.
        
        fb_result_pages: The number of "batches" of posts the Facebook API fetches,
                         starting with the most recent posts. Each batch contains about 25 posts.
        end_date format: A string (in YYYY-MM-DD format) which tells the Facebook API not to
                         fetch any posts created after the specified date.
    '''
    # all attributes with hardcoded defaults are subject to change at Facebook's whim
    def __init__(self, language, verbosity=None, fb_result_pages=10, end_date=None,
                 account_id=None):
        
        AdjustableVerbosityObject.__init__(self, verbosity)
        FacebookConnector.__init__(self)
        
        self.language = language
        self.account_id = v.get('language', language, 'facebook_account_id') if account_id is None else account_id
        self.benarnews_url_mappings = self.get_benarnews_url_mappings(fb_result_pages, end_date)
        
        self.updates_skipped = 0
        self.updates_attempted = 0
        self.updates_successful = 0
    
    
    def get_benarnews_url(self, fb_permalink):
        
        #TODO: test invalid permalink
        if fb_permalink[-1] == '/':
            post_id = fb_permalink[0:-2].split('/')[-1]
        else:
            post_id = fb_permalink.split('/')[-1]
        
        try:
            return self.benarnews_url_mappings['%s_%s' % (self.account_id, post_id)]
        except KeyError: # no mapping found with post_id as the key
            return None
    
    
    def get_benarnews_url_mappings(self, fb_result_pages=10, end_date=None):
        
        mappings = {}
        
        # 2nd arg was originally 'posts', but was changed due to a Facebook API change
        posts = self.api_connection.get_connections(self.account_id, 'feed/?fields=link,permalink_url,created_time', until=end_date)

        initial_postdate = posts['data'][0]['created_time']
        final_postdate = None
        
        # Iterate through the specific number of pages of Facebook posts
        #
        # NOTE: fb_result_pages is used only to determine how many times
        # to call requests.get(posts['paging']['next'])
        for x in range(0, fb_result_pages):
            
            missing_fields = []
            
            # get post ID and link; update final_postdate
            for post in posts['data']:

                if util.dict_item_exists(post, 'id'):
                    found_post_id = str(post['id'])
                else:
                    missing_fields.append('id')
                
                if util.dict_item_exists(post, 'link'):
                    mappings[found_post_id] = post['link']
                else:
                    missing_fields.append('link')
                
                if util.dict_item_exists(post, 'created_time'):
                    final_postdate = post['created_time']
                else:
                    missing_fields.append('created_time')
            
            if len(missing_fields) > 0:
                self.printif("WARNING: Expected field(s) '%s' not found in one or more queried Facebook posts." % "','".join(set(missing_fields)))
            
            try:
                # Attempt to make a request to the next page of data, if it exists.
                posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                # A key error is not a problem when posts['paging']['next']
                # no longer returns a page, because Facebook imposes a limit on
                # the number of pages. In this case, simply break the loop.
                break
        
        self.printif('%s posts from %s to %s mapped.' % (self.language, initial_postdate, final_postdate))
            
        return mappings
    
    
    def map_posts(self, mysql_writer, report_segment):
        
        if report_segment is not None:
            permalink_rows = mysql_writer.select_facebook_permalinks(report_segment, self.language)
        else:
            permalink_rows = mysql_writer.select_all_facebook_permalinks(self.language)
        
        for row in permalink_rows:
            
            mysql_row_id = row[0]
            fb_permalink = row[2]
            benarnews_url = row[3]
            
            if benarnews_url is None or len(benarnews_url) <= 4:
                
                self.updates_attempted += 1
                
                benarnews_url = self.get_benarnews_url(fb_permalink)
                benarnews_url = util.sanitize_benarnews_url(benarnews_url)
                
                if benarnews_url is not None:
                    
                    mysql_writer.update_facebook_post(mysql_row_id, benarnews_url)
                    self.updates_successful += 1
                
                fb_postdate = row[1].strftime('%Y-%m-%d') if row[1] is not None else 'unknown'
                self.printif("MySQL: row #%s (post date: %s) mapped to %s"
                             % (mysql_row_id, fb_postdate, benarnews_url))
            
            else:
                
                self.updates_skipped += 1
                self.printif("MySQL: row #%s skipped" % mysql_row_id)
        

class FacebookLinkMapperError(Exception):
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)