import sys, os
sys.path.append(os.path.realpath(''))
import datetime

import core.config as config
import googleanalytics.metric_strings as ga
import googleanalytics.filter_strings as fil
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


# Reads by Topic query
CONTAINER = GAQueryContainer()

# version 1
BASE = GAQueryBase(
    dimensions='%s,%s' % ('ga:pagePath', ga.TOPIC),
    metrics='ga:pageviews',
    max_results=5000,
    sort='-ga:pageviews',
    # this filter needs a bug fix; see test_failcases.py
    filters=';'.join((fil.OLD_READS_BY_TOPIC, ga.PUBLICATION_DATE + '=~201508|201509|201510')),
    view_name_includes='Debug Data', 
    comment='''Articles pre-tagged with topics (i.e. published in August 2015 or later).

The join_queries attribute of the vocabulary.py entry for this metric must be
null or empty, because the MetricResult class groups the Google Analytics result by
Topic, and adding any further dimensions may produce inaccurate metric values.'''
)

CONTAINER.add(GAQueryDefinition(BASE, 'readsbytopic', 
    title='Article Reads by Topic',
    effective_date=   config.EARLIEST_REPORT_DATE,
    termination_date= datetime.date(2015, 10, 31),
    group_by=ga.TOPIC,
    show_rows=True,
    total_only=True
))

# version 2
BASE.dimensions = '%s,%s' % (ga.TOPIC, ga.ARTICLE_UID)
BASE.filters = fil.READS_V2
BASE.view_name_includes = 'Report Data'

CONTAINER.add(GAQueryDefinition(BASE, 'readsbytopic', 
    title='Article Reads by Topic',
    effective_date=   datetime.date(2015, 11, 1),
    termination_date= datetime.date(2016, 5, 31),
    group_by=ga.TOPIC,
    show_rows=True,
    total_only=True
))

# version 3
BASE.dimensions = '%s,%s' % (ga.TOPIC, ga.ARTICLE_UID)
BASE.filters = fil.READS_V3
BASE.view_name_includes = 'Report Data'

CONTAINER.add(GAQueryDefinition(BASE, 'readsbytopic', 
    title=              'Article Reads by Topic',
    effective_date=     datetime.date(2016, 6, 1),
    group_by=           ga.TOPIC,
    show_rows=          True,
    total_only=         True
))