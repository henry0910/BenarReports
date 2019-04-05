import sys, os
sys.path.append(os.path.realpath(''))
import datetime

import core.config as config
import googleanalytics.metric_strings as ga
import googleanalytics.filter_strings as fil
from googleanalytics.custom_filter import CustomQueryFilter
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


CONTAINER = GAQueryContainer()

# version 1
BASE = GAQueryBase(
    dimensions='%s,ga:date' % ga.LANGUAGE,
    metrics='ga:pageviews',
    sort='ga:date',
    filters=fil.READS_V1,
    view_name_includes='Report Data',
    comment='''Calculations.ods instructions:
1) Paste rows into a scratch sheet.
2) Use space as a delimiter (otherwise, OpenOffice will
   insert single quotes in front of the numbers).
3) Verify that the dates are correctly ordered.
4) Paste the metric values into Calculations.ods.'''
)

CONTAINER.add(GAQueryDefinition(BASE, 'dailyreads',
    title=               'Daily Article Reads',
    effective_date=      config.EARLIEST_REPORT_DATE,
    termination_date=    datetime.date(2015, 10, 31),
    daily_metric=        True,
    show_rows=           True,
    include_total=       False,
    has_webproperty_sum= False
))

# version 2
BASE.filters = fil.READS_V2

CONTAINER.add(GAQueryDefinition(BASE, 'dailyreads', 
    title=               'Daily Article Reads',
    effective_date=      datetime.date(2015, 11, 1),
    termination_date=    datetime.date(2016, 5, 31),
    daily_metric=        True,
    show_rows=           True,
    include_total=       False,
    has_webproperty_sum= False
))

# version 3
BASE.filters = fil.READS_V3

CONTAINER.add(GAQueryDefinition(BASE, 'dailyreads', 
    title=               'Daily Article Reads',
    effective_date=      datetime.date(2016, 6, 1),
    daily_metric=        True,
    show_rows=           True,
    include_total=       False,
    has_webproperty_sum= False
))


# Philippines GADiffResult filter (use_diff_metric=True):

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '=~philippine',
    metric_keyword= 'dailyreads', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='Philippines',
    use_diff_metric=True,
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))
