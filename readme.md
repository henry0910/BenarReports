Rfa_Analytics

Project Folder to automate some of BenarNews metric reports steps

Getting Started

rfa_test_tables: orm models(don't modify it unless the database change)

rfa_sql_query: main script files do the query work including facebook and twitter query result and add new quarterly metric data into the metric_quarterly_by_item table. Besides, this file contain some test functions.

helper_function: some helper function for rfa_sql_query and can be used multiple times and there is no need to modify them

config.py: main script files to change parameters of metric reports. (Important)

Prerequisites

install below packages 
1. pymysql
2. sqlalchemy
3. pandas 
4. pytest 
5. glob 

(Other packages dependencies may be required)
