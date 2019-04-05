# Strings used in the Google Analytics account to customize that account for BenarNews

# definitions
DEFS = {}

# dimension code definitions (to prevent gibberish strings like 'dimension16' from being used elsewhere):
DEFS['dimensionname'] = {
    'ga:dimension1': 'Content Type',
    'ga:dimension2': 'Language',
    'ga:dimension3': 'Section',
    'ga:dimension4': 'Categories',
    'ga:dimension5': 'Featured Story',
    'ga:dimension6': 'Publication Date',
    'ga:dimension7': 'Page Title',
    'ga:dimension8': 'Page Template',
    'ga:dimension9': 'Theme',
    'ga:dimension10': 'Topic',
    'ga:dimension11': 'Objective',
    'ga:dimension12': 'Word Count',
    'ga:dimension13': 'Article UID',
    'ga:dimension14': 'Headline',
    'ga:dimension15': 'Short Headline',
    'ga:dimension16': 'Article CMS ID',
}

DEFS['dimensioncode'] = {
    DEFS['dimensionname']['ga:dimension1']: 'ga:dimension1',
    DEFS['dimensionname']['ga:dimension2']: 'ga:dimension2',
    DEFS['dimensionname']['ga:dimension3']: 'ga:dimension3',
    DEFS['dimensionname']['ga:dimension4']: 'ga:dimension4',
    DEFS['dimensionname']['ga:dimension5']: 'ga:dimension5',
    DEFS['dimensionname']['ga:dimension6']: 'ga:dimension6',
    DEFS['dimensionname']['ga:dimension7']: 'ga:dimension7',
    DEFS['dimensionname']['ga:dimension8']: 'ga:dimension8',
    DEFS['dimensionname']['ga:dimension9']: 'ga:dimension9',
    DEFS['dimensionname']['ga:dimension10']: 'ga:dimension10',
    DEFS['dimensionname']['ga:dimension11']: 'ga:dimension11',
    DEFS['dimensionname']['ga:dimension12']: 'ga:dimension12',
    DEFS['dimensionname']['ga:dimension13']: 'ga:dimension13',
    DEFS['dimensionname']['ga:dimension14']: 'ga:dimension14',
    DEFS['dimensionname']['ga:dimension15']: 'ga:dimension15',
    DEFS['dimensionname']['ga:dimension16']: 'ga:dimension16',
}

# metric code definitions
DEFS['metricname'] = {
    'ga:metric1': 'Comments',
    'ga:metric2': 'Newsletter Subscriptions',
    'ga:metric3': 'Emails Sent',
    'ga:metric4': 'News Submissions',
}

DEFS['metriccode'] = {
    DEFS['metricname']['ga:metric1']: 'ga:metric1',
    DEFS['metricname']['ga:metric2']: 'ga:metric2',
    DEFS['metricname']['ga:metric3']: 'ga:metric3',
    DEFS['metricname']['ga:metric4']: 'ga:metric4',
}

# dimension constants (redundant, but more readable than DEFS['dimensioncode']['Dimension Name']):
CONTENT_TYPE = DEFS['dimensioncode']['Content Type']
LANGUAGE = DEFS['dimensioncode']['Language']
SECTION = DEFS['dimensioncode']['Section']
CATEGORIES = DEFS['dimensioncode']['Categories']
FEATURED_STORY = DEFS['dimensioncode']['Featured Story']
PUBLICATION_DATE = DEFS['dimensioncode']['Publication Date']
PAGE_TITLE = DEFS['dimensioncode']['Page Title']
PAGE_TEMPLATE = DEFS['dimensioncode']['Page Template']
THEME = DEFS['dimensioncode']['Theme']
TOPIC = DEFS['dimensioncode']['Topic']
OBJECTIVE = DEFS['dimensioncode']['Objective']
WORD_COUNT = DEFS['dimensioncode']['Word Count']
ARTICLE_UID = DEFS['dimensioncode']['Article UID']
HEADLINE = DEFS['dimensioncode']['Headline']
SHORT_HEADLINE = DEFS['dimensioncode']['Short Headline']
ARTICLE_CMSID = DEFS['dimensioncode']['Article CMS ID']

# a duplicate of the dictionary in core.vocabulary.py, added as a workaround for circular imports in other files
WEBPROPERTIES = {
    'UA-61666183-15': {
        'enviro': 'prod',
        'language': 'Totals',
        'total': True,
        'report_order': 5,
    },
    'UA-61666183-6': {
        'enviro': 'prod',
        'language': 'English',
        'total': False,
        'report_order': 0,
    },
    'UA-61666183-10': {
        'enviro': 'prod',
        'language': 'Indonesian',
        'total': False,
        'report_order': 1,
    },
    'UA-61666183-9': {
        'enviro': 'prod',
        'language': 'Malaysian',
        'total': False,
        'report_order': 2,
    },
    'UA-61666183-8': {
        'enviro': 'prod',
        'language': 'Thai',
        'total': False,
        'report_order': 3,
    },
    'UA-61666183-7': {
        'enviro': 'prod',
        'language': 'Bengali',
        'total': False,
        'report_order': 4,
    },
}

# a duplicate of the function in core.vocabulary.py, added as a workaround for circular imports in other files
def get_webproperty_by_language(language):
    for key, value in WEBPROPERTIES.items():
        if language == value['language']:
            return key
    raise NotInVocabularyError("A web property for language '%s'" % language)
