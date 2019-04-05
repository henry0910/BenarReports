import urllib
import subprocess
import warnings
import ast

import facebook
from facebook import GraphAPI

import core.config as config
import core.vocabulary as v
from core.api_connector import APIConnector, APIConnectionError


class FacebookConnector(APIConnector):
    '''
    Connects to the Facebook Graph API.
    '''
    def __init__(self):
        
        graph_api = GraphAPI()
        
        self.access_token = graph_api.get_app_access_token(config.FACEBOOK_APP_ID, config.FACEBOOK_APP_SECRET)
        self.api_connection = facebook.GraphAPI(self.access_token, version=config.FACEBOOK_VERSION)
        
        self.validate_connection()
        
    
    def validate_connection(self):
 
#        try:
        posts = self.api_connection.get_connections(v.get('language', 'English', 'facebook_account_id'), 'posts')
#        except facebook.GraphAPIError:  # should be facebook.GraphAPIError, but importing it doesn't work for some reason
#            raise facebook.GraphAPIError('Cannot load or map Facebook posts: Invalid Graph API token. ' +
#                  'Please access the Facebook Graph API Explorer ' +
#                  '(https://developers.facebook.com/tools/explorer/145634995501895/) for a new token, ' +
#                  'and add it to config.cfg.')


class FacebookConnectorException(Exception):

    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)


APIConnector.register(FacebookConnector)
