import datetime

import core.config as config

    
class CustomQueryFilter(object):
    '''
    Stores a string which gets appended to the corresponding filter of a
    Google Analytics query before the query is executed.
    
    Using filter modifications is an alternative to creating near-duplicate
    copies of lots of GAQueryBase objects just to be able to change a single
    attribute in all of those queries.
    
    All CustomQueryFilter objects must be specific to a metric keyword
    (for code maintainability, multiple keywords per object are no longer supported).
    
    A CustomQueryFilter object may optionally be specific to a custom report,
    or to a webproperty (i.e. to break out Philippines data from the English webproperty).
    
    If replace=True, the custom filter will entirely replace the original filter.
    If replace=False, the custom filter will be appended to the original filter.
    '''
    def __init__(self, filter_string, metric_keyword,
                 report_keyword=None,
                 webproperty_id=None,
                 sub_webproperty_name=None,  # i.e. 'Philippines'
                 replace=False,
                 use_diff_metric=False,
                 effective_date=None,
                 termination_date=None):
        
        self.filter_string = filter_string
        self.metric_keyword = metric_keyword
        self.report_keyword = report_keyword
        self.webproperty_id = webproperty_id
        self.sub_webproperty_name = sub_webproperty_name
        self.replace = replace
        self.use_diff_metric = use_diff_metric
        self.effective_date = effective_date if effective_date is not None else config.EARLIEST_REPORT_DATE
        self.termination_date = termination_date if termination_date is not None else datetime.date.today()
