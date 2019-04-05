from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from rfa_test_tables import metric_daily_facebook_page, metric_lifetime_facebook_post
import pandas as pd
from helper_function import df_rename, summary_total, facebook_expanded_data_post_quarterly
from rfa_query.config import DATABASE_CONFIG
from tests.config_test import DATABASE_TEST_CONFIG


def get_engine(environment):
    if environment == 'test':
        host = DATABASE_TEST_CONFIG['host']
        dbname = DATABASE_TEST_CONFIG['dbname']
        user = DATABASE_TEST_CONFIG['user']
        password = DATABASE_TEST_CONFIG['password']
        port = DATABASE_TEST_CONFIG['port']
    else:
        host = DATABASE_CONFIG['host']
        dbname = DATABASE_CONFIG['dbname']
        user = DATABASE_CONFIG['user']
        password = DATABASE_CONFIG['password']
        port = DATABASE_CONFIG['port']

    connnect_str = "mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host, port, dbname)
    engine = create_engine(connnect_str, echo=True)
    return engine


class Facebook(object):
    def __init__(self, latest_snapshot_time, previous_snapshot_time, first_day_of_report_period,
                 last_day_of_report_period, report_year, last_year,
                 report_quarter, last_quarter, program, lang, environment='prod'):

        engine = get_engine(environment)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.latest_snapshot_time = latest_snapshot_time
        self.previous_snapshot_time = previous_snapshot_time
        self.first_day_of_report_period = first_day_of_report_period
        self.last_day_of_report_period = last_day_of_report_period
        self.report_year = report_year
        self.last_year = last_year
        self.report_quarter = report_quarter
        self.last_quarter = last_quarter
        self.program = program
        self.lang = lang

    def facebook_metric_daily_page_quarterly(self):
        a = self.session.query(metric_daily_facebook_page).\
            filter(and_(metric_daily_facebook_page.date >= self.first_day_of_report_period,
                        metric_daily_facebook_page.date <= self.last_day_of_report_period))
        data = pd.read_sql(a.statement, self.session.bind)
        return data

    def facebook_metric_daily_table(self):
        data = self.facebook_metric_daily_page_quarterly()
        data = data.groupby("language").sum()
        return data

    def facebook_csv_export_time(self):
        cet = self.session.query(metric_lifetime_facebook_post)
        data_cet = pd.read_sql(cet.statement, self.session.bind)
        data_cet["csv_export_time"].unique()
        return data_cet["csv_export_time"].unique()

    def facebook_total_profile_likes_by_lang(self):
        a = self.session.query(metric_daily_facebook_page). \
            filter(metric_daily_facebook_page.date == self.last_day_of_report_period)
        data = pd.read_sql(a.statement, self.session.bind)
        data = data[["language", "likes"]]
        return data.groupby("language").sum()

    def facebook_news_profile_likes_by_lang(self):
        a = self.session.query(metric_daily_facebook_page).\
            filter(metric_daily_facebook_page.date == self.last_day_of_report_period)
        data_a = pd.read_sql(a.statement, self.session.bind)
        b = self.session.query(metric_daily_facebook_page).\
            filter(metric_daily_facebook_page.date == self.first_day_of_report_period)
        data_b = pd.read_sql(b.statement, self.session.bind)
        data_a = data_a.add_prefix('a.')
        data_b = data_b.add_prefix("b.")
        data = pd.merge(data_a, data_b, left_on="a.language", right_on="b.language", how="inner")
        data["new_likes"] = data["a.likes"] - data["b.likes"]
        data = data[["a.language", "a.date", "new_likes"]]
        df_rename(data)
        return data

    def facebook_metric_by_objective(self):
        data1 = self.facebook_data_post_quarterly()
        data2 = self.facebook_data_post_quarterly()
        data3 = self.facebook_data_post_quarterly()
        data1 = data1[["objective1", "views", "shares", "likes", "comments", "clicks"]]
        data2 = data2[["objective2", "views", "shares", "likes", "comments", "clicks"]]
        data3 = data3[["objective3", "views", "shares", "likes", "comments", "clicks"]]
        data1 = data1.rename(columns={"objective1": "objective"})
        data2 = data2.rename(columns={"objective2": "objective"})
        data3 = data3.rename(columns={"objective3": "objective"})
        data = pd.concat([data1, data2, data3])
        return data.groupby("objective").sum()

    def facebook_metric_by_theme(self):
        data = self.facebook_data_post_quarterly()
        data = data[["theme", "views", "shares", "clicks", "comments", "likes"]]
        return data.groupby("theme").sum()

    def facebook_top_shared_post(self):
        data = self.facebook_data_post_quarterly()
        data["likes_shares"] = data["likes"] + data["shares"]
        data = data.sort_values(by=["likes_shares"], ascending=False)
        return data

    def facebook_data_post_quarterly(self):
        data = facebook_expanded_data_post_quarterly(self.latest_snapshot_time,
                                                     self.previous_snapshot_time,
                                                     self.first_day_of_report_period)
        return data

    def facebook_top_five_items(self):
        data = self.facebook_data_post_quarterly()
        data = data[["headline", "pubdate", "likes",
                    "shares", "views", "media_type",
                     "program", "service", "permalink", "rfa_link"]]
        data['likes_shares'] = data['likes'] + data['shares']
        data = data[data["program"] == "VEO"]
        df_english = data[data["service"] == "English"]
        df_bengali = data[data["service"] == "Bengali"]
        df_indo = data[data["service"] == "Indonesian"]
        df_thai = data[data["service"] == "Thai"]
        df_phi = data[data["service"] == "Philippines"]
        df_may = data[data["service"] == "Malaysian"]
        return df_english, df_bengali, df_indo, df_thai, df_phi, df_may

    def facebook_summary(self):
        metric = ['Facebook: New Profile Likes', 'Facebook: Views of Content',
                  'Facebook: URL Clicks', 'Facebook: Comments']
        data = pd.DataFrame(columns=['Total', str(self.report_year) + '-' + str(self.report_quarter)], index=metric)
        for m in metric:
            if m == 'Facebook: New Profile Likes':
                total = sum(self.facebook_total_profile_likes_by_lang()['likes'])
                quarter = sum(self.facebook_news_profile_likes_by_lang()['new_likes'])
            elif m.find('Views') != -1:
                total = sum(summary_total(m)['value'])
                quarter = sum(self.facebook_metric_daily_page_quarterly()['views'])
            elif m.find('Clicks') != -1:
                total = sum(summary_total(m)['value'])
                quarter = sum(self.facebook_metric_daily_page_quarterly()['clicks'])
            else:
                total = sum(summary_total(m)['value'])
                quarter = sum(self.facebook_metric_daily_page_quarterly()['comments'])
            data.loc[m] = [total, quarter]
        return data

    def facebook_summary_by_program(self):
        pass
