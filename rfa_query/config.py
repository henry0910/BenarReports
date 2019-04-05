# Change configuration here # 

DATABASE_CONFIG = {
    'host': '172.31.1.74',
    'dbname': 'rfa_analytics',
    'user': 'shent',
    'password': 'newshoes!',
    'port': '3306'
}


REPORT_DATE_CONFIG = {
    'report_year': 2019,
    'last_year': 2018,
    'report_quarter': 1,
    "last_quarter": 4,
    'program': 'VEO',
    "lang": "English"
}

FACEBOOK_REPORT_CONFIG = {
    'latest_snapshot_time': '2019-03-18 11:00:00',
    'previous_snapshot_time': '2018-12-17 11:00:00',
    'first_day_of_report_period': '2018-12-16',
    'last_day_of_report_period': '2019-03-15',
    'keyword': 'fbposts'
}

# #
RFAPAGE_REPORT_CONFIG = {
    'metric': 'reads',
    'platform': 'benarnews.org',
    'keyword': 'summarystatisticsbyprogram'
}

# #

TWITTER_REPORT_CONFIG = {
    'latest_snapshot_time': '2019-03-18 13:00:00',
    'previous_snapshot_time': '2018-12-17 10:00:00',
    'first_day_of_report_period': '2018-12-15',
    'last_day_of_report_period': '2019-03-15',
    'keyword': 'twmetricbylang'
}

TWITTER_PARSER = {
    'time': '2018-07-11'
}
