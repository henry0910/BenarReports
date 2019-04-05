import core.config as config
import core.report as report
from database.mysql_writer import MySQLWriter
from facebook.link_mapper import FacebookLinkMapper


class FacebookMapperGroup(object):
    
    def __init__(self, year, month, language_list, environment=config.DEFAULT_ENV, end_date=None, verbosity=None):
        
        self.mappers = []
        
        if year is not None and month is not None:
            
            self.report_segment = report.get_monthly_report(int(year), int(month)).segments[0]
            for language in language_list:
                self.mappers.append(FacebookLinkMapper(language, end_date=end_date, verbosity=verbosity))
            
        else:
            
            self.report_segment = None
            for language in language_list:
                self.mappers.append(FacebookLinkMapper(language, fb_result_pages=1000,
                                                       end_date=end_date, verbosity=verbosity))
        
        self.facebook_page_writer = MySQLWriter(environment, table=config.FACEBOOK_PAGE_TABLE, verbosity=verbosity)
        self.facebook_post_writer = MySQLWriter(environment, table=config.FACEBOOK_POST_TABLE, verbosity=verbosity)
        
        self.skipped = 0
        self.attempted = 0
        self.successful = 0
        
        
    def map_posts(self, importcsv=False):
        
        for mapper in self.mappers:
            
            if importcsv:
            
                page_filename = '%s' % (mapper.language.lower()[0:3] + '_page')  # i.e. 'eng_page'
                post_filename = '%s' % (mapper.language.lower()[0:3] + '_post')
                
                # TODO: find out why these exists here, and remove them if they shouldn't;
                #       I've been doing loads manually, so these could create duplicate records
                self.facebook_page_writer.load_csv(page_filename, config.CSV_INPUT_DIR)
                self.facebook_post_writer.load_csv(post_filename, config.CSV_INPUT_DIR)
                
            mapper.map_posts(self.facebook_post_writer, self.report_segment)
            
            self.skipped += mapper.updates_skipped
            self.attempted += mapper.updates_attempted
            self.successful += mapper.updates_successful
        
        standard_msg = '%s out of %s attempts successful (%s skipped).' % (self.successful, self.attempted, self.skipped)
        warning_msg = 'Did you mean to import CSV files first using the -i option?'
        
        return '\n%s %s\n' % (standard_msg, warning_msg if self.attempted == 0 and self.skipped == 0 else '')
    
    
    # Not currently in use, but should be used eventually to add the
    # Facebook and Twitter export timestamps to the database instead of
    # adding them manually to *_timestamps.json
    def get_csv_export_time(filename, directory=config.CSV_REPORT_DIR):
        
        fileobj = open('%s/%s.csv' % (directory, filename))
        # read two lines, in order to skip the header
        csv_export_time = fileobj.readline()
        csv_export_time = fileobj.readline()
        fileobj.close()
        
        try:
            csv_export_time = csv_export_time.split(',')[-1]  # assumes csv_export_time is the final column
            return csv_export_time
        except IndexError:
            return None
