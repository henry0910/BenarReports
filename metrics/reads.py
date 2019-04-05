import sys, os
sys.path.append(os.path.realpath(''))
import datetime
import copy

import core.config as config
import googleanalytics.metric_strings as ga
import googleanalytics.filter_strings as fil
from googleanalytics.custom_filter import CustomQueryFilter
from googleanalytics.query import GAQueryBase, GAQueryDefinition, GAQueryContainer


CONTAINER = GAQueryContainer()

# version 1:

BASE = GAQueryBase(
    dimensions=         ga.LANGUAGE,
    metrics=            'ga:pageviews',
    sort=               ga.LANGUAGE,
    filters=            fil.READS_V1,
    view_name_includes= 'Report Data',
    comment=            '''Calculations.ods instructions:
1) Paste rows into a scratch sheet.
2) Use space as a delimiter (otherwise, OpenOffice will
   insert single quotes in front of the numbers).
3) Verify that the dates are correctly ordered.
4) Paste the metric values into Calculations.ods.'''
)

CONTAINER.add(GAQueryDefinition(BASE, 'reads',
    title=               'Article Reads',
    effective_date=      config.EARLIEST_REPORT_DATE,
    termination_date=    datetime.date(2015, 10, 31),
    show_rows= False,
    include_total=       False,
    has_webproperty_sum= True
))

# version 2:

BASE.filters = fil.READS_V2

CONTAINER.add(GAQueryDefinition(BASE, 'reads', 
    title=               'Article Reads',
    effective_date=      datetime.date(2015, 11, 1),
    termination_date=    datetime.date(2016, 5, 31),
    show_rows= False,
    include_total=       False,
    has_webproperty_sum= True
))

# version 3:

BASE.filters = fil.READS_V3

CONTAINER.add(GAQueryDefinition(BASE, 'reads', 
    title=               'Article Reads',
    effective_date=      datetime.date(2016, 6, 1),
    termination_date=    datetime.date(2017, 7, 31),
    show_rows= False,
    include_total=       False,
    has_webproperty_sum= True,
    mysql_table=         config.MONTHLY_REPORT_TABLE
))

# version 4:

BASE = GAQueryBase(
    dimensions=         '%s' % ga.ARTICLE_CMSID,
    metrics=            'ga:pageviews',
    filters=            fil.READS_V3,
    view_name_includes= 'Report Data'
)

CONTAINER.add(GAQueryDefinition(BASE, 'reads',
    title=               'Article Reads',
    effective_date=      datetime.date(2017, 8, 1),
    show_rows= False,
    has_webproperty_sum= False,
    has_report_lines=    True,
    mysql_table=         config.MONTHLY_REPORT_TABLE,
    adjust_for_uncategorized_articles=True
))


# Philippines sub-webproperty filters:

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '!~philippine',
    metric_keyword=       'reads', 
    webproperty_id=       ga.get_webproperty_by_language('English'),
    sub_webproperty_name= 'English',
    effective_date=       config.EARLIEST_PHILIPPINES_REPORT_DATE
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '=~philippine',
    metric_keyword=       'reads', 
    webproperty_id=       ga.get_webproperty_by_language('English'),
    sub_webproperty_name= 'Philippines',
    effective_date=       config.EARLIEST_PHILIPPINES_REPORT_DATE
))

# Dhaka report filters:

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~142113|002655|170451|184336|152049|150111|173249|162835|092323|161552|180321|160504',
               ga.PUBLICATION_DATE + '=~201607'),
    metric_keyword= 'reads', 
    report_keyword= 'dhaka', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    effective_date=   datetime.date(2016, 7, 1),
    termination_date= datetime.date(2017, 6, 30)
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~173138|030618|163746|182822|173048|170540|145221|160539|155111|165347|151226|165939',
               ga.PUBLICATION_DATE + '=~201607'),
    metric_keyword= 'reads', 
    report_keyword= 'dhaka', 
    webproperty_id= ga.get_webproperty_by_language('Bengali'),
    effective_date=   datetime.date(2016, 7, 1),
    termination_date= datetime.date(2017, 6, 30)
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~142113|002655|170451|184336|152049|150111|173249|162835|092323|161552|180321|160504',
               ga.PUBLICATION_DATE + '=~201607'),
    metric_keyword= 'reads', 
    report_keyword= 'dhakatest', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    effective_date=   datetime.date(2016, 7, 1),
    termination_date= datetime.date(2017, 6, 30)
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~173138|030618|163746|182822|173048|170540|145221|160539|155111|165347|151226|165939',
               ga.PUBLICATION_DATE + '=~201607'),
    metric_keyword= 'reads', 
    report_keyword= 'dhakatest', 
    webproperty_id= ga.get_webproperty_by_language('Bengali'),
    effective_date=   datetime.date(2016, 7, 1),
    termination_date= datetime.date(2017, 6, 30)
))

# Tamim report filters:

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~131354',
               ga.PUBLICATION_DATE + '=~20160827'),
    metric_keyword=   'reads', 
    report_keyword=   'tamim', 
    webproperty_id=   ga.get_webproperty_by_language('English'),
    effective_date=   datetime.date(2016, 8, 1),
    termination_date= datetime.date(2017, 6, 30)
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~140134',
               ga.PUBLICATION_DATE + '=~20160827'),
    metric_keyword=   'reads', 
    report_keyword=   'tamim', 
    webproperty_id=   ga.get_webproperty_by_language('Bengali'),
    effective_date=   datetime.date(2016, 8, 1),
    termination_date= datetime.date(2017, 6, 30)
))
