import sys, os
sys.path.append(os.path.realpath(''))
import datetime

import googleanalytics.metric_strings as ga
import googleanalytics.filter_strings as fil
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


CONTAINER = GAQueryContainer()

# version 1 (no legacy versions have been added)
BASE = GAQueryBase(
    dimensions=ga.THEME,
    metrics='ga:pageviews',
    sort='-ga:pageviews',
    filters=fil.READS_V3,
    view_name_includes='Report Data'
)

CONTAINER.add(GAQueryDefinition(BASE, 'readsbytheme', 
    title='Article Reads by Theme',
    effective_date=   datetime.date(2016, 6, 1),
    group_by=ga.THEME,
    show_rows=True,
    total_only=True
))