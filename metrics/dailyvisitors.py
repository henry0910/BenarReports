import sys, os
sys.path.append(os.path.realpath(''))

import core.config as config
import googleanalytics.metric_strings as ga
from googleanalytics.custom_filter import CustomQueryFilter
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


# to clarify the meaning of "unique":
UNIQUE_VISITORS = 'ga:users'


CONTAINER = GAQueryContainer()

query_base = GAQueryBase(
    dimensions='ga:date',
    metrics=UNIQUE_VISITORS,
    sort='ga:date',
    view_name_includes='Report Data',
    comment='''Calculations.ods instructions:
1) Paste rows into a scratch sheet.
2) Use space as a delimiter (otherwise, OpenOffice will
   insert single quotes in front of the numbers).
3) Verify that the dates are correctly ordered.
4) Paste the metric values into Calculations.ods.'''
)

CONTAINER.add(GAQueryDefinition(query_base, 'dailyvisitors',
    title='Daily Unique Visitors',
    daily_metric=True,
    show_rows=True,
    has_webproperty_sum=False,
    include_total=True,
    row_sort_index=0
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
    metric_keyword= 'dailyvisitors', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='English',
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '=~philippine',
    metric_keyword= 'dailyvisitors', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='Philippines',
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))
