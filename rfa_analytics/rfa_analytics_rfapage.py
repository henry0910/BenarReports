import pandas as pd
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tests.config_test import DATABASE_TEST_CONFIG
from rfa_query.config import DATABASE_CONFIG
from helper_function import df_rename, metric_summary, summary_total
from rfa_test_tables import mapping_theme_objective, metadata_rfapage, metric_quarterly_by_item


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


class Rfa(object):

    def __init__(self, report_year, last_year, report_quarter, last_quarter, program, metric, platform,
                 environment='prod'):
        engine = get_engine(environment)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.report_year = report_year
        self.last_year = last_year
        self.report_quarter = report_quarter
        self.last_quarter = last_quarter
        self.program = program
        self.metric = metric
        self.platform = platform

    def rfapage_data_post_quarterly(self):
        a = self.session.query(metric_quarterly_by_item).filter(and_(metric_quarterly_by_item.platform == "benarnews.org",
                                                                     metric_quarterly_by_item.year == self.report_year,
                                                                     metric_quarterly_by_item.quarter == self.report_quarter))
        b = self.session.query(metadata_rfapage)
        c = self.session.query(mapping_theme_objective)
        df_a = pd.read_sql(a.statement, self.session.bind)
        df_b = pd.read_sql(b.statement, self.session.bind)
        df_c = pd.read_sql(c.statement, self.session.bind)
        df_a = df_a.add_prefix("a.")
        df_b = df_b.add_prefix("b.")
        df_c = df_c.add_prefix("c.")
        df_ab = pd.merge(df_a, df_b, left_on="a.online_id", right_on="b.online_id", how="left")
        df_final = pd.merge(df_ab, df_c, left_on="b.theme", right_on="c.theme", how="left")
        df_final = df_final[["a.id", "a.online_id", "a.year",
                             "a.quarter", "a.service", "a.value",
                             "b.program", "b.theme", "b.media_type",
                             "b.pubdate", "b.headline", "c.objective1",
                             "c.objective2", "c.objective3"]]
        df_rename(df_final)
        return df_final

    def rfapage_by_lang_by_program(self):
        res = []
        data = self.rfapage_data_post_quarterly()
        data_prc = data[data["program"] == "PRC"]
        data_veo = data[data["program"] == "VEO"]
        data_prc = data_prc.groupby("service").sum()
        data_veo = data_veo.groupby("service").sum()
        res.append(data_veo)
        res.append(data_prc)
        return res

    def rfapage_by_theme_by_program(self):
        res = []
        data = self.rfapage_data_post_quarterly()
        data_prc = data[data["program"] == "PRC"]
        data_veo = data[data["program"] == "VEO"]
        data_prc = data_prc.groupby("theme").sum()
        data_veo = data_veo.groupby("theme").sum()
        res.append(data_veo)
        res.append(data_prc)
        return res

    def rfapage_by_objective_by_program(self):
        res = []
        data1 = self.rfapage_data_post_quarterly()
        data2 = self.rfapage_data_post_quarterly()
        data3 = self.rfapage_data_post_quarterly()
        data1 = data1[["value", "objective1", "program"]]
        data2 = data2[["value", "objective2", "program"]]
        data3 = data3[["value", "objective3", "program"]]
        program = ['VEO', 'PRC']
        for i in program:
            data1 = data1.rename(columns={"objective1": "objective"})
            data2 = data2.rename(columns={"objective2": "objective"})
            data3 = data3.rename(columns={"objective3": "objective"})
            data = pd.concat([data1, data2, data3])
            data = data[data["program"] == i]
            data = data.dropna()
            data = data.groupby("objective").sum()
            res.append(data)
        return res

    # def rfapage_summary_statistics(self):
    #     metric = ["Overall Page Views", "Article Reads", "Video Views", "Slideshow Views",
    #               "Articles Published", "Videos Published", "Slideshows Published", "Article Word Count",
    #               "Unique Visitors"]
    #     df_final = pd.DataFrame(columns=["Total", str(self.last_quarter) + "/" + str(self.last_year),
    #                             str(self.report_quarter) + "/" + str(self.report_year), "Quarterly_change"],
    #                             index=metric)
    #     for m in metric:
    #         if m != "Unique Visitors":
    #             df_total = summary_total(m)
    #             # df_total = df_total[df_total["program"] == "All"]
    #             df_last = metric_summary(self.last_year, self.last_quarter, m)
    #             # df_last = df_last[df_last["program"] == "All"]
    #             df_curr = metric_summary(self.report_year, self.report_quarter, m)
    #             # df_curr = df_curr[df_curr["program"] == "All"]
    #             total = sum(df_total["value"])
    #             last = sum(df_last["value"])
    #             curr = sum(df_curr["value"])
    #             percent = float(curr) / float(last) - 1
    #             df_final.loc[m] = [total, last, curr, percent]
    #         else:
    #             df_total = summary_total("New Visitors for running totals")
    #             df_total = df_total[df_total["service"] == "All"]
    #             df_last = metric_summary(self.last_year, self.last_quarter,
    #                                      "Unique Visitors for report period")
    #             df_last = df_last[df_last["service"] == "All"]
    #             df_curr = metric_summary(self.report_year, self.report_quarter,
    #                                      "Unique Visitors for report period")
    #             df_curr = df_curr[df_curr["service"] == "All"]
    #             total = sum(df_total["value"])
    #             last = sum(df_last["value"])
    #             curr = sum(df_curr["value"])
    #             percent = float(curr) / float(last) - 1
    #             df_final.loc[m] = [total, last, curr, percent]
    #     return df_final

    # def rfapage_summary_statistics_by_lang(self):
    #     res = []
    #     metric = ["Overall Page Views", "Article Reads", "Video Views", "Slideshow Views",
    #               "Articles Published", "Videos Published", "Slideshows Published", "Article Word Count",
    #               "Unique Visitors"]
    #     lang = ["English", "Philippines", "Indonesian", "Malaysian", "Thai", "Bengali"]
    #     for each in lang:
    #         df_final = pd.DataFrame(columns=["Total_" + each, str(self.last_quarter) + "/" + str(self.last_year),
    #                                 str(self.report_quarter) + "/" + str(self.report_year),
    #                                 "Quarterly_change"],
    #                                 index=metric)
    #         for m in metric:
    #             print(m)
    #             if m != "Unique Visitors":
    #                 df_total = summary_total(m)
    #                 df_total = df_total[df_total["service"] == each]
    #                 df_last = metric_summary(self.last_year, self.last_quarter, m)
    #                 df_last = df_last[df_last["service"] == each]
    #                 df_curr = metric_summary(self.report_year, self.report_quarter, m)
    #                 df_curr = df_curr[df_curr["service"] == each]
    #                 total = sum(df_total["value"])
    #                 last = sum(df_last["value"])
    #                 curr = sum(df_curr["value"])
    #                 if last != 0:
    #                     percent = float(curr) / float(last) - 1
    #                 else:
    #                     percent = -1
    #                 df_final.loc[m] = [total, last, curr, percent]
    #             else:
    #                 df_total = summary_total("New Visitors for running totals")
    #                 df_total = df_total[df_total["service"] == each]
    #                 df_last = metric_summary(self.last_year, self.last_quarter,
    #                                          "Unique Visitors for report period")
    #                 df_last = df_last[df_last["service"] == each]
    #                 df_curr = metric_summary(self.report_year, self.report_quarter,
    #                                          "Unique Visitors for report period")
    #                 df_curr = df_curr[df_curr["service"] == each]
    #                 total = sum(df_total["value"])
    #                 last = sum(df_last["value"])
    #                 curr = sum(df_curr["value"])
    #                 if last != 0:
    #                     percent = float(curr) / float(last) - 1
    #                 else:
    #                     percent = -1
    #                 df_final.loc[m] = [total, last, curr, percent]
    #         res.append(df_final)
    #     return res
