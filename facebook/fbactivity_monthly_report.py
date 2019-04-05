import sys, os
sys.path.append(os.path.realpath('..'))

import core.config as config
import core.report as report
from database.mysql_writer import MySQLReader, MySQLWriter


# 1: select from facebook_page:

rpt = report.get_monthly_report(int(config.REPORT_YEAR), int(config.REPORT_MONTH))
prev_rpt = report.get_monthly_report(int(config.REPORT_YEAR), int(config.REPORT_MONTH) - 1)

reader = MySQLReader(config.REPORT_ENVIRONMENT, table=config.FACEBOOK_PAGE_TABLE)
writer = MySQLWriter(config.REPORT_ENVIRONMENT, table=config.MONTHLY_REPORT_TABLE)

views = reader.select_facebook_views(rpt.segments[0])
clicks = reader.select_facebook_clicks(rpt.segments[0])

# 2: insert to monthly_report:

header = ['`year`', '`month`', '`service`', '`metric`', '`value`', '`comment`']

data_rows = []

for service in config.REPORT_SERVICES.split(','):

    current_fans = reader.select_facebook_profile_likes_total(rpt.segments[0], language=service)
    prev_fans = reader.select_facebook_profile_likes_total(prev_rpt.segments[0], language=service)

    values = [
        current_fans - prev_fans if None not in [current_fans, prev_fans] else None,
        int([x for x in views if x[0] == service][0][1]),
        int([x for x in clicks if x[0] == service][0][1])
    ]

    for index, value in enumerate(values):
        if values[index] is not None:

            data_rows.append(["%s" % config.REPORT_YEAR,
                              "%s" % config.REPORT_MONTH,
                              "'%s'" % service,
                              "'%s'" % config.REPORT_METRICS.split(',')[index],
                              "%s" % values[index],
                              "''"])

writer.insert(header, data_rows)
