import sys, os
sys.path.append(os.path.realpath(''))
import datetime

import core.config as config
import googleanalytics.metric_strings as ga
from googleanalytics.custom_filter import CustomQueryFilter
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


NEW_VISITORS = 'ga:newUsers'


CONTAINER = GAQueryContainer()

query_base = GAQueryBase(
    dimensions='ga:year',
    metrics=NEW_VISITORS,
    view_name_includes='Report Data'
)

CONTAINER.add(GAQueryDefinition(query_base, 'newvisitors',
    title=               'New Visitors for running totals',
    termination_date=    datetime.date(2017, 7, 31),
    include_total=       True,
    show_rows= False
))

CONTAINER.add(GAQueryDefinition(query_base, 'newvisitors',
    title=               'New Visitors for running totals',
    effective_date=      datetime.date(2017, 8, 1),
    include_total=       True,
    show_rows= False,
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
    metric_keyword= 'newvisitors', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='English',
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '=~philippine',
    metric_keyword= 'newvisitors', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='Philippines',
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))
