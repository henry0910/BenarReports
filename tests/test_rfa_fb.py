
import unittest
from rfa_analytics.rfa_analytics_facebook import Facebook
from config_test import FACEBOOK_TEST

latest_snapshot_time = FACEBOOK_TEST["latest_snapshot_time"]
previous_snapshot_time = FACEBOOK_TEST["previous_snapshot_time"]
first_day_of_report_period = FACEBOOK_TEST["first_day_of_report_period"]
last_day_of_report_period = FACEBOOK_TEST["last_day_of_report_period"]
report_year = FACEBOOK_TEST["report_year"]
report_quarter = FACEBOOK_TEST["report_quarter"]
last_year = FACEBOOK_TEST["last_year"]
last_quarter = FACEBOOK_TEST["last_quarter"]
program = FACEBOOK_TEST["program"]
lang = FACEBOOK_TEST["lang"]


class TestFbMethods(unittest.TestCase):

    def setUp(self):
        self.latest_snapshot_time = latest_snapshot_time
        self.previous_snapshot_time = previous_snapshot_time
        self.first_day_of_report_period = first_day_of_report_period
        self.last_day_of_report_period = last_day_of_report_period
        self.report_year = report_year
        self.report_quarter = report_quarter
        self.last_year = last_year
        self.last_quarter = last_quarter
        self.program = program
        self.lang = lang
        self.fb_test = Facebook(latest_snapshot_time, previous_snapshot_time,
                                first_day_of_report_period, last_day_of_report_period,
                                report_year, last_year, report_quarter, last_quarter, program,
                                lang)

    def tearDown(self):
        pass

    def test_facebook_total_profile_metric_by_lang(self):
        result = self.fb_test.facebook_total_profile_metric_by_lang()
        for index, row in result.iterrows():
            if index == 'Bengali':
                self.assertAlmostEqual(row['likes'], 19927196)
                self.assertAlmostEqual(row['views'], 55495503)
                self.assertAlmostEqual(row['clicks'], 1327266)
                self.assertAlmostEqual(row['comments'], 23276)

    def test_facebook_metric_daily_table(self):
        result = self.fb_test.facebook_metric_daily_table()
        for index, row in result.iterrows():
            if index == 'English':
                self.assertAlmostEqual(row['likes'], 1094085)
                self.assertAlmostEqual(row['views'], 17599798)
                self.assertAlmostEqual(row['clicks'], 129730)
                self.assertAlmostEqual(row['comments'], 1595)

    def test_facebook_data_post_quarterly(self):
        result = self.fb_test.facebook_data_post_quarterly()
        self.assertEqual(len(result), 1844)

    def test_facebook_metric_by_theme(self):
        result = self.fb_test.facebook_metric_by_theme()
        for index, row in result.iterrows():
            if index == 'Anti-Crime':
                self.assertEqual(row['views'], 3027051)
                self.assertEqual(row['shares'], 314)
                self.assertEqual(row['clicks'], 133628)
                self.assertEqual(row['comments'], 271)
                self.assertEqual(row['likes'], 24746)

    # def test_facebook_csv_export_time(self):
    #     result = self.fb_test.facebook_csv_export_time()
    #     self.assertGreater(len(result), 20)
    #
    # def test_facebook_top_shared_post(self):
    #     result = self.fb_test.facebook_top_shared_post()
    #     max_likes_shares = max(result["likes_shares"])
    #     self.assertEqual(max_likes_shares, 100440)
    #
    # def test_facebook_data_post_quarterly(self):
    #     result = self.fb_test.facebook_data_post_quarterly()
    #     self.assertEqual(len(result.index), 2916)
    #


if __name__ == '__main__':
    unittest.main()
