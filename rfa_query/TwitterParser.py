from rfa_analytics.twitter_parse import TwitterParser
from config import TWITTER_PARSER
import os

if __name__ == "__main__":
    dir_path = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(dir_path, '..', 'twitter_download'))
    time = TWITTER_PARSER['time']
    tp = TwitterParser(path, time)
    print(tp.get_all_files())

