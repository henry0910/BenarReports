import sys, os
sys.path.append(os.path.realpath(''))
import datetime

import core.config as config
import googleanalytics.metric_strings as ga
import googleanalytics.filter_strings as fil
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


# Proxy network article reads by city query

# version 1
CONTAINER = GAQueryContainer()
BASE = GAQueryBase(
    dimensions='ga:city,ga:country',
    metrics='ga:pageviews',
    sort='ga:pageviews',
    filters=';'.join((fil.READS_V3, 'ga:networkDomain==opera-mini.net')),
    view_name_includes='Report Data'
)
CONTAINER.add(GAQueryDefinition(BASE, 'proxyreadsbycity', 
    title='Article Reads from Proxy Networks by City',
    effective_date=   config.EARLIEST_REPORT_DATE,
    termination_date= datetime.date(2016, 9, 30),
    show_rows=True,
    has_webproperty_sum=True,
    total_only=True
))

# version 2
BASE.filters = ';'.join((fil.READS_V3, 'ga:browser==Opera Mini'))

CONTAINER.add(GAQueryDefinition(BASE, 'proxyreadsbycity', 
    title='Article Reads from Proxy Networks by City',
    effective_date=   datetime.date(2016, 10, 1),
    show_rows=True,
    has_webproperty_sum=True,
    total_only=True
))
