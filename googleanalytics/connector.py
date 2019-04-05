import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build

import core.config as config
from core.api_connector import APIConnector


class GAConnector(APIConnector):
    '''
    A connection to the Google Analytics API.
    '''
    def __init__(self):

        # read the key file
        key_file_location = config.WORKING_DIR + "/" + config.GA_SERVICE_KEY_FILE
        f = open(key_file_location, 'rb')
        key = f.read()
        f.close()
        
        credentials = SignedJwtAssertionCredentials(config.GA_SERVICE_ACCOUNT_EMAIL, key,
                                                    scope=config.GA_SERVICE_SCOPES)
        
        self.validate_connection()
        
        # Authenticate and initialize service. First two parameters are API name and version.
        self.service = build('analytics', config.GA_VERSION, http=credentials.authorize(httplib2.Http()))

    def validate_connection(self):
        
        key_file_location = config.WORKING_DIR + "/" + config.GA_SERVICE_KEY_FILE
        f = open(key_file_location, 'rb')
        key = f.read()
        f.close()
        credentials = SignedJwtAssertionCredentials(config.GA_SERVICE_ACCOUNT_EMAIL, key,
                                                    scope=config.GA_SERVICE_SCOPES)
        build('analytics', config.GA_VERSION, http=credentials.authorize(httplib2.Http()))

    def get_accounts(self):
        
        return self.service.management().accounts().list().execute()
    
    def get_webproperties(self, account_id):
        
        return self.service.management().webproperties().list(accountId=account_id).execute()

    def get_profiles(self, webproperty_id):
        
        return self.service.management().profiles().list(
            accountId=webproperty_id[3:11],  # A GA Account ID is a substring of a Web Property ID
            webPropertyId=webproperty_id
            ).execute()
    
    
    def execute_query(self, ga_service_query, profile):
        # Get Analytics data for a View (Profile), using date range and metrics args
        return self.service.data().ga().get(
            ids='ga:' + profile.get('id'),
            start_date=ga_service_query.start_date,
            end_date=ga_service_query.end_date,
            metrics=ga_service_query.base.metrics,
            dimensions=ga_service_query.base.dimensions,
            max_results=ga_service_query.base.max_results,
            sort=ga_service_query.base.sort,
            filters=ga_service_query.base.filters
            ).execute()
    
    
APIConnector.register(GAConnector)
