from rfa_query import get_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from rfa_analytics.rfa_test_tables import metadata_twitter_post, metric_lifetime_twitter_post
import glob


class TwitterParser(object):
    engine = get_engine()
    Session = sessionmaker(bind=engine)

    def __init__(self, path, time, session=Session):
        self.input = path
        self._session = session()
        self.time = time

    def get_all_files(self):
        all_files = glob.glob(self.input + '/*.csv')
        return all_files

    def metric_lifetime_twitter_insertion(self):
        all_file_list = self.get_all_files()
        for single_file in all_file_list:
            filename = single_file.split('/')[-1]
            df = pd.read_csv(filename)
            df = df[["Tweet id", "impressions", "retweets", "likes", "url clicks"]]
            df["csv_export_time"] = self.time
            df = df.rename(columns={"Tweet id": "postid", "url clicks": "clicks", "impressions": "views"})
            if filename.find("Ben") != -1:
                df["service"] = "Bengali"
            if filename.find("Eng") != -1:
                df["service"] = "English"
            if filename.find("Ind") != -1:
                df["service"] = "Indonesian"
            if filename.find("Mal") != -1:
                df["service"] = "Malaysian"
            if filename.find("Phi") != -1:
                df["service"] = "Philippines"
            if filename.find("Tha") != -1:
                df["service"] = "Thai"
            for index, row in df.iterrows():
                postid = row["postid"]
                service = row["service"]
                views = row["views"]
                likes = row["likes"]
                retweets = row["retweets"]
                clicks = row["clicks"]
                csv_export_time = row["csv_export_time"]
                curr = metric_lifetime_twitter_post(service=service, postid=postid, views=views, likes=likes,
                                                       retweets=retweets, clicks=clicks, csv_export_time=csv_export_time)
                self._session.add(curr)
            try:
                self._session.commit()
            except:
                self._session.rollback()

    def metadata_twitter_post(self):
        all_file_list = self.get_all_files()
        for single_file in all_file_list:
            filename = single_file.split('/')[-1]
            df = pd.read_csv(filename)
            df = df[["Tweet id", "Tweet permalink", "time"]]
            df = df.rename(columns={"Tweet id": "postid", "Tweet permalink": "permalink", "time": "postdate"})
            if filename.find("Ben") != -1:
                df["service"] = "Bengali"
            if filename.find("Eng") != -1:
                df["service"] = "English"
            if filename.find("Ind") != -1:
                df["service"] = "Indonesian"
            if filename.find("Mal") != -1:
                df["service"] = "Malaysian"
            if filename.find("Phi") != -1:
                df["service"] = "Philippines"
            if filename.find("Tha") != -1:
                df["service"] = "Thai"
            for index, row in df.iterrows():
                postid = row["postid"]
                service = row["service"]
                permalink = row["permalink"]
                postdate = row["postdate"].split(" ")[0]
                curr = metadata_twitter_post(service=service, postid=postid, permalink=permalink, postdate=postdate)
                self._session.add(curr)
            try:
                self._session.commit()
            except:
                self._session.rollback()


