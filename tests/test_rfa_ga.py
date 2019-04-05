import unittest
from rfa_analytics.rfa_analytics_rfapage import Rfa
from config_test import RFAPAGE_TEST

report_year = RFAPAGE_TEST["report_year"]
report_quarter = RFAPAGE_TEST["report_quarter"]
last_year = RFAPAGE_TEST["last_year"]
last_quarter = RFAPAGE_TEST["last_quarter"]
program = RFAPAGE_TEST["program"]
rfa_metric = RFAPAGE_TEST["metric"]
rfa_platform = RFAPAGE_TEST["platform"]


class TestGaMethods(unittest.TestCase):

    def setUp(self):
        self.report_year = report_year
        self.report_quarter = report_quarter
        self.last_year = last_year
        self.last_quarter = last_quarter
        self.program = program
        self.rfa_metric = rfa_metric
        self.rfa_platform = rfa_platform
        self.rfa_test = Rfa(report_year, last_year, report_quarter, last_quarter,
                            program, rfa_metric, rfa_platform)

    def tearDown(self):
        pass

    def test_rfa_data_post_quarterly(self):
        result = self.rfa_test.rfapage_data_post_quarterly()
        self.assertEqual(len(result), 8197)

    def test_rfa_by_lang_by_program(self):
        result = self.rfa_test.rfapage_by_lang_by_program()
        for index, row in result[0].iterrows():
            if index == 'English':
                self.assertEqual(row['value'], 132447)
            if index == 'Thai':
                self.assertEqual(row['value'], 62279)

    def test_rfa_by_theme_by_program(self):
        result = self.rfa_test.rfapage_by_theme_by_program()
        for index, row in result[0].iterrows():
            if index == 'Anti-Crime':
                self.assertEqual(row['value'], 44729)
            if index == 'Border Security':
                self.assertEqual(row['value'], 6118)


if __name__ == "__main__":
    unittest.main()
