import unittest
from rfa_analytics.rfa_analytics_twitter import Twitter
from config_test import TWITTER_TEST

latest_snapshot_time = TWITTER_TEST["latest_snapshot_time"]
previous_snapshot_time = TWITTER_TEST["previous_snapshot_time"]
first_day_of_report_period = TWITTER_TEST["first_day_of_report_period"]
last_day_of_report_period = TWITTER_TEST["last_day_of_report_period"]
report_year = TWITTER_TEST["report_year"]
report_quarter = TWITTER_TEST["report_quarter"]
last_year = TWITTER_TEST["last_year"]
last_quarter = TWITTER_TEST["last_quarter"]
program = TWITTER_TEST["program"]
lang = TWITTER_TEST["lang"]


class TestTwMethods(unittest.TestCase):

    def setUp(self):
        self.latest_snapshot_time = latest_snapshot_time
        self.previous_snapshot_time = previous_snapshot_time
        self.first_day_of_report_period = first_day_of_report_period
        self.last_day_of_report_period = last_day_of_report_period
        self.report_year = report_year
        self.report_quarter = report_quarter
        self.program = program
        self.lang = lang
        self.tw_test = Twitter(latest_snapshot_time, previous_snapshot_time,
                               first_day_of_report_period, last_day_of_report_period,
                               report_year, report_quarter, program, lang)

    def tearDown(self):
        pass

    def test_twitter_metric_table(self):
        result = self.tw_test.twitter_metric_table()
        self.assertEqual(len(result), 3549)

    def test_twitter_metric_by_lang(self):
        result = self.tw_test.twitter_metric_by_lang()
        for index, row in result.iterrows():
            if index == "English":
                self.assertEqual(row["views"], 378370)
                self.assertEqual(row['likes'], 426)
                self.assertEqual(row['retweets'], 1604)
                self.assertEqual(row['clicks'], 1990)

    def test_twitter_data_post_quarterly(self):
        result = self.tw_test.twitter_data_post_quarterly()
        self.assertEqual(len(result), 1897)

    def test_twitter_metric_by_theme(self):
        result = self.tw_test.twitter_metric_by_theme()
        for index, row in result.iterrows():
            if index == 'Anti-Crime':
                self.assertEqual(row['views'], 22136)
            if index == 'Human Rights':
                self.assertEqual(row['views'], 53226)

    def test_twitter_top_five_items(self):
        result = self.tw_test.twitter_top_five_items()
        self.assertEqual(max(result['retweets']), 45)


if __name__ == '__main__':
    unittest.main()
