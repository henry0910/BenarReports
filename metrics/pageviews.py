import sys, os
sys.path.append(os.path.realpath(''))
import copy
import datetime

import core.config as config
import googleanalytics.metric_strings as ga
import googleanalytics.filter_strings as fil
from googleanalytics.custom_filter import CustomQueryFilter
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


# version 1 base
BASE_V1 = GAQueryBase(
    dimensions='ga:date',
    metrics='ga:pageviews',
    sort='ga:date',
    filters=fil.PATH_NOT_UNDEFINED,
    view_name_includes='Debug Data',
    comment='''There are pageviews under Report Data from May 21-23,
but they're greater than the number in Debug Data, which doesn't make sense,
so it's recommended to use Debug Data numbers from May 21-23.'''
)

# version 2 base
BASE_V2 = copy.deepcopy(BASE_V1)
BASE_V2.view_name_includes = 'Report Data'
BASE_V2.comment = None

CONTAINER = GAQueryContainer()

# version 1 definition
CONTAINER.add(GAQueryDefinition(
    BASE_V1,
    'pageviews', 
    title='Overall Page Views',
    effective_date=   config.EARLIEST_REPORT_DATE, 
    termination_date= datetime.date(2015, 5, 23),
    has_webproperty_sum=True,
    show_rows=False
))

# version 2 definition
CONTAINER.add(GAQueryDefinition(
    BASE_V2,
    'pageviews', 
    title=               'Overall Page Views',
    effective_date=      datetime.date(2015, 5, 24),
    termination_date=    datetime.date(2017, 7, 31),
    has_webproperty_sum= True,
    show_rows= False
))

# version 3 definition
CONTAINER.add(GAQueryDefinition(
    BASE_V2,
    'pageviews', 
    title=               'Overall Page Views',
    effective_date=      datetime.date(2017, 8, 1),
    has_webproperty_sum= True,
    show_rows= False,
    has_report_lines=    True,  # new version was created for this option, because data doesn't exist for older dates
    mysql_table=         config.MONTHLY_REPORT_TABLE
))


# Philippines GADiffResult filter (use_diff_metric=True):

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '=~philippine',
    metric_keyword= 'pageviews', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='Philippines',
    use_diff_metric=True,
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))
