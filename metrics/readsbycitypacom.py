import sys, os
sys.path.append(os.path.realpath(''))
import datetime

import googleanalytics.metric_strings as ga
import googleanalytics.filter_strings as fil
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


# Cities by Article Reads (PACOM AoR) query
CONTAINER = GAQueryContainer()

# version 1 (no legacy versions have been added)
BASE = GAQueryBase(
    dimensions='ga:city,ga:country',
    metrics='ga:pageviews',
    sort='-ga:pageviews',
    filters=';'.join((fil.READS_V3, fil.VISITOR_COUNTRIES)),
    max_results=15,
    view_name_includes='Report Data'
)

CONTAINER.add(GAQueryDefinition(BASE, 'readsbycitypacom', 
    title='Cities by Article Reads, PACOM AoR',
    effective_date=   datetime.date(2016, 6, 1),
    show_rows=True
))