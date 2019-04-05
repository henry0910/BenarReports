import sys, os
sys.path.append(os.path.realpath(''))
import datetime

import googleanalytics.metric_strings as ga
import googleanalytics.filter_strings as fil
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


CONTAINER = GAQueryContainer()

# version 1 (no legacy versions have been added)
BASE = GAQueryBase(
    dimensions='ga:country',
    metrics='ga:pageviews',
    sort='-ga:pageviews',
    filters=fil.READS_V3,
    max_results=300,  # queries all countries to prevent data loss when grouping across ReportSegments
    view_name_includes='Report Data'
)

CONTAINER.add(GAQueryDefinition(BASE, 'readsbycountry', 
    title='Countries by Article Reads',
    effective_date=datetime.date(2016, 6, 1),
    group_by='ga:country',
    show_rows=True,
    max_rows_to_print=12,
    total_only=True
))