from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class mapping_cmsid_rfapage(Base):
    __tablename__ = "mapping_cmsid_rfapage"

    id = Column(Integer, primary_key=True)
    service = Column(String)
    cmsid = Column(String)
    rfa_link = Column(String)

class mapping_link_rfapage(Base):
    __tablename__ = 'mapping_link_rfapage'

    id = Column(Integer, primary_key=True)
    external_link = Column(String)
    rfa_link = Column(String)


class mapping_theme_objective(Base):
    __tablename__ = "mapping_theme_objective"

    id = Column(Integer, primary_key=True)
    program = Column(String)
    theme = Column(String)
    objective1 = Column(String)
    objective2 = Column(String)
    objective3 = Column(String) 



class metadata_facebook_post(Base):
    __tablename__ = 'metadata_facebook_post'

    id = Column(Integer, primary_key=True)
    service = Column(String)
    postid = Column(String)
    permalink = Column(String)
    post_type = Column(String)
    postdate = Column(Date)
    program = Column(String)
    theme = Column(String)
    notes = Column(String)

class metadata_rfapage(Base):
    __tablename__ = "metadata_rfapage"

    id = Column(Integer, primary_key=True)
    service = Column(String)
    online_id = Column(String)
    program = Column(String)
    theme = Column(String)
    media_type = Column(String)
    pubdate = Column(Date)
    headline = Column(String)
    topic1 = Column(Date)
    topic2 = Column(Date)
    topic3 = Column(Date)
    topic4 = Column(Date)
    topic5 = Column(Date)

class metadata_twitter_post(Base):
    __tablename__ = "metadata_twitter_post"

    id = Column(Integer, primary_key = True)
    service = Column(String)
    postid = Column(String)
    permalink = Column(String)
    post_type = Column(String)
    postdate = Column(Date)
    program = Column(String)
    theme = Column(String)
    notes = Column(String)

class metric_daily_facebook_page(Base):
    __tablename__ = "metric_daily_facebook_page"

    id = Column(Integer, primary_key = True)
    language = Column(String)
    date = Column(Date)
    likes = Column(Integer)
    views = Column(Integer)
    clicks = Column(Integer)
    comments = Column(Integer)

class metric_lifetime_facebook_post(Base):
    __tablename__ = "metric_lifetime_facebook_post"

    id = Column(Integer, primary_key=True)
    postid = Column(String)
    views = Column(Integer)
    comments = Column(Integer)
    likes = Column(Integer)
    shares = Column(Integer)
    clicks = Column(Integer)
    csv_export_time = Column(Date)

class metric_lifetime_twitter_post(Base):
    __tablename__ = "metric_lifetime_twitter_post"

    id = Column(Integer, primary_key = True)
    service = Column(String)
    postid = Column(String)
    views = Column(Integer)
    likes = Column(Integer)
    retweets = Column(Integer)
    clicks = Column(Integer)
    csv_export_time = Column(Date)

class metric_monthly_naver_comments(Base):
    __tablename__ = "metric_monthly_naver_comments"

    id = Column(Integer, primary_key = True)
    comments = Column(Integer)
    headline = Column(String)
    year = Column(Integer)
    month = Column(Integer)

class metric_monthly_naver_likes(Base):
    __tablename__ = "metric_monthly_naver_likes"
    id = Column(Integer, primary_key = True)
    likes = Column(Integer)
    headline = Column(String)
    year = Column(Integer)
    month = Column(Integer)

class metric_monthly_naver_views(Base):
    __tablename__ = "metric_monthly_naver_views"

    id = Column(Integer, primary_key = True)
    views = Column(Integer)
    headline = Column(String)
    year = Column(Integer)
    month = Column(Integer)

class metric_quarterly_by_item(Base):
    __tablename__ = "metric_quarterly_by_item"

    id = Column(Integer, primary_key = True)
    platform = Column(String)
    service = Column(String)
    online_id = Column(String)
    year = Column(Integer)
    quarter = Column(Integer)
    metric = Column(String)
    value = Column(Integer)
    notes = Column(String)

class metric_quarterly_by_rfapage(Base):
    __tablename__ = "metric_quarterly_by_rfapage"

    id = Column(Integer, primary_key=True)
    rfa_link = Column(String)
    year = Column(Integer)
    quarter = Column(Integer)
    metric = Column(String)
    value = Column(Integer)
    notes = Column(String)

class metric_quarterly_summary(Base):

    __tablename__ = "metric_quarterly_summary"
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    quarter = Column(Integer)
    platform = Column(String)
    service = Column(String)
    program = Column(String)
    metric = Column(String)
    value = Column(Integer)
    notes = Column(String)

class metadata_report(Base):
    __tablename__ = 'metadata_report'
    id = Column(Integer, primary_key=True)
    first_day = Column(String)
    last_day = Column(String)
    initial_fb_snapshot = Column(String)
    final_fb_snapshot = Column(String)
    initial_tw_snapshot = Column(String)
    final_tw_snapshot = Column(String)



