import sys, os
METRICS_DIR = os.path.realpath('')
sys.path.append(METRICS_DIR + '/core')
sys.path.append(METRICS_DIR + '/profiles')
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import googleanalytics.metric_strings as ga
import profiles.profile_filter_strings as pfil

##############################
## Filter Terms             ##
##############################
# =~ (matches regex)
# !~ (does not match regex)
# , (or - precedes 'and' in order of operations)
# ; (and)
##############################
## Sort Terms              ##
##############################
# - (descending sort)

# filter components:
CTYPE_ARTICLE = ga.CONTENT_TYPE + '==article'
CTYPE_VIDEO = ga.CONTENT_TYPE + '=~Video'
ARTICLE_AND_SLIDESHOW = ga.SECTION + '!~about'
ARTICLE_NOT_SLIDESHOW = ARTICLE_AND_SLIDESHOW + '|slide|galeri-foto'
SLIDESHOW_NOT_ARTICLE = ga.SECTION + '=~slide|galeri-foto'
PATH_NOT_UNDEFINED = 'ga:pagePath!~/undefined$'
# path to a content page (i.e. not a form)
PATH_TO_CONTENT = PATH_NOT_UNDEFINED + '|_form$|_form/|_form\?'
# one path per article: used to calculate Facebook share button metrics
ONE_PATH_PER_ARTICLE = PATH_TO_CONTENT + '|html/|html\?|^/search|^/translate'

# sub-webproperty filter components
SUBWEBPROPERTY_REGEX = '|'.join(pfil.SUBWEBPROPERTIES)
ARTICLE_NOT_SLIDESHOW_SUBWEBPROPERTY = ';'.join((ARTICLE_NOT_SLIDESHOW, '%s=~%s' % (ga.SECTION, SUBWEBPROPERTY_REGEX)))
ARTICLE_NOT_SLIDESHOW_NOR_SUBWEBPROPERTY = '%s|%s' % (ARTICLE_NOT_SLIDESHOW, SUBWEBPROPERTY_REGEX)

# legacy filters (not used for current reports):
PATH_TO_CONTENT_LAUNCH = PATH_NOT_UNDEFINED # replaced by PATH_TO_CONTENT as of November 2015
PATH_TO_CONTENT_Y15 = PATH_NOT_UNDEFINED + '|_form$' # replaced by PATH_TO_CONTENT as of November 2015
ARTICLE_AND_SLIDESHOW_READS_Y15 = ';'.join((CTYPE_ARTICLE, ARTICLE_AND_SLIDESHOW, PATH_TO_CONTENT_Y15))
# yes, for some reason the new PATH_TO_CONTENT is more accurate for old reads by topic
OLD_READS_BY_TOPIC = ';'.join((PATH_TO_CONTENT, pfil.PRODUCTION_HOST, pfil.NEWS_PAGE))
READS_V1 = ';'.join((CTYPE_ARTICLE, ARTICLE_NOT_SLIDESHOW, PATH_TO_CONTENT_LAUNCH))
READS_V2 = ';'.join((CTYPE_ARTICLE, ARTICLE_NOT_SLIDESHOW, PATH_TO_CONTENT_Y15))

# current filters:
READS_V3 = ';'.join((CTYPE_ARTICLE, ARTICLE_NOT_SLIDESHOW, PATH_TO_CONTENT))
READS_V3_PHIL = ';'.join((CTYPE_ARTICLE, ARTICLE_NOT_SLIDESHOW_SUBWEBPROPERTY, PATH_TO_CONTENT))
READS_V3_NONPHIL = ';'.join((CTYPE_ARTICLE, ARTICLE_NOT_SLIDESHOW_NOR_SUBWEBPROPERTY, PATH_TO_CONTENT))
ARTICLE_AND_SLIDESHOW_READS = ';'.join((CTYPE_ARTICLE, ARTICLE_AND_SLIDESHOW, PATH_TO_CONTENT))
ARTICLE_AND_SLIDESHOW_LIST = ';'.join((CTYPE_ARTICLE, ARTICLE_AND_SLIDESHOW, ONE_PATH_PER_ARTICLE))

VISITOR_COUNTRIES = 'ga:country=~%s' % ',ga:country=~'.join('|'.join(i) for i in pfil.VISITOR_COUNTRIES)
