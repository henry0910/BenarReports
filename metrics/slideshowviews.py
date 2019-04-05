import sys, os
sys.path.append(os.path.realpath(''))
import datetime

import core.config as config
import googleanalytics.metric_strings as ga
import googleanalytics.filter_strings as fil
from googleanalytics.custom_filter import CustomQueryFilter
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


# Slideshow Views query
CONTAINER = GAQueryContainer()

# version 1:

BASE = GAQueryBase(
    dimensions='ga:date',
    metrics='ga:pageviews',
    max_results=None,
    sort='ga:date',
    filters=';'.join((fil.CTYPE_ARTICLE, fil.SLIDESHOW_NOT_ARTICLE, fil.PATH_TO_CONTENT_LAUNCH)),
    view_name_includes='Report Data',
    comment=None
)

CONTAINER.add(GAQueryDefinition(BASE, 'slideshowviews', 
    title='Slideshow Views',
    effective_date=   config.EARLIEST_REPORT_DATE,
    termination_date= datetime.date(2015, 10, 31),
    has_webproperty_sum=True,
    show_rows=False
))

# version 2:

BASE.filters = ';'.join((fil.CTYPE_ARTICLE, fil.SLIDESHOW_NOT_ARTICLE, fil.PATH_TO_CONTENT_Y15))

CONTAINER.add(GAQueryDefinition(BASE, 'slideshowviews', 
    title='Slideshow Views',
    effective_date=   datetime.date(2015, 11, 1),
    termination_date= datetime.date(2016, 5, 31),
    has_webproperty_sum=True,
    show_rows=False
))

# version 3:

BASE.filters = ';'.join((fil.CTYPE_ARTICLE, fil.SLIDESHOW_NOT_ARTICLE, fil.PATH_TO_CONTENT))

CONTAINER.add(GAQueryDefinition(BASE, 'slideshowviews', 
    title=               'Slideshow Views',
    effective_date=      datetime.date(2016, 6, 1),
    termination_date=    datetime.date(2017, 7, 31),
    has_webproperty_sum= True,
    show_rows= False
))

# version 4:

BASE = GAQueryBase(
    dimensions='%s' % ga.ARTICLE_CMSID,
    metrics='ga:pageviews',
    filters=';'.join((fil.CTYPE_ARTICLE, fil.SLIDESHOW_NOT_ARTICLE, fil.PATH_TO_CONTENT)),
    view_name_includes='Report Data'
)

CONTAINER.add(GAQueryDefinition(BASE, 'slideshowviews', 
    title=               'Slideshow Views',
    effective_date=      datetime.date(2017, 8, 1),
    has_webproperty_sum= False,
    show_rows= False,
    has_report_lines=    True,
    mysql_table=         config.MONTHLY_REPORT_TABLE,
    adjust_for_uncategorized_articles=True
))


# Philippines sub-webproperty filters:

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '!~philippine',
    metric_keyword= 'slideshowviews', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='English',
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '=~philippine',
    metric_keyword= 'slideshowviews', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='Philippines',
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))
