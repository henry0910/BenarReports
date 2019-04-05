import os
import copy
import datetime

import core.util as util
import core.config as config


class GAQueryBase(object):
    
    def __init__(self, dimensions=None, metrics=None, max_results=None, sort=None, filters=None,
                 view_name_includes=None, comment=None):
        '''
        An object containing the minimum parameters needed for a Google Analytics query.
        All of this class's attributes are attributes of a Google Analytics query,
        except for comment, an optional string for developer notes which may be printed
        along with the query result.
        '''
        self.dimensions = dimensions
        self.metrics = metrics
        self.max_results = max_results
        self.sort = sort
        self.filters = filters
        self.view_name_includes = view_name_includes
        self.comment = comment


class GAQueryDefinition(object):
    '''
    Parameters:
        :query_base (GAQueryBase): the query parameters used by Google Analytics
        :keyword (str):  used to look up additional attributes from core.vocabulary.py
        :title (str):  the human-readable title of the query (i.e. 'Article Reads')
        
        :adjust_for_uncategorized_articles (bool): whether to adjust the values of the metric result according to records in the cms_items database table, where special content items which cannot be captured by a Google Analytics query (i.e. BenarNews Philippines articles outside the Philippines section of the English-language website) are stored.
        :country (str): the name of a country by which to filter the query, so that only results for that country are shown
        :effective_date (datetime.date): the earliest date for which the query is valid
        :end_date_today (bool): whether the date range of the query should end on today's date (defaults to the end date of the Report object to which the GAQueryDefinition belongs)
        :group_by (string): analogous to the MySQL command; the code for a Google Analytics Dimension (i.e. 'ga:date') by which to group query results
        :has_report_lines (bool): if True, instructs ReportWriter to store the results of this query in a MonthlyReportLineGroup or QuarterlyReportLineGroup object
        :has_report_tables (bool): True if a custom class exists for this query in report_table_group.py (i.e. the TopArticlesReportTableGroup class, built for queries of the 'toparticles' metric), and if that class is intended to be used in the report
        :has_row_sum (bool): if True, a sum of all rows for each webproperty is calculated and output by ReportWriter
        :has_webproperty_sum (bool): if True, a sum of all values for all webproperties is calculated and output by ReportWriter
        :include_total (bool): if True, the Totals webproperty is included in the list of queried webproperties
        :join_queries (GAQueryBase list): a list of additional GAQueryBase objects to join to base_query
        :max_rows_to_print (int): the maximum number of query result rows for ReportWriter to output
        :metric_index (int): the index of the query result column containing the Google Analytics Metric (all other columns are Dimensions)
        :mysql_table (str): the name of the MySQL table where the query results will be stored
        :reverse_row_sort (bool): if True, the rows of the query result are sorted in reverse order by value
        :row_sort_index (int): the index of the column by which to sort the query result
        :show_rows (bool): if True, instructs the ReportWriter to display any rows of the query result in its output
        :termination_date (datetime.date): the latest date for which the query is valid
        :total_only (bool): if True, instructs the ReportWriter to query and output only the Totals webproperty
        
    Attributes:
        Aside from the attributes provided by the GAQueryDefinition parameters,
        GAQueryDefinition receives all the attributes of QAQueryBase
        through the query_base parameter.
      
    Stores an GAQueryBase object, and adds attributes to it
    which are needed to interface with the rest of the reporting code.
    If multiple versions of a query need to be stored in an GAQueryDictionary,
    versions are defined here via effective_date and termination_date.
    '''
    def __init__(self, query_base, keyword, title,
                 adjust_for_uncategorized_articles=False,
                 country=None,
                 daily_metric=False,
                 effective_date=None,
                 end_date_today=False,
                 group_by=None,
                 has_report_lines=False,
                 has_report_tables=None,
                 has_row_sum=True,
                 has_webproperty_sum=None,
                 include_total=False,
                 join_queries=None,
                 max_rows_to_print=None,
                 metric_index=None,
                 mysql_table=None,
                 reverse_row_sort=False,
                 row_sort_index=1,
                 show_rows=None,
                 termination_date=None,
                 total_only=False):
        
        # if the following attributes are both True, it's possible for a sum to
        # be calculated on overlapping webproperties (i.e. English plus Totals),
        # so an exception must be raised to prevent it
        if has_webproperty_sum and include_total:
            raise GAQueryDefinitionException('has_webproperty_sum and include_total cannot both be True, due to the risk of double-counting data')
        
        if effective_date and termination_date and effective_date >= termination_date:
            raise GAQueryDefinitionException('effective_date must be earlier than termination_date')
        
        self.base = copy.deepcopy(query_base)
        self.parent = None  # set by QueryContainer.add()
        self.keyword = keyword
        self.title = title
        
        self.adjust_for_uncategorized_articles = adjust_for_uncategorized_articles
        self.country = country
        self.daily_metric = daily_metric
        self.effective_date = effective_date if effective_date is not None else config.EARLIEST_REPORT_DATE
        self.end_date_today = end_date_today  # used for queries like Articles Published
        self.group_by = group_by
        self.has_report_tables = has_report_tables
        self.has_report_lines = has_report_lines
        self.has_row_sum = has_row_sum
        self.has_webproperty_sum = has_webproperty_sum
        self.include_total = include_total
        self.join_queries = [] if join_queries is None else join_queries
        self.max_rows_to_print = max_rows_to_print
        self.metric_index = metric_index
        self.mysql_table = mysql_table
        self.reverse_row_sort = reverse_row_sort
        self.row_sort_index = row_sort_index
        self.show_rows = show_rows
        self.termination_date = termination_date if termination_date is not None else datetime.date.today()
        self.total_only = total_only
        self.webproperty_ids = []  # set by ReportWriter
        
        
    def get_parameter_by_report(self, parameter, report_segment):
        
        if (self.effective_date <= report_segment.start_date and report_segment.end_date <= self.termination_date):
            return getattr(self, parameter)
        
        # if nothing was returned, raise an error
        raise NotInVocabularyError("Query parameter '%s' for ReportSegment dated %s to %s"
                                   % (parameter, report_segment.start_date, report_segment.end_date))
    
    
    def apply_custom_filters(self, custom_filter_list):

        for custom in custom_filter_list:
            custom_str = custom.filter_string
            # use deepcopy so the change doesn't affect other queries
            if self.base.filters is None:  # some queries don't have filters, so we're careful not to join on None here
                self.base.filters = custom_str
            else:
                if custom.replace:
                    self.base.filters = custom_str
                else:
                    self.base.filters = ';'.join([self.base.filters, custom_str])


class GAServiceQuery(object):
    '''
    Implementation of an GAQueryBase with a start date, end date,
    and GA service object.
    '''
    def __init__(self, query_base, report_segment):
        
        # deepcopy the query base so the change doesn't affect other queries
        self.base = copy.deepcopy(query_base)
        # converts datetime objects to strings in the format expected by the Google API
        self.start_date = datetime.date.strftime(report_segment.start_date, "%Y-%m-%d")
        self.end_date = datetime.date.strftime(report_segment.end_date, "%Y-%m-%d")


class GAQueryContainer(object):
    '''
    Stores all versions of a GA query, and encapsulates the query attributes so
    that the correct version of each attribute is returned when its getter is called.
    '''
    def __init__(self, query_definitions=None):
        
        if query_definitions is not None and len(query_definitions) > 0:
            
            self.queries = sorted(query_definitions, key=lambda qd: qd.effective_date)
            
            unique_keywords = set(qd.keyword for qd in query_definitions)
            if len(unique_keywords) > 1:
                raise GAQueryKeywordError(', '.join(unique_keywords))
            
        else:
            
            # query definitions can be added later, instead of during initialization
            self.queries = []
        
        self.custom_filters = []
        
        
    def add(self, query_definition):
        
        self.queries.append(query_definition)
        query_definition.parent = self
        
        unique_keywords = set(qd.keyword for qd in self.queries)
        if len(unique_keywords) > 1:
            raise GAQueryKeywordError(', '.join(unique_keywords))
        
        
    def get_query_definition_for_report(self, report_segment):
        
        for query in self.queries:
            if query.effective_date <= report_segment.start_date and query.termination_date >= report_segment.end_date:
                return query
        return None
        
        
    def latest_query(self):
        
        return self.queries[-1] if len(self.queries) > 0 else None


    def keyword(self):
        
        return self.latest_query.keyword()
        
        
    def get_parameter(self, parameter, version_date=None):
        
        if len(self.queries) == 1 or version_date is None:
            
            return getattr(self.latest_query, parameter)
        
        elif version_date is not None:
            
            for query in self.queries:
                if (query.effective_date <= version_date and version_date <= query.termination_date):
                    return getattr(query, parameter)
                
        # if nothing was returned, raise an error
        raise NotInVocabularyError("Query parameter '%s' for version date '%s'"
                                   % (parameter, version_date if version_date is not None else '(no date)'))
        
        
    def get_parameter_by_report(self, parameter, report_segment):
        
        if len(self.queries) == 1 or report_segment is None:
            # parameter may be either in GAQueryDefinition or GAQueryBase,
            # hence the AttributeError except clause
            try:
                return getattr(self.latest_query(), parameter)
            except AttributeError:
                return getattr(self.latest_query().base, parameter)
        else:
            for query in self.queries:
                if (query.effective_date <= report_segment.start_date and report_segment.end_date <= query.termination_date):
                    try:
                        return getattr(query, parameter)
                    except AttributeError:
                        return getattr(query.base, parameter)
        
        # if nothing was returned, raise an error
        raise NotInVocabularyError("Query parameter '%s' for ReportSegment dated %s to %s"
                                   % (parameter, report_segment.start_date, report_segment.end_date))
    
    
    def get_filters(self, metric_keyword=None, webproperty_id=None, use_diff_metric=None,
                    report_start_date=None, report_end_date=None, report_keyword=None,
                    include_subwebproperty_filters=True):
    
        if include_subwebproperty_filters:
            matching_filters = copy.deepcopy(self.custom_filters)
        else:
            matching_filters = [f for f in copy.deepcopy(self.custom_filters) if f.sub_webproperty_name is None]
    
        if metric_keyword is not None:
            matching_filters = [f for f in matching_filters if f.metric_keyword == metric_keyword]
        if report_start_date is not None:
            matching_filters = [f for f in matching_filters if f.effective_date <= report_start_date]
        if report_end_date is not None:
            matching_filters = [f for f in matching_filters if f.termination_date >= report_end_date]
        if webproperty_id is not None:
            matching_filters = [f for f in matching_filters if f.webproperty_id == webproperty_id]
        if use_diff_metric is not None:
            matching_filters = [f for f in matching_filters if f.use_diff_metric == use_diff_metric]
    
        # report_keyword is for special reports, so if None is specified, remove all
        # filters associated with a special report
        if report_keyword is None:
            matching_filters = [f for f in matching_filters if f.report_keyword is None]
        else:
            matching_filters = [f for f in matching_filters if f.report_keyword == report_keyword]
    
        return matching_filters
    
    
    def get_sub_webproperty_filters(self, metric_keyword=None, webproperty_id=None, use_diff_metric=None,
                                    report_start_date=None, report_end_date=None, report_keyword=None):
    
        matching_filters = [f for f in copy.deepcopy(self.custom_filters) if f.sub_webproperty_name is not None]
    
        if metric_keyword is not None:
            matching_filters = [f for f in matching_filters if f.metric_keyword == metric_keyword]
        if report_start_date is not None:
            matching_filters = [f for f in matching_filters if f.effective_date <= report_start_date]
        if report_end_date is not None:
            matching_filters = [f for f in matching_filters if f.termination_date >= report_end_date]
        if webproperty_id is not None:
            matching_filters = [f for f in matching_filters if f.webproperty_id == webproperty_id]
        if use_diff_metric is not None:
            matching_filters = [f for f in matching_filters if f.use_diff_metric == use_diff_metric]
    
        # report_keyword is for special reports, so if None is specified, remove all
        # filters associated with a special report
        if report_keyword is None:
            matching_filters = [f for f in matching_filters if f.report_keyword is None]
        else:
            matching_filters = [f for f in matching_filters if f.report_keyword == report_keyword]
    
        return matching_filters    

    
class GAQueryKeywordError(Exception):
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr('Only one keyword allowed per GAQueryContainer, but multiple keywords found: ' + self.value)

    
class GAQueryDefinitionException(Exception):
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
    
    
# TODO: raise this instead of KeyError when a dictionary element is not found?
# TODO: find a way to consolidate this with the NotInVocabularyError class in vocabulary.py
class NotInVocabularyError(Exception):
    
    def __init__(self, value=None):
        self.value = value if value is not None else "An item"
        
    def __str__(self):
        return repr('%s was not found in %s' % (self.value, os.path.basename(__file__)))