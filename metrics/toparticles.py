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


# version 1 (join queries)

join1_base = GAQueryBase(
    dimensions='%s,%s,%s,%s' % (ga.ARTICLE_UID, ga.HEADLINE, ga.PUBLICATION_DATE, 'ga:pagePath'),
    metrics='ga:pageviews',
    max_results=150,  # needs lots of extra rows in order to map properly to Facebook data
    sort='-ga:pageviews',
    filters=fil.ARTICLE_AND_SLIDESHOW_READS,
    view_name_includes='Report Data'
)

join2_base = GAQueryBase(
    dimensions='%s,%s' % (ga.ARTICLE_UID, ga.ARTICLE_CMSID),
    metrics='ga:pageviews',
    max_results=150, # needs lots of extra rows in order to map properly to Facebook data
    sort='-ga:pageviews',
    filters=fil.ARTICLE_AND_SLIDESHOW_READS,
    view_name_includes='Report Data',
    comment='''CMS ID is a separate join, because it was only recently
added to Google Analytics, and some stories won't have it.'''
)

# version 1 (main query)

main_base = GAQueryBase(
    dimensions='%s,%s' % (ga.ARTICLE_UID, ga.LANGUAGE),
    metrics='ga:pageviews',
    # max_results needs to be very high for three reasons:
    # 1) In DataQualityReports, the Totals metric must cover the top 10
    #    articles for each language, even if the least-read language's top 10
    #    are low in the overall list.
    # 2) When mapping articles, FacebookLinkMapper may report top shared
    #    articles that got relatively few reads.
    # 3) Grouping data across ReportSegments.
    max_results=150,
    sort='-ga:pageviews',
    filters=fil.ARTICLE_AND_SLIDESHOW_READS_Y15,
    view_name_includes='Report Data',
    comment='''In the reports, the section title is 'Top 10 Articles Read',
but management decided slideshows are worth including here
as well as in the 'Top 10 Items Shared' section. We just
forgot to change the title of the former section.

Total reads of slideshows are still tracked in a separate
metric, as seen in the summary stats - hence the use of
different GA query filters between this and the
Article Reads query.

Warning: any metric that uses Article UID cannot be used to
collect data before September 2015, because UIDs were
implemented in August.'''
)

CONTAINER.add(GAQueryDefinition(main_base, 'toparticles', 
    title=                 'Top 10 Read Articles',
    effective_date=        config.EARLIEST_REPORT_DATE,
    termination_date=      datetime.date(2016, 5, 31),
    join_queries=          [join1_base, join2_base],
    mysql_table=           config.ARTICLE_METRIC_TABLE,
    metric_index=          2,
    show_rows=             True,
    has_row_sum=           False,
    has_webproperty_sum=   False,
    has_report_tables=     True,
    max_rows_to_print=     10,
    include_total=         False
))

# version 2

main_base = copy.deepcopy(main_base)
main_base.filters = fil.ARTICLE_AND_SLIDESHOW_READS

CONTAINER.add(GAQueryDefinition(main_base, 'toparticles', 
    title='Top 10 Read Articles',
    effective_date=   datetime.date(2016, 6, 1),
    termination_date= datetime.date(2017, 6, 30),
    join_queries=     [join1_base, join2_base],
#    group_by=         ga.ARTICLE_UID,
    mysql_table=      config.ARTICLE_METRIC_TABLE,
    metric_index=     2,
    show_rows=        True,
    has_row_sum=      False,
    has_webproperty_sum=False,
    has_report_tables=True,
    max_rows_to_print=10,
    include_total=False
))

# version 3

join_base = GAQueryBase(
    dimensions='%s,%s,%s,%s' % (ga.ARTICLE_CMSID, ga.HEADLINE, ga.PUBLICATION_DATE, 'ga:pagePath'),
    metrics='ga:pageviews',
    sort='-ga:pageviews',
    filters=fil.ARTICLE_AND_SLIDESHOW_READS,
    view_name_includes='Report Data'
)


main_base = GAQueryBase(
    dimensions=ga.ARTICLE_CMSID,
    metrics='ga:pageviews',
    sort='-ga:pageviews',
    filters=fil.ARTICLE_AND_SLIDESHOW_READS,
    max_results=150,
    view_name_includes='Report Data'
)

CONTAINER.add(GAQueryDefinition(main_base, 'toparticles', 
    title=               'Top 10 Read Articles',
    effective_date=      datetime.date(2017, 7, 1),
    join_queries=        [join_base],
    mysql_table=         config.ARTICLE_METRIC_TABLE,
    metric_index=        2,
    show_rows=           True,
    has_row_sum=         False,
    has_webproperty_sum= False,
    has_report_tables=   True,
    max_rows_to_print=   10,
    include_total=       False,
    adjust_for_uncategorized_articles=True
))


# Philippines sub-webproperty filters:

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '=~philippine',
    metric_keyword= 'toparticles', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='Philippines',
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    ga.SECTION + '!~philippine',
    metric_keyword= 'toparticles', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    sub_webproperty_name='English',
    effective_date=config.EARLIEST_PHILIPPINES_REPORT_DATE
))

# Dhaka report filters:

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~142113|002655|170451|184336|152049|150111|173249|162835|092323|161552|180321|160504',
               ga.PUBLICATION_DATE + '=~201607'),
    metric_keyword= 'toparticles', 
    report_keyword= 'dhaka', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    effective_date=   datetime.date(2016, 7, 1),
    termination_date= datetime.date(2017, 6, 30)
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~173138|030618|163746|182822|173048|170540|145221|160539|155111|165347|151226|165939',
               ga.PUBLICATION_DATE + '=~201607'),
    metric_keyword= 'toparticles', 
    report_keyword= 'dhaka', 
    webproperty_id= ga.get_webproperty_by_language('Bengali'),
    effective_date=   datetime.date(2016, 7, 1),
    termination_date= datetime.date(2017, 6, 30)
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~142113|002655|170451|184336|152049|150111|173249|162835|092323|161552|180321|160504',
               ga.PUBLICATION_DATE + '=~201607'),
    metric_keyword= 'toparticles', 
    report_keyword= 'dhakatest', 
    webproperty_id= ga.get_webproperty_by_language('English'),
    effective_date=   datetime.date(2016, 7, 1),
    termination_date= datetime.date(2017, 6, 30)
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~173138|030618|163746|182822|173048|170540|145221|160539|155111|165347|151226|165939',
               ga.PUBLICATION_DATE + '=~201607'),
    metric_keyword= 'toparticles', 
    report_keyword= 'dhakatest', 
    webproperty_id= ga.get_webproperty_by_language('Bengali'),
    effective_date=   datetime.date(2016, 7, 1),
    termination_date= datetime.date(2017, 6, 30)
))

# Tamim report filters:

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~131354',
               ga.PUBLICATION_DATE + '=~20160827'),
    metric_keyword=   'toparticles', 
    report_keyword=   'tamim', 
    webproperty_id=   ga.get_webproperty_by_language('English'),
    effective_date=   datetime.date(2016, 8, 1),
    termination_date= datetime.date(2017, 6, 30)
))

CONTAINER.custom_filters.append(CustomQueryFilter(
    '%s;%s' % (ga.ARTICLE_UID + '=~140134',
               ga.PUBLICATION_DATE + '=~20160827'),
    metric_keyword=   'toparticles', 
    report_keyword=   'tamim', 
    webproperty_id=   ga.get_webproperty_by_language('Bengali'),
    effective_date=   datetime.date(2016, 8, 1),
    termination_date= datetime.date(2017, 6, 30)
))