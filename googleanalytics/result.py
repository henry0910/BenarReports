import datetime

import googleanalytics.custom_filter as custom_filter
import core.vocabulary as v
from core.vocabulary import NotInVocabularyError
from googleanalytics.query import GAServiceQuery


class GAResult(object):

    def __init__(self, metric_result_group, language, query_definition, ga_connector,
                 join_query=None, verbosity=1):
        
        mrg = metric_result_group
        webproperty_id = v.get('language', language, 'ga_webproperty_id')
        
        if join_query is None:
            self.service_query = GAServiceQuery(query_definition.base, mrg.parent)
        else:
            self.service_query = join_query
        
        if self.service_query is None:
            raise InvalidGAResultError(
                ("GAResult for keyword '%s' and web property ID '%s' has no service_query value. " +
                 "The MetricResultGroup with this keyword may not have been added to a Report.")
                % (self.metric_keyword, webproperty_id))
        
        # the MetricResultGroup may override the view_name_includes value predefined in vocabulary.py
        view_name_includes = query_definition.base.view_name_includes
        if view_name_includes is not None:
            self.service_query.base.view_name_includes = view_name_includes
        
        if query_definition.end_date_today:
            self.service_query.end_date = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
        
        self.rows = None
        self.valid_profile = None
        self.view_name = None
        self.metric_totals = None
        self.split_char = None
        self.group_by = None
        self.contains_sampled_data = None
        
        # Get a list of all Views (Profiles) for the Web Property
        profiles = ga_connector.get_profiles(webproperty_id)

        # find a profile whose name includes view_name_includes,
        # or if there is none, use the first profile
        includes = self.service_query.base.view_name_includes
        self.valid_profile = next((profile for profile in profiles.get('items')), None)  # first profile
        if includes is not None:
            for profile in profiles.get('items'):
                if includes in profile['name']:
                    self.valid_profile = profile
                    break
    
        if self.has_valid_profile():
    
            # execute the GA query, and parse the results
            body = ga_connector.execute_query(self.service_query, self.valid_profile)
            
            self.profile_info = body.get('profileInfo')
            self.query_info = body.get('query')
            self.column_headers = body.get('columnHeaders')
            self.view_name = body.get('profileInfo').get('profileName')
            self.totals_info = body.get('totalResults')
            self.metric_totals = body.get('totalsForAllResults')
            self.rows = self.get_rows(body, max_results=self.service_query.base.max_results)
            
            self.contains_sampled_data = body.get('containsSampledData')
            mrg.data_quality_report.sampling[language] = self.contains_sampled_data
            
            
    def has_valid_profile(self):
        return self.valid_profile is not None
            
    
    # TODO: the group-by code should be moved to MetricResult.rows, because as an
    #       GAResult feature it undermines the purpose of this class by
    #       overriding the original GA result structure with a MetricResult structure.
    def get_rows(self, ga_result_body, max_results=None):
        """
        Gets all the rows of data, and column headers, returned by the API.
        """

        rows = []

        if ga_result_body is None:
            return None

        if ga_result_body.get('rows', []):
            
            for row in ga_result_body.get('rows'):
                rows.append(row)

        headers = []

        for header in ga_result_body.get('columnHeaders'):
            headers.append(header.get('name'))
            
        rows.insert(0, headers)

        return rows if max_results is None else rows[0:max_results+1]  # +1 to account for the header
    
    
    # for debugging purposes only; not reachable by executing main.py
    def print_report_info(self, ga_result_body):
        """Prints general information about this report, if ReportWriter verbosity is at least 3.
        """
        print 'Report Info:'
        print 'Contains Sampled Data = %s' % ga_result_body.get('containsSampledData')
        print 'Kind                  = %s' % ga_result_body.get('kind')
        print 'ID                    = %s' % ga_result_body.get('id')
        print 'Self Link             = %s' % ga_result_body.get('selfLink')
    
    
    # for debugging purposes only; not reachable by executing main.py
    def print_pagination_info(self):
        """Prints common pagination details, if ReportWriter verbosity is at least 3.
        """
        print 'Pagination Info:'
        print 'Items per page = %s' % ga_result_body.get('itemsPerPage')
        print 'Total Results  = %s' % ga_result_body.get('totalResults')
        
        # These only have values if other result pages exist.
        if ga_result_body.get('previousLink'):
            print 'Previous Link  = %s' % ga_result_body.get('previousLink')
        if ga_result_body.get('nextLink'):
            print 'Next Link      = %s' % ga_result_body.get('nextLink')


class GADiffResult(GAResult):
    
    def __init__(self, minuend, subtrahend):
        
        if type(minuend) is not GAResult or type(subtrahend) is not GAResult:
            raise InvalidGAResultError('Cannot create GADiffResult: minuend and subtrahend must be of type GAResult.')
        
        value_index = None
        for index, header in enumerate(minuend.column_headers):
            if header['name'] != subtrahend.column_headers[index]['name']:
                raise InvalidGAResultError('Cannot create GADiffResult: minuend and subtrahend must have identical column headers.')
            if header['name'] in v.get_computable_metrics():
                value_index = index
        
        # copy fields that are expected to have immaterial or no differences between the minuend and subtrahend:
        
        self.service_query = minuend.service_query
        self.column_headers = minuend.column_headers
        self.profile_info = minuend.profile_info
        self.query_info = minuend.query_info
        self.valid_profile = minuend.valid_profile if minuend.valid_profile is not None else subtrahend.valid_profile
        self.view_name = minuend.view_name
        self.metric_totals = minuend.metric_totals
        self.split_char = minuend.split_char
        self.group_by = minuend.group_by
        self.contains_sampled_data = minuend.contains_sampled_data or subtrahend.contains_sampled_data
        self.rows = [minuend.rows[0]]  # copy only the header row initially
        
        # calculate differences:
        
        self.totals_info = minuend.totals_info - subtrahend.totals_info
        
        for row_index, row in enumerate(minuend.rows):

            if row_index > 0:  # skip the first row, because we already copied it
                for column_index, value in enumerate(row):
                    
                    if column_index != value_index:
                        
                        try:
                            subtrahend.rows[row_index][column_index]
                        except IndexError:
                            raise InvalidGAResultError(
                                'Cannot create GADiffResult: minuend and subtrahend ' +
                                'must have the same number of rows and columns.')
                        
                        if value != subtrahend.rows[row_index][column_index]:
                            raise InvalidGAResultError(
                                'Cannot create GADiffResult: minuend and subtrahend rows ' +
                                'must have identical values in all columns except the metric column.')
                    
                    else:
                        
                        row_to_insert = [item for item in row]
                        row_to_insert[value_index] = (
                            int(row_to_insert[value_index]) - int(subtrahend.rows[row_index][value_index]))
                        self.rows.append(row_to_insert)
                        
        for metric_code, total in minuend.metric_totals.iteritems():
            try:
                self.metric_totals[metric_code] = (int(total) - int(subtrahend.metric_totals[metric_code]))
            except KeyError:
                # if it's not possible to calculate a new value, then the old value doesn't need to change
                pass
            

class InvalidGAResultError(Exception):
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)