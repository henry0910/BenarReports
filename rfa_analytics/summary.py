import pandas as pd


class Summary(object):
    def __init__(self, facebook, twitter, rfapage):
        self.facebook = facebook
        self.twitter = twitter
        self.rfapage = rfapage

    def impacts(self):
        facebook_data = self.facebook.facebook_data_post_quarterly()
        twitter_data = self.twitter.twitter_data_post_quarterly()
        rfa_data = self.rfapage.rfapage_data_post_quarterly()
        return facebook_data, twitter_data, rfa_data

    def impact_by_theme(self):
        res = []
        program = ["VEO", "PRC"]
        for i in program:
            df_facebook, df_twitter, df_google = self.impacts()
            df_facebook = df_facebook[df_facebook["program"] == i]
            df_twitter = df_twitter[df_twitter["program"] == i]
            df_google = df_google[df_google["program"] == i]
            df_facebook = df_facebook[["theme", "views"]]
            df_twitter = df_twitter[["theme", "views"]]
            df_google = df_google[["theme", "value"]]
            df_facebook = df_facebook.groupby("theme").sum()
            df_twitter = df_twitter.groupby("theme").sum()
            df_google = df_google.groupby("theme").sum()
            df_facebook = df_facebook.rename(columns={"views": "Facebook views"})
            df_twitter = df_twitter.rename(columns={"views": "Twitter views"})
            df_google = df_google.rename(columns={"value": "article reads"})
            df_final = pd.concat([df_google, df_facebook, df_twitter], axis=1)
            df_final = df_final.fillna(0)
            df_final["Total"] = df_final["Facebook views"] + df_final["Twitter views"] + df_final["article reads"]
            res.append(df_final)
        return res

    def impact_by_objective(self):
        res = []
        program = ["VEO", "PRC"]
        for i in program:
            df_facebook, df_twitter, df_google = self.impacts()
            df_facebook = df_facebook[df_facebook["program"] == i]
            df_twitter = df_twitter[df_twitter["program"] == i]
            df_google = df_google[df_google["program"] == i]
            df_facebook = df_facebook[["views", "objective1", "objective2", "objective3"]]
            df_twitter = df_twitter[["views", "objective1", "objective2", "objective3"]]
            df_google = df_google[["value", "objective1", "objective2", "objective3"]]
            df_facebook = pd.melt(df_facebook, id_vars=["views"], value_vars=["objective1", "objective2", "objective3"],
                                  value_name="objective")
            df_twitter = pd.melt(df_twitter, id_vars=["views"], value_vars=["objective1", "objective2", "objective3"],
                                 value_name="objective")
            df_google = pd.melt(df_google, id_vars=["value"], value_vars=["objective1", "objective2", "objective3"],
                                value_name="objective")
            df_facebook = df_facebook.dropna()
            df_twitter = df_twitter.dropna()
            df_google = df_google.dropna()
            df_facebook = df_facebook.groupby("objective").sum()
            df_twitter = df_twitter.groupby("objective").sum()
            df_google = df_google.groupby("objective").sum()
            df_facebook = df_facebook.rename(columns={"views": "Facebook views"})
            df_twitter = df_twitter.rename(columns={"views": "Twitter views"})
            df_google = df_google.rename(columns={"value": "article reads"})
            df_final = pd.concat([df_google, df_facebook, df_twitter], axis=1)
            df_final["Total"] = df_final["Facebook views"] + df_final["Twitter views"] + df_final["article reads"]
            res.append(df_final)
        return res

    def summary_statistics_social_media(self):
        data_twitter = self.twitter.twitter_summary()
        data_facebook = self.facebook.facebook_summary()
        data = pd.concat([data_facebook, data_twitter])
        return data

