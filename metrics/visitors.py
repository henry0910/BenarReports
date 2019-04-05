import sys, os
sys.path.append(os.path.realpath(''))
import datetime

import core.config as config
import googleanalytics.metric_strings as ga
from googleanalytics.custom_filter import CustomQueryFilter
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


# constants to clarify the meaning of "unique":
OLD_UNIQUE_VISITORS = 'ga:newUsers' # replaced by UNIQUE_VISITORS as of February 2016
UNIQUE_VISITORS = 'ga:users'


# Unique Visitors for Report Period query
CONTAINER = GAQueryContainer()

# version 1
BASE = GAQueryBase(
    dimensions=         'ga:date',
    metrics=            OLD_UNIQUE_VISITORS,
    max_results=        None, 
    sort=               None, 
    filters=            None, 
    view_name_includes= 'Report Data'
)

CONTAINER.add(GAQueryDefinition(BASE, 'visitors', 
    title=               'Unique Visitors for report period',
    effective_date=      config.EARLIEST_REPORT_DATE,
    termination_date=    datetime.date(2016, 1, 31),
    show_rows= False,
    has_webproperty_sum= False,
    include_total=       True
))

# version 2
BASE.dimensions = 'ga:year'
BASE.metrics = UNIQUE_VISITORS

CONTAINER.add(GAQueryDefinition(BASE, 'visitors', 
    title=               'Unique Visitors for report period',
    effective_date=      datetime.date(2016, 2, 1),
    termination_date=    datetime.date(2017, 7, 31),
    show_rows= False,
    has_webproperty_sum= False,
    include_total=       True
))

# version 3

CONTAINER.add(GAQueryDefinition(BASE, 'visitors', 
    title=               'Unique Visitors for report period',
    effective_date=      datetime.date(2017, 8, 1),
    show_rows= False,
    has_webproperty_sum= False,
    include_total=       True,
    has_report_lines=    True,
    mysql_table=         config.MONTHLY_REPORT_TABLE
))


# Philippines sub-webproperty filters:

# WARNING:
#    Do not alter these filters in an attempt to capture "lost" visitors
#    to non-sectioned pages. In the case of Unique Visitors, there's no
#    way to do it without the risk of overcounting. It may be possible with
#    New Visitors, but even so, it amounts to having two visitors metrics
#    that apply to different parts of the website. Also, the "loss" of
#    visitors was at most half a percent when last checked.

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '!~philippine',
    metric_keyword= 'visitors', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='English',
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '=~philippine',
    metric_keyword= 'visitors', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='Philippines',
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))
