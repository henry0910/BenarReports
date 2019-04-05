from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from rfa_test_tables import metadata_twitter_post, metric_lifetime_twitter_post, metric_quarterly_summary,\
                mapping_link_rfapage, mapping_cmsid_rfapage, metadata_rfapage, metadata_report
import pandas as pd
import helper_function
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


class Twitter(object):

    def __init__(self, latest_snapshot_time, previous_snapshot_time, first_day_of_report_period,
                 last_day_of_report_period, report_year, report_quarter, program, lang, environment="prod"):
        engine = get_engine(environment)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
        self.latest_snapshot_time = latest_snapshot_time
        self.previous_snapshot_time = previous_snapshot_time
        self.first_day_of_report_period = first_day_of_report_period
        self.last_day_of_report_period = last_day_of_report_period
        self.report_year = report_year
        self.report_quarter = report_quarter
        self.program = program
        self.lang = lang

    def twitter_metric_table(self):
        a = self.session.query(metadata_twitter_post).\
            filter(and_(metadata_twitter_post.postdate >= self.first_day_of_report_period,
                        metadata_twitter_post.postdate <= self.last_day_of_report_period))
        data_a = pd.read_sql(a.statement, self.session.bind)
        b = self.session.query(metric_lifetime_twitter_post)
        data_b = pd.read_sql(b.statement, self.session.bind)
        data_a = data_a.add_prefix("a.")
        data_b = data_b.add_prefix("b.")
        data = pd.merge(data_a, data_b, left_on="a.postid", right_on="b.postid", how="inner")
        data = data[["a.postid", "a.service", "a.postdate",
                     "b.views", "b.likes", "b.retweets",
                     "b.clicks", "b.csv_export_time"]]
        helper_function.df_rename(data)
        return data

    def twitter_metric_by_lang(self):
        data = self.twitter_metric_table()
        data = data[["service", "views", "likes", "retweets", "clicks"]]
        data = data.groupby(by=["service"]).sum()
        return data

    def twitter_csv_export_time(self):
        a = self.session.query(metric_lifetime_twitter_post)
        data = pd.read_sql(a.statement, self.session.bind)
        res = []
        for i in data["csv_export_time"]:
            if i not in res:
                res.append(i)
        return res

    def twitter_metric_by_theme(self):
        data = self.twitter_data_post_quarterly()
        data = data[["theme", "views", "likes", "retweets", "clicks"]]
        return data.groupby("theme").sum()

    def twitter_metric_by_objective(self):
        data1 = self.twitter_data_post_quarterly()
        data2 = self.twitter_data_post_quarterly()
        data3 = self.twitter_data_post_quarterly()
        data1 = data1[["objective1", "views", "likes", "retweets", "clicks"]]
        data2 = data2[["objective2", "views", "likes", "retweets", "clicks"]]
        data3 = data3[["objective3", "views", "likes", "retweets", "clicks"]]
        data1 = data1.rename(columns={"objective1": "objective"})
        data2 = data2.rename(columns={"objective2": "objective"})
        data3 = data3.rename(columns={"objective3": "objective"})
        data = pd.concat([data1, data2, data3])
        return data.groupby("objective").sum()

    def twitter_top_shared_post(self):
        data = self.twitter_data_post_quarterly()
        data = data.sort_values(by=["retweets"], ascending=False)
        return data

    def twitter_data_post_quarterly(self):
        data = helper_function.twitter_expanded_data_post_quarterly(self.latest_snapshot_time, 
                                                                    self.previous_snapshot_time, 
                                                                    self.first_day_of_report_period)
        return data

    def twitter_top_five_items(self):
        data = self.twitter_data_post_quarterly()
        data = data[data["program"] == "VEO"]
        data = data[["headline", "service", "pubdate",
                                 "retweets", "likes", "views",
                                 "media_type", "permalink", "rfa_link"]]
        data = data.sort_values(by=["retweets"], ascending=False)
        return data

    def twitter_metric(self, metric):
        a = self.session.query(metric_quarterly_summary).\
            filter(and_(metric_quarterly_summary.metric == metric,
                        metric_quarterly_summary.year == self.report_year,
                        metric_quarterly_summary.quarter == self.report_quarter))
        data = pd.read_sql(a.statement, self.session.bind)
        return sum(data["value"])


    def twitter_complete_data(self):
        a = self.session.query(metric_lifetime_twitter_post)
        b = self.session.query(metadata_twitter_post)
        c = self.session.query(mapping_link_rfapage)
        d = self.session.query(mapping_cmsid_rfapage)
        e = self.session.query(metadata_rfapage)
        data_a = pd.read_sql(a.statement, self.session.bind)
        data_b = pd.read_sql(b.statement, self.session.bind)
        data_c = pd.read_sql(c.statement, self.session.bind)
        data_d = pd.read_sql(d.statement, self.session.bind)
        data_e = pd.read_sql(e.statement, self.session.bind)
        pass

    def twitter_summary(self):
        metric = ["Twitter: New Followers", "Twitter: Views",
                  "Twitter: Tweets via Benarnews.org",
                  "Twitter: Retweets", "Twitter: URL Clicks"]
        data = pd.DataFrame(columns=['Total', str(self.report_year) + '-' + str(self.report_quarter)], index=metric)
        for m in metric:
            total = sum(helper_function.summary_total(m)['value'])
            quarter = self.twitter_metric(m)
            data.loc[m] = [total, quarter]
        return data

    def twitter_summary_prc(self):
        metric = ["Twitter: Views", "Twitter: Retweets", "Twitter: URL Clicks"]
        df = pd.DataFrame(columns=['Total', str(self.report_year) + '-' + str(self.report_quarter)], index=metric)
        a = self.session.query(metadata_report)
        report_time = pd.read_sql(a.statement, self.session.bind)
        first_day = [i for i in report_time['first_day']]
        tw_previous_snapshot = [i for i in report_time['initial_tw_snapshot']]
        tw_latest_snapshot = [i for i in report_time['final_tw_snapshot']]
        total_views = 0
        total_clicks = 0
        total_retweets = 0
        for i in range(0, len(first_day)):
            data = helper_function.twitter_expanded_data_post_quarterly(str(tw_latest_snapshot[i]),
                                                                        str(tw_previous_snapshot[i]),
                                                                        str(first_day[i]))
            data = data[data["program"] == 'PRC']
            total_views += sum(data["views"])
            total_clicks += sum(data["clicks"])
            total_retweets += sum(data["retweets"])
        data_curr = self.twitter_data_post_quarterly()
        data_curr = data_curr[data_curr["program"] == 'PRC']
        curr_views = sum(data_curr["views"])
        curr_clicks = sum(data_curr["clicks"])
        curr_retweets = sum(data_curr["retweets"])
        df.iloc[0] = [total_views, curr_views]
        df.iloc[1] = [total_retweets, curr_retweets]
        df.iloc[2] = [total_clicks, curr_clicks]
        return df

    def twitter_summary_veo(self):
        data_all = self.twitter_summary()
        data_prc = self.twitter_summary_prc()
        return data_prc, data_all