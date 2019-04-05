from rfa_query.config import DATABASE_CONFIG
from sqlalchemy import create_engine

def get_engine():
    host = DATABASE_CONFIG['host']
    dbname = DATABASE_CONFIG['dbname']
    user = DATABASE_CONFIG['user']
    password = DATABASE_CONFIG['password']
    port = DATABASE_CONFIG['port']
    connnect_str = "mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host, port, dbname)
    engine = create_engine(connnect_str, echo=True)
    return engine