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
    dimensions=ga.LANGUAGE,
    metrics='ga:pageviews',
    filters=';'.join((fil.READS_V1, fil.VISITOR_COUNTRIES)), 
    view_name_includes='Report Data'
)

CONTAINER.add(GAQueryDefinition(BASE, 'pacomreads',
    title='Article Reads in the PACOM AoR',
    effective_date=   config.EARLIEST_REPORT_DATE,
    termination_date= datetime.date(2015, 10, 31),
    show_rows=False,
    has_webproperty_sum=True
))

# version 2
BASE.filters = ';'.join((fil.READS_V2, fil.VISITOR_COUNTRIES))

CONTAINER.add(GAQueryDefinition(BASE, 'pacomreads', 
    title='Article Reads in the PACOM AoR',
    effective_date=   datetime.date(2015, 11, 1),
    termination_date= datetime.date(2016, 5, 31),
    show_rows=False,
    has_webproperty_sum=True
))

# version 3
BASE.filters = ';'.join((fil.READS_V3, fil.VISITOR_COUNTRIES))

CONTAINER.add(GAQueryDefinition(BASE, 'pacomreads', 
    title=               'Article Reads in the PACOM AoR',
    effective_date=      datetime.date(2016, 6, 1),
    show_rows=           False,
    has_webproperty_sum= True
))


# Philippines GADiffResult filter (use_diff_metric=True):

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '=~philippine',
    metric_keyword= 'pacomreads', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='Philippines',
    use_diff_metric=True,
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))
