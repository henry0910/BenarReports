import sys, os
sys.path.append(os.path.realpath(''))
import datetime

import core.config as config
import googleanalytics.metric_strings as ga
import googleanalytics.filter_strings as fil
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


# Video Views query
CONTAINER = GAQueryContainer()

# version 1
BASE = GAQueryBase(
    dimensions='ga:pagePath',
    metrics='ga:pageviews',
    sort='ga:pagePath',
    filters=';'.join((fil.CTYPE_VIDEO, fil.PATH_TO_CONTENT_LAUNCH)),
    view_name_includes='Report Data'
)

CONTAINER.add(GAQueryDefinition(BASE, 'videoviews', 
    title='Video Views',
    effective_date=   config.EARLIEST_REPORT_DATE,
    termination_date= datetime.date(2015, 10, 31),
    has_webproperty_sum=True,
    show_rows=False
))

# version 2
BASE.filters = ';'.join((fil.CTYPE_VIDEO, fil.PATH_TO_CONTENT))

CONTAINER.add(GAQueryDefinition(BASE, 'videoviews', 
    title=               'Video Views',
    effective_date=      datetime.date(2015, 11, 1),
    mysql_table=         config.MONTHLY_REPORT_TABLE,
    has_webproperty_sum= True,
    show_rows=           False
))