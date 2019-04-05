import pandas as pd
from rfa_test_tables import mapping_cmsid_rfapage, mapping_link_rfapage, mapping_theme_objective, \
    metadata_facebook_post, metadata_rfapage, metadata_twitter_post, \
    metric_lifetime_facebook_post, metric_lifetime_twitter_post, \
    metric_quarterly_by_item, metric_quarterly_summary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_
from rfa_query.config import DATABASE_CONFIG


def get_session():
    host = DATABASE_CONFIG['host']
    dbname = DATABASE_CONFIG['dbname']
    user = DATABASE_CONFIG['user']
    password = DATABASE_CONFIG['password']
    port = DATABASE_CONFIG['port']
    connnect_str = "mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host, port, dbname)
    engine = create_engine(connnect_str, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


session = get_session()


def df_rename(df):
    return df.rename(columns=lambda x: x.split('.')[-1], inplace=True)


def Aup(snapshort_time, first_day_of_report_period):
    fbmeta = session.query(metadata_facebook_post).filter(metadata_facebook_post.postdate < first_day_of_report_period)
    fbmetric = session.query(metric_lifetime_facebook_post). \
        filter(metric_lifetime_facebook_post.csv_export_time == snapshort_time)
    df_fbmeta = pd.read_sql(fbmeta.statement, session.bind)
    df_fbmetric = pd.read_sql(fbmetric.statement, session.bind)
    df_fbmeta = df_fbmeta.add_prefix("fbmeta.")
    df_fbmetric = df_fbmetric.add_prefix("fbmetric.")
    df_final = pd.merge(df_fbmeta, df_fbmetric, left_on="fbmeta.postid", right_on="fbmetric.postid", how="inner")
    df_final = df_final[
        ["fbmeta.service", "fbmeta.postid", "fbmeta.permalink", "fbmeta.post_type", "fbmeta.postdate", "fbmetric.views",
         "fbmetric.shares", "fbmetric.likes", "fbmetric.comments", "fbmetric.clicks"]]
    df_rename(df_final)
    return df_final


def Bup(snapshort_time, first_day_of_report_period):
    fbmeta = session.query(metadata_facebook_post).filter(metadata_facebook_post.postdate >= first_day_of_report_period)
    fbmetric = session.query(metric_lifetime_facebook_post). \
        filter(metric_lifetime_facebook_post.csv_export_time == snapshort_time)
    df_fbmeta = pd.read_sql(fbmeta.statement, session.bind)
    df_fbmetric = pd.read_sql(fbmetric.statement, session.bind)
    df_fbmeta = df_fbmeta.add_prefix("fbmeta.")
    df_fbmetric = df_fbmetric.add_prefix("fbmetric.")
    df_final = pd.merge(df_fbmeta, df_fbmetric, left_on="fbmeta.postid", right_on="fbmetric.postid", how="inner")
    df_final = df_final[
        ["fbmeta.service", "fbmeta.postid", "fbmeta.permalink", "fbmeta.post_type", "fbmeta.postdate", "fbmetric.views",
         "fbmetric.shares", "fbmetric.likes", "fbmetric.comments", "fbmetric.clicks"]]
    df_rename(df_final)
    return df_final


def Aup_twitter(snapshort_time, first_day_of_report_period):
    twmeta = session.query(metadata_twitter_post).filter(metadata_twitter_post.postdate < first_day_of_report_period)
    twmetric = session.query(metric_lifetime_twitter_post). \
        filter(metric_lifetime_twitter_post.csv_export_time == snapshort_time)
    df_twmeta = pd.read_sql(twmeta.statement, session.bind)
    df_twmetric = pd.read_sql(twmetric.statement, session.bind)
    df_twmeta = df_twmeta.add_prefix("twmeta.")
    df_twmetric = df_twmetric.add_prefix("twmetric.")
    df_final = pd.merge(df_twmeta, df_twmetric, left_on="twmeta.postid", right_on="twmetric.postid", how="inner")
    df_final = df_final[
        ["twmeta.service", "twmeta.postid", "twmeta.permalink", "twmeta.post_type", "twmeta.postdate", "twmetric.views",
         "twmetric.likes", "twmetric.retweets", "twmetric.clicks"]]
    df_rename(df_final)
    return df_final


def Bup_twitter(snapshort_time, first_day_of_report_period):
    twmeta = session.query(metadata_twitter_post).filter(metadata_twitter_post.postdate >= first_day_of_report_period)
    twmetric = session.query(metric_lifetime_twitter_post). \
        filter(metric_lifetime_twitter_post.csv_export_time == snapshort_time)
    df_twmeta = pd.read_sql(twmeta.statement, session.bind)
    df_twmetric = pd.read_sql(twmetric.statement, session.bind)
    df_twmeta = df_twmeta.add_prefix("twmeta.")
    df_twmetric = df_twmetric.add_prefix("twmetric.")
    df_final = pd.merge(df_twmeta, df_twmetric, left_on="twmeta.postid", right_on="twmetric.postid", how="inner")
    df_final = df_final[
        ["twmeta.service", "twmeta.postid", "twmeta.permalink", "twmeta.post_type", "twmeta.postdate", "twmetric.views",
         "twmetric.likes", "twmetric.retweets", "twmetric.clicks"]]
    df_rename(df_final)
    return df_final


def facebook_expanded_data_post_quarterly(latest_snapshot_time, previous_snapshot_time, first_day_of_report_period):
    df_aup1 = Aup(latest_snapshot_time, first_day_of_report_period)
    df_aup2 = Aup(previous_snapshot_time, first_day_of_report_period)
    df_aup1 = df_aup1[["service", "postid", "permalink", "post_type", "postdate",
                       "views", "shares", "likes", "comments", "clicks"]]
    df_aup2 = df_aup2[["service", "postid", "permalink", "post_type", "postdate",
                       "views", "shares", "likes", "comments", "clicks"]]
    df_aup1 = df_aup1.add_prefix("Aup1.")
    df_aup2 = df_aup2.add_prefix("Aup2.")
    df_aup12 = pd.merge(df_aup1, df_aup2, left_on="Aup1.postid", right_on="Aup2.postid", how="inner")

    # # Alink #
    alink = session.query(mapping_link_rfapage)
    df_alink = pd.read_sql(alink.statement, session.bind)
    df_alink = df_alink.add_prefix("Alink.")
    # # Acms
    acms = session.query(mapping_cmsid_rfapage)
    df_acms = pd.read_sql(acms.statement, session.bind)
    df_acms = df_acms.add_prefix("Acms.")
    arfa = session.query(metadata_rfapage)
    df_arfa = pd.read_sql(arfa.statement, session.bind)
    df_arfa = df_arfa.add_prefix("Arfa.")
    aobj = session.query(mapping_theme_objective)
    df_aobj = pd.read_sql(aobj.statement, session.bind)
    df_aobj = df_aobj.add_prefix("Aobj.")
    df_aupalink = pd.merge(df_aup12, df_alink, left_on="Aup1.permalink", right_on="Alink.external_link", how="left")
    df_aacms = pd.merge(df_aupalink, df_acms, left_on="Alink.rfa_link", right_on="Acms.rfa_link", how="left")
    df_aarfa = pd.merge(df_aacms, df_arfa, how="left", left_on="Acms.cmsid", right_on="Arfa.online_id")
    df_A = pd.merge(df_aarfa, df_aobj, how="left", left_on="Arfa.theme", right_on="Aobj.theme")
    df_A["views"] = df_A["Aup1.views"] - df_A["Aup2.views"]
    df_A["shares"] = df_A["Aup1.shares"] - df_A["Aup2.shares"]
    df_A["likes"] = df_A["Aup1.likes"] - df_A["Aup2.likes"]
    df_A["comments"] = df_A["Aup1.comments"] - df_A["Aup2.comments"]
    df_A["clicks"] = df_A["Aup1.clicks"] - df_A["Aup2.clicks"]
    df_A = df_A[
        ["Aup1.postid", "Aup1.service", "Aup1.permalink", "Alink.rfa_link",
         "Aup1.post_type", "Aup1.postdate", "views", "shares",
         "likes", "comments", "clicks", "Arfa.program", "Arfa.theme",
         "Arfa.headline", "Arfa.pubdate", "Arfa.media_type",
         "Aobj.objective1", "Aobj.objective2",
         "Aobj.objective3"]]
    df_rename(df_A)

    df_bup1 = Bup(latest_snapshot_time, first_day_of_report_period)
    bup2 = session.query(mapping_link_rfapage)
    df_bup2 = pd.read_sql(bup2.statement, session.bind)
    bcms = session.query(mapping_cmsid_rfapage)
    df_bcms = pd.read_sql(bcms.statement, session.bind)
    brfa = session.query(metadata_rfapage)
    df_brfa = pd.read_sql(brfa.statement, session.bind)
    bobj = session.query(mapping_theme_objective)
    df_bobj = pd.read_sql(bobj.statement, session.bind)

    df_bup1 = df_bup1.add_prefix("Bup1.")
    df_bup2 = df_bup2.add_prefix("Bup2.")
    df_bcms = df_bcms.add_prefix("Bcms.")
    df_brfa = df_brfa.add_prefix("Brfa.")
    df_bobj = df_bobj.add_prefix("Bobj.")

    df_bup12 = pd.merge(df_bup1, df_bup2, how="left", left_on="Bup1.permalink", right_on="Bup2.external_link")
    df_bbcms = pd.merge(df_bup12, df_bcms, how="left", left_on="Bup2.rfa_link", right_on="Bcms.rfa_link")
    df_bbrfa = pd.merge(df_bbcms, df_brfa, how="left", left_on="Bcms.cmsid", right_on="Brfa.online_id")
    ## problems ##
    df_B = pd.merge(df_bbrfa, df_bobj, how="left", left_on="Brfa.theme", right_on="Bobj.theme")

    df_B = df_B[["Bup1.postid", "Bup1.service", "Bup1.permalink", "Bup2.rfa_link",
                 "Bup1.post_type", "Bup1.postdate", "Bup1.views",
                 "Bup1.shares", "Bup1.likes", "Bup1.comments", "Bup1.clicks", "Brfa.program", "Brfa.theme",
                 "Brfa.headline", "Brfa.pubdate", "Brfa.media_type",
                 "Bobj.objective1", "Bobj.objective2", "Bobj.objective3"]]
    ###
    df_rename(df_B)
    df_final = pd.concat([df_A, df_B])
    df_final = df_final[df_final["service"] != "Korean"]
    df_add = facebook_theme_multiple_sources()
    df_final = df_final.add_prefix("final.")
    df_add = df_add.add_prefix("add.")
    df_final = pd.merge(df_final, df_add, left_on="final.postid", right_on="add.postid", how="inner")
    df_final = df_final[["final.postid", "final.service", "final.permalink", "final.rfa_link",
                         "final.post_type", "final.postdate", "final.views",
                         "final.shares", "final.likes", "final.comments", "final.clicks", "add.program",
                         "add.theme", "final.headline", "final.pubdate", "final.media_type", "final.objective1",
                         "final.objective2", "final.objective3"]]
    df_rename(df_final)
    return df_final


def twitter_expanded_data_post_quarterly(latest_snapshot_time, previous_snapshot_time, first_day_of_report_period):
    df_aup1 = Aup_twitter(latest_snapshot_time, first_day_of_report_period)
    df_aup2 = Aup_twitter(previous_snapshot_time, first_day_of_report_period)
    df_aup1 = df_aup1[["service", "postid", "permalink", "post_type", "postdate",
                        "views", "likes", "retweets", "clicks"]]
    df_aup2 = df_aup2[["service", "postid", "permalink", "post_type", "postdate",
                        "views", "likes", "retweets", "clicks"]]
    df_aup1 = df_aup1.add_prefix("Aup1.")
    df_aup2 = df_aup2.add_prefix("Aup2.")
    df_aup12 = pd.merge(df_aup1, df_aup2, left_on="Aup1.postid", right_on="Aup2.postid", how="inner")
    alink = session.query(mapping_link_rfapage)
    df_alink = pd.read_sql(alink.statement, session.bind)
    df_alink = df_alink.add_prefix("Alink.")
    acms = session.query(mapping_cmsid_rfapage)
    df_acms = pd.read_sql(acms.statement, session.bind)
    df_acms = df_acms.add_prefix("Acms.")
    arfa = session.query(metadata_rfapage)
    df_arfa = pd.read_sql(arfa.statement, session.bind)
    df_arfa = df_arfa.add_prefix("Arfa.")
    aobj = session.query(mapping_theme_objective)
    df_aobj = pd.read_sql(aobj.statement, session.bind)
    df_aobj = df_aobj.add_prefix("Aobj.")
    df_aupalink = pd.merge(df_aup12, df_alink, left_on="Aup1.permalink", right_on="Alink.external_link", how="left")
    df_aacms = pd.merge(df_aupalink, df_acms, left_on="Alink.rfa_link", right_on="Acms.rfa_link", how="left")
    df_aarfa = pd.merge(df_aacms, df_arfa, how="left", left_on="Acms.cmsid", right_on="Arfa.online_id")
    df_A = pd.merge(df_aarfa, df_aobj, how="left", left_on="Arfa.theme", right_on="Aobj.theme")
    df_A["views"] = df_A["Aup1.views"] - df_A["Aup2.views"]
    df_A["likes"] = df_A["Aup1.likes"] - df_A["Aup2.likes"]
    df_A["retweets"] = df_A["Aup1.retweets"] - df_A["Aup2.retweets"]
    df_A["clicks"] = df_A["Aup1.clicks"] - df_A["Aup2.clicks"]
    df_A = df_A[
        ["Aup1.postid", "Aup1.service", "Aup1.permalink", "Alink.rfa_link", "Aup1.post_type", "Aup1.postdate", "views", "likes",
            "retweets", "clicks", "Arfa.program", "Arfa.theme", "Arfa.pubdate", "Arfa.headline", "Arfa.media_type",
            "Aobj.objective1", "Aobj.objective2",
            "Aobj.objective3"]]
    df_rename(df_A)

    df_bup1 = Bup_twitter(latest_snapshot_time, first_day_of_report_period)
    bup2 = session.query(mapping_link_rfapage)
    df_bup2 = pd.read_sql(bup2.statement, session.bind)
    bcms = session.query(mapping_cmsid_rfapage)
    df_bcms = pd.read_sql(bcms.statement, session.bind)
    brfa = session.query(metadata_rfapage)
    df_brfa = pd.read_sql(brfa.statement, session.bind)
    bobj = session.query(mapping_theme_objective)
    df_bobj = pd.read_sql(bobj.statement, session.bind)

    df_bup1 = df_bup1.add_prefix("Bup1.")
    df_bup2 = df_bup2.add_prefix("Bup2.")
    df_bcms = df_bcms.add_prefix("Bcms.")
    df_brfa = df_brfa.add_prefix("Brfa.")
    df_bobj = df_bobj.add_prefix("Bobj.")
    df_bup12 = pd.merge(df_bup1, df_bup2, how="left", left_on="Bup1.permalink", right_on="Bup2.external_link")
    df_bbcms = pd.merge(df_bup12, df_bcms, how="left", left_on="Bup2.rfa_link", right_on="Bcms.rfa_link")
    df_bbrfa = pd.merge(df_bbcms, df_brfa, how="left", left_on="Bcms.cmsid", right_on="Brfa.online_id")
    df_B = pd.merge(df_bbrfa, df_bobj, how="left", left_on="Brfa.theme", right_on="Bobj.theme")
    df_B = df_B[["Bup1.postid", "Bup1.service", "Bup1.permalink", "Bup2.rfa_link",
                    "Bup1.post_type", "Bup1.postdate", "Bup1.views",
                    "Bup1.likes", "Bup1.retweets",
                    "Bup1.clicks", "Brfa.program", "Brfa.theme", "Brfa.pubdate", "Brfa.headline", "Brfa.media_type",
                    "Bobj.objective1",
                    "Bobj.objective2", "Bobj.objective3"]]
    df_rename(df_B)
    df_final = pd.concat([df_A, df_B])
    df_final = df_final[df_final["service"] != "Korean"]
    return df_final


def twitter_total_prc_summary(beginning_of_prc, current_day_of_prc, first_day):
    data = twitter_expanded_data_post_quarterly(beginning_of_prc, current_day_of_prc, first_day)
    return data


def twitter_top5_items(year, quarter, program):
    a = session.query(metric_quarterly_by_item).filter(and_(metric_quarterly_by_item.year == year,
                                                            metric_quarterly_by_item.quarter == quarter,
                                                            metric_quarterly_by_item.platform == "twitter"))
    df_a = pd.read_sql(a.statement, session.bind)
    df_pivot = df_a.pivot(index="online_id", columns="metric", values="value")
    df_pivot = df_pivot.add_prefix("pivot.")
    df_a = df_a[["service", "online_id", "year", "quarter"]]
    df_a = pd.merge(df_a, df_pivot, on="online_id", how="inner")
    df_rename(df_a)
    df_a = df_a.add_prefix("a.")
    b = session.query(metadata_twitter_post)
    df_b = pd.read_sql(b.statement, session.bind)
    df_b = df_b.add_prefix("b.")
    df_ab = pd.merge(df_a, df_b, left_on="a.online_id", right_on="b.postid", how="inner")
    c = session.query(mapping_link_rfapage)
    df_c = pd.read_sql(c.statement, session.bind)
    df_c = df_c.add_prefix("c.")
    df_abc = pd.merge(df_ab, df_c, left_on="b.permalink", right_on="c.external_link", how="inner")
    d = session.query(mapping_cmsid_rfapage)
    df_d = pd.read_sql(d.statement, session.bind)
    df_d = df_d.add_prefix("d.")
    df_abcd = pd.merge(df_abc, df_d, left_on="c.rfa_link", right_on="d.rfa_link", how="inner")
    e = session.query(metadata_rfapage).filter(metadata_rfapage.program == program)
    df_e = pd.read_sql(e.statement, session.bind)
    df_e = df_e.add_prefix("e.")
    df_final = pd.merge(df_abcd, df_e, left_on="d.cmsid", right_on="e.online_id", how="inner")
    df_final = df_final[["a.online_id", "a.service", "a.year",
                        "a.quarter", "a.clicks", "a.likes",
                        "a.retweets", "a.views", "e.media_type",
                        "e.pubdate", "e.headline"]]
    df_rename(df_final)
    return df_final.sort_values(by=["retweets"], ascending=False)


def metric_quarterly_by_item_table(platform, latest_snapshot_time, previous_snapshot_time, first_day_of_report_quarter,
                                   report_year, report_quarter):
    if platform == "twitter":
        df_aup1 = Aup_twitter(latest_snapshot_time, first_day_of_report_quarter)
        df_aup1 = df_aup1[["service", "postid", "views"]]
        df_aup2 = Aup_twitter(previous_snapshot_time, first_day_of_report_quarter)
        df_aup2 = df_aup2[["service", "postid", "views"]]
        df_aup1 = df_aup1.add_prefix("Aup1.")
        df_aup2 = df_aup2.add_prefix("Aup2.")
        df_A = pd.merge(df_aup1, df_aup2, left_on="Aup1.postid", right_on="Aup2.postid", how="inner")
        df_A["views"] = df_A["Aup1.views"] - df_A["Aup2.views"]
        df_A["metric"] = "views"
        df_A = df_A[["views", "Aup1.service", "Aup1.postid", "metric"]]
        df_A["platform"] = platform
        df_A["year"] = str(report_year)
        df_A["quarter"] = str(report_quarter)
        df_rename(df_A)

        df_bup = Bup_twitter(latest_snapshot_time, first_day_of_report_quarter)
        df_bup = df_bup[["postid", "service", "views"]]
        df_bup["platform"] = platform
        df_bup["year"] = str(report_year)
        df_bup["quarter"] = str(report_quarter)
        df_bup["metric"] = "views"

        df_final = pd.concat([df_A, df_bup])
        return df_final

    if platform == "facebook":
        df_aup1 = Aup(latest_snapshot_time, first_day_of_report_quarter)
        df_aup1 = df_aup1[["service", "postid", "views"]]
        df_aup2 = Aup(previous_snapshot_time, first_day_of_report_quarter)
        df_aup2 = df_aup2[["service", "postid", "views"]]
        df_aup1 = df_aup1.add_prefix("Aup1.")
        df_aup2 = df_aup2.add_prefix("Aup2.")
        df_A = pd.merge(df_aup1, df_aup2, left_on="Aup1.postid", right_on="Aup2.postid", how="inner")
        df_A["views"] = df_A["Aup1.views"] - df_A["Aup2.views"]
        df_A["metric"] = "views"
        df_A = df_A[["views", "Aup1.service", "Aup1.postid", "metric"]]
        df_A["platform"] = platform
        df_A["year"] = str(report_year)
        df_A["quarter"] = str(report_quarter)

        df_rename(df_A)

        df_bup = Bup(latest_snapshot_time, first_day_of_report_quarter)

        df_bup = df_bup[["postid", "service", "views"]]
        df_bup["platform"] = platform
        df_bup["year"] = str(report_year)
        df_bup["quarter"] = str(report_quarter)
        df_bup["metric"] = "views"

        df_final = pd.concat([df_A, df_bup])
        return df_final


def facebook_theme_multiple_sources():
    a = session.query(metadata_facebook_post)
    b = session.query(mapping_link_rfapage).filter(~mapping_link_rfapage.rfa_link.like('%benarnews.org%')).\
        filter(~mapping_link_rfapage.rfa_link.like('%rfa.org%'))

    df_a = pd.read_sql(a.statement, session.bind)
    df_b = pd.read_sql(b.statement, session.bind)
    df_a = df_a.add_prefix('a.')
    df_b = df_b.add_prefix("b.")
    df_sub1 = pd.merge(df_a, df_b, left_on="a.permalink", right_on="b.external_link", how="inner")
    df_sub1 = df_sub1[["a.postid", "a.service", "a.permalink", "a.postdate", "b.rfa_link", "a.program", "a.theme"]]
    df_rename(df_sub1)

    w = session.query(metadata_facebook_post)
    x = session.query(mapping_link_rfapage).filter(or_(mapping_link_rfapage.rfa_link.like('%benarnews.org%'),
                                                       mapping_link_rfapage.rfa_link.like('%rfa.org%')))
    y = session.query(mapping_cmsid_rfapage)
    z = session.query(metadata_rfapage)
    df_w = pd.read_sql(w.statement, session.bind)
    df_x = pd.read_sql(x.statement, session.bind)
    df_y = pd.read_sql(y.statement, session.bind)
    df_z = pd.read_sql(z.statement, session.bind)
    df_w = df_w.add_prefix("w.")
    df_x = df_x.add_prefix("x.")
    df_y = df_y.add_prefix("y.")
    df_z = df_z.add_prefix("z.")
    df_wx = pd.merge(df_w, df_x, left_on="w.permalink", right_on='x.external_link', how="inner")
    df_wxy = pd.merge(df_wx, df_y, left_on="x.rfa_link", right_on="y.rfa_link", how="left")
    df_sub2 = pd.merge(df_wxy, df_z, left_on="y.cmsid", right_on="z.online_id", how="left")
    df_sub2 = df_sub2[["w.postid", "w.service", "w.permalink", "w.postdate", "x.rfa_link", "z.program", "z.theme"]]
    df_rename(df_sub2)
    df_final = pd.concat([df_sub1, df_sub2])
    df_final = df_final[df_final["service"] != 'Korean']
    return df_final


def facebook_top5_items_helper(language, year, quarter, program):
    a = session.query(metric_quarterly_by_item).filter(and_(metric_quarterly_by_item.platform == "facebook",
                                                            metric_quarterly_by_item.service == language,
                                                            metric_quarterly_by_item.year == year,
                                                            metric_quarterly_by_item.quarter == quarter))
    df_a = pd.read_sql(a.statement, session.bind)
    df_pivot = df_a.pivot(index="online_id", columns="metric", values="value")
    df_pivot = df_pivot.add_prefix("pivot.")
    df_a = df_a[["service", "online_id", "year", "quarter"]]
    df_a = pd.merge(df_a, df_pivot, left_on="online_id", right_on="online_id", how="inner")
    df_rename(df_a)
    df_a = df_a.add_prefix("a.")
    b = session.query(metadata_facebook_post).filter(metadata_facebook_post.service == language)
    df_b = pd.read_sql(b.statement, session.bind)
    df_b = df_b[["postid", "permalink", "post_type"]]
    df_b = df_b.add_prefix("b.")
    df_ab = pd.merge(df_a, df_b, left_on="a.online_id", right_on="b.postid", how="inner")
    c = session.query(mapping_link_rfapage)
    df_c = pd.read_sql(c.statement, session.bind)
    df_c = df_c.add_prefix("c.")
    df_abc = pd.merge(df_ab, df_c, left_on="b.permalink", right_on="c.external_link")
    d = session.query(mapping_cmsid_rfapage).filter(mapping_cmsid_rfapage.service == language)
    df_d = pd.read_sql(d.statement, session.bind)
    df_d = df_d.add_prefix("d.")
    df_abcd = pd.merge(df_abc, df_d, left_on="c.rfa_link", right_on="d.rfa_link", how="inner")
    e = session.query(metadata_rfapage).filter(and_(metadata_rfapage.service == language,
                                                    metadata_rfapage.program == program))
    df_e = pd.read_sql(e.statement, session.bind)
    df_e = df_e.add_prefix("e.")
    df_final = pd.merge(df_abcd, df_e, left_on="d.cmsid", right_on="e.online_id", how="inner")
    df_final = df_final[["a.service", "a.year", "a.quarter",
                         "a.online_id", "a.clicks", "a.comments",
                         "a.likes", "a.shares", "a.views", "d.cmsid",  "e.program",
                        "e.media_type", "e.pubdate",
                         "e.headline"]]
    df_rename(df_final)
    df_final["likes_shares"] = df_final["likes"] + df_final["shares"]
    return df_final.sort_values(by=["likes_shares"], ascending=False)


# Select Google Articles From New Table #
def google_articles_table(quarter, lang):
    google = session.query(metric_quarterly_by_item). \
        filter(and_(metric_quarterly_by_item.platform == 'benarnews.org',
                    metric_quarterly_by_item.quarter == quarter, metric_quarterly_by_item.service == lang))
    df_google = pd.read_sql(google.statement, session.bind)
    return df_google


# select google articles reads #
def google_articles_reads(year, quarter, metric):
    google = session.query(metric_quarterly_by_item).filter(and_(metric_quarterly_by_item.platform == "benarnews.org",
                                                                 metric_quarterly_by_item.year == year,
                                                                 metric_quarterly_by_item.quarter == quarter,
                                                                 metric_quarterly_by_item.metric == metric))
    df_google = pd.read_sql(google.statement, session.bind)
    return df_google


# select google articles by different objective #
def google_articles_reads_by_obj(year, quarter, metric):
    a = session.query(metric_quarterly_by_item).filter(and_(metric_quarterly_by_item.platform == "benarnews.org",
                                                            metric_quarterly_by_item.year == year,
                                                            metric_quarterly_by_item.quarter == quarter,
                                                            metric_quarterly_by_item.metric == metric))
    df_a = pd.read_sql(a.statement, session.bind)
    b = session.query(metadata_rfapage)
    df_b = pd.read_sql(b.statement, session.bind)
    c = session.query(mapping_theme_objective)
    df_c = pd.read_sql(c.statement, session.bind)
    df_a = df_a.add_prefix("a.")
    df_b = df_b.add_prefix('b.')
    df_c = df_c.add_prefix("c.")
    df_ab = pd.merge(df_a, df_b, left_on="a.online_id", right_on="b.online_id", how="left")
    df_abc = pd.merge(df_ab, df_c, left_on="b.theme", right_on="c.theme", how="left")
    df_final = df_abc[["a.value", "c.objective1", "c.objective2", "c.objective3"]]
    return df_final


def google_articles_reads_by_theme_program(report_year, report_quarter, platform, metric, program):
    a = session.query(metric_quarterly_by_item).filter(and_(metric_quarterly_by_item.platform == platform,
                                                            metric_quarterly_by_item.year == report_year,
                                                            metric_quarterly_by_item.quarter == report_quarter,
                                                            metric_quarterly_by_item.metric == metric))
    df_a = pd.read_sql(a.statement, session.bind)
    b = session.query(metadata_rfapage).filter(metadata_rfapage.program == program)
    df_b = pd.read_sql(b.statement, session.bind)
    df_a = df_a.add_prefix("a.")
    df_b = df_b.add_prefix("b.")
    df_final = pd.merge(df_a, df_b, how="left", left_on="a.online_id", right_on="b.online_id")
    df_final = df_final[["a.value", "b.theme"]]
    df_rename(df_final)
    return df_final.groupby("theme").sum()


def google_articles_reads_by_objective_program(report_year, report_quarter, platform, metric, program):
    a = session.query(metric_quarterly_by_item).filter(and_(metric_quarterly_by_item.platform == platform,
                                                            metric_quarterly_by_item.year == report_year,
                                                            metric_quarterly_by_item.quarter == report_quarter,
                                                            metric_quarterly_by_item.metric == metric))
    df_a = pd.read_sql(a.statement, session.bind)
    b = session.query(metadata_rfapage).filter(metadata_rfapage.program == program)
    df_b = pd.read_sql(b.statement, session.bind)
    c = session.query(mapping_theme_objective)
    df_c = pd.read_sql(c.statement, session.bind)
    df_a = df_a.add_prefix("a.")
    df_b = df_b.add_prefix('b.')
    df_c = df_c.add_prefix("c.")
    df_ab = pd.merge(df_a, df_b, left_on="a.online_id", right_on="b.online_id", how="left")
    df_abc = pd.merge(df_ab, df_c, left_on="b.theme", right_on="c.theme", how="left")
    df_final1 = df_abc[["a.value", "c.objective1"]]
    df_final2 = df_abc[["a.value", "c.objective2"]]
    df_final3 = df_abc[["a.value", "c.objective3"]]
    df_final1 = df_final1.rename(columns={"a.value": "value", "c.objective1": "objective"})
    df_final2 = df_final1.rename(columns={"a.value": "value", "c.objective2": "objective"})
    df_final3 = df_final1.rename(columns={"a.value": "value", "c.objective3": "objective"})
    df_final = pd.concat([df_final1, df_final2, df_final3])
    return df_final


def metric_summary(report_year, report_quarter, metric):
    a = session.query(metric_quarterly_summary).filter(and_(metric_quarterly_summary.year == report_year,
                                                            metric_quarterly_summary.quarter == report_quarter,
                                                            metric_quarterly_summary.platform == "benarnews.org",
                                                            metric_quarterly_summary.metric == metric))
    df_a = pd.read_sql(a.statement, session.bind)
    return df_a


def summary_total(metric):
    a = session.query(metric_quarterly_summary).filter(and_(metric_quarterly_summary.metric == metric))
    df_a = pd.read_sql(a.statement, session.bind)
    return df_a


def google_articles_get_prc_article_reads_by_quarter(year, quarter):
    a = session.query(metric_quarterly_by_item).filter(metric_quarterly_by_item.year == year,
                                                       metric_quarterly_by_item.quarter == quarter,
                                                       metric_quarterly_by_item.platform == "benarnews.org")
    df_a = pd.read_sql(a.statement, session.bind)
    b = session.query(metadata_rfapage).filter(metadata_rfapage.program == "PRC")
    df_b = pd.read_sql(b.statement, session.bind)
    df_a = df_a.add_prefix("a.")
    df_b = df_b.add_prefix("b.")
    df_final = pd.merge(df_a, df_b, left_on="a.online_id", right_on="b.online_id", how="inner")
    df_final = df_final[["a.service", "a.value", "b.program"]]
    df_rename(df_final)
    return df_final


def google_articles_get_prc_article_reads_total():
    a = session.query(metric_quarterly_by_item).filter(metric_quarterly_by_item.platform == "benarnews.org")
    df_a = pd.read_sql(a.statement, session.bind)
    b = session.query(metadata_rfapage).filter(metadata_rfapage.program == "PRC")
    df_b = pd.read_sql(b.statement, session.bind)
    df_a = df_a.add_prefix("a.")
    df_b = df_b.add_prefix("b.")
    df_final = pd.merge(df_a, df_b, left_on="a.online_id", right_on="b.online_id", how="inner")
    df_final = df_final[["a.service", "a.value", "b.program"]]
    df_rename(df_final)
    return df_final


if __name__ == "__main__":
    latest_snapshot_time1 = '2019-03-18 13:00:00'
    previous_snapshot_time1 = '2018-12-17 10:00:00'
    first_day1 = '2018-12-15'

    latest_snapshot_time2 = '2018-12-17 10:00:00'
    previous_snapshot_time2 = '2018-10-01 13:00:00'
    first_day2 = '2018-10-01'

    latest_snapshot_time3 = '2018-10-01 13:00:00'
    previous_snapshot_time3 = '2018-09-04 12:00:00'
    first_day3 = '2018-09-01'

    latest_snapshot_time4 = '2018-09-04 12:00:00'
    previous_snapshot_time4 = '2018-08-01 12:00:00'
    first_day4 = '2018-08-01'

    data1 = twitter_expanded_data_post_quarterly(latest_snapshot_time1, previous_snapshot_time1, first_day1)
    data2 = twitter_expanded_data_post_quarterly(latest_snapshot_time2, previous_snapshot_time2, first_day2)
    data3 = twitter_expanded_data_post_quarterly(latest_snapshot_time3, previous_snapshot_time3, first_day3)
    data4 = twitter_expanded_data_post_quarterly(latest_snapshot_time4, previous_snapshot_time4, first_day4)

    data1 = data1[data1['program'] == 'PRC']
    data2 = data2[data2['program'] == 'PRC']
    data3 = data3[data3['program'] == 'PRC']
    data4 = data4[data4['program'] == 'PRC']
    total_retweets = sum(data1["views"]) + sum(data2["views"]) + sum(data3["views"]) + sum(data4["views"])
    print(total_retweets)