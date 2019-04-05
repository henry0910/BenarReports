from rfa_analytics.rfa_analytics_facebook import Facebook
from rfa_analytics.rfa_analytics_twitter import Twitter
from rfa_analytics.rfa_analytics_rfapage import Rfa
from rfa_analytics.summary import Summary
import rfa_query.config as rfc
import os

if __name__ == "__main__":
    csv_mode = True
    keyword = 'Facebook'

    facebook_latest_snapshot_time = rfc.FACEBOOK_REPORT_CONFIG["latest_snapshot_time"]
    facebook_previous_snapshot_time = rfc.FACEBOOK_REPORT_CONFIG["previous_snapshot_time"]
    facebook_first_day_of_period = rfc.FACEBOOK_REPORT_CONFIG["first_day_of_report_period"]
    facebook_last_day_of_period = rfc.FACEBOOK_REPORT_CONFIG["last_day_of_report_period"]

    twitter_latest_snapshot_time = rfc.TWITTER_REPORT_CONFIG["latest_snapshot_time"]
    twitter_previous_snapshot_time = rfc.TWITTER_REPORT_CONFIG["previous_snapshot_time"]
    twitter_first_day_of_period = rfc.TWITTER_REPORT_CONFIG["first_day_of_report_period"]
    twitter_last_day_of_period = rfc.TWITTER_REPORT_CONFIG["last_day_of_report_period"]

    rfa_metric = rfc.RFAPAGE_REPORT_CONFIG["metric"]
    rfa_platform = rfc.RFAPAGE_REPORT_CONFIG["platform"]

    report_quarter = rfc.REPORT_DATE_CONFIG['report_quarter']
    last_quarter = rfc.REPORT_DATE_CONFIG["last_quarter"]
    report_year = rfc.REPORT_DATE_CONFIG['report_year']
    last_year = rfc.REPORT_DATE_CONFIG["last_year"]
    program = rfc.REPORT_DATE_CONFIG['program']
    lang = 'English'

    facebook = Facebook(facebook_latest_snapshot_time, facebook_previous_snapshot_time,
                        facebook_first_day_of_period, facebook_last_day_of_period,
                        report_year, last_year, report_quarter, last_quarter, program,
                        lang, environment='prod')
    twitter = Twitter(twitter_latest_snapshot_time, twitter_previous_snapshot_time, twitter_first_day_of_period,
                      twitter_last_day_of_period, report_year, report_quarter, program, lang, environment="prod")
    rfa = Rfa(report_year, last_year, report_quarter, last_quarter, program, rfa_metric, rfa_platform,
              environment='prod')
    impacts = Summary(facebook, twitter, rfa)

    dir_path = os.path.dirname(__file__)
    output_path = os.path.abspath(os.path.join(dir_path, '..', 'output'))

    # facebook #

    # if keyword == 'Facebook' and csv_mode:
    #     data_facebook_metric_table = facebook.facebook_metric_daily_table()
    #     data_facebook_csv_export_time = facebook.facebook_csv_export_time()
    #     data_facebook_profile_by_lang = facebook.facebook_total_profile_metric_by_lang()
    #     data_facebook_new_profile_by_lang = facebook.facebook_news_profile_likes_by_lang()
    #     data_facebook_metric_by_objective = facebook.facebook_metric_by_objective()
    #     data_facebook_metric_by_theme = facebook.facebook_metric_by_theme()
    #     data_facebook_data_post_quarterly = facebook.facebook_data_post_quarterly()
    #     data_facebook_top_five_items = facebook.facebook_top_five_items()
    #     data_facebook_metric_table.to_csv(output_path + '_metric_table.csv')

    # twitter #
    print(twitter.twitter_summary_veo())
    # data_twitter_metric_table = twitter.twitter_metric_table()
    # data_twitter_metric_by_lang = twitter.twitter_metric_by_lang()
    # data_twitter_csv_export_time = twitter.twitter_csv_export_time()
    # data_twitter_metric_by_theme = twitter.twitter_metric_by_theme()
    # data_twitter_metric_by_objective = twitter.twitter_metric_by_objective()
    # data_twitter_data_post_quarterly = twitter.twitter_data_post_quarterly()
    # data_twitter_top_five_items = twitter.twitter_top_five_items()
    # # rfa_page #
    # data_rfa_data_post_quarterly = rfa.rfapage_data_post_quarterly()
    #
    #
    
