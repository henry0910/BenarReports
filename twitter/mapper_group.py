import core.config as config
import core.report as report
from database.mysql_writer import MySQLWriter
from twitter.link_mapper import TwitterLinkMapper


class TwitterMapperGroup(object):
    
    def __init__(self, year, month, language_list, environment=config.DEFAULT_ENV,
                 upload=False):
        
        self.mappers = []
        
        if year is not None and month is not None:
            
            self.report_segment = report.get_monthly_report(int(year), int(month)).segments[0]
            for language in language_list:
                self.mappers.append(TwitterLinkMapper(language, upload=upload))
            
        else:
            
            self.report_segment = None
            for language in language_list:
                self.mappers.append(TwitterLinkMapper(language, upload=upload))
        
        self.twitter_post_writer = MySQLWriter(environment, table=config.TWITTER_POST_TABLE)
        
        #self.skipped = 0
        #self.attempted = 0
        #self.successful = 0
        
        
    def map_posts(self, importcsv=False, upload=False):
        
        for mapper in self.mappers:
            
            if importcsv:
            
                post_filename = 'Twitter-%s' % mapper.language  # i.e. 'Twitter-English'
                
                # TODO: find out why this exists here, and remove it if it shouldn't;
                #       I've been doing loads manually, so this could create duplicate records
                self.twitter_post_writer.load_csv(post_filename, config.CSV_INPUT_DIR)
            
            if upload:
            
                mapper.map_posts(self.twitter_post_writer, self.report_segment)
            
            #self.skipped += mapper.updates_skipped
            #self.attempted += mapper.updates_attempted
            #self.successful += mapper.updates_successful
        
#        standard_msg = '%s out of %s attempts successful (%s skipped).' % (self.successful, self.attempted, self.skipped)
#        warning_msg = 'Did you mean to import CSV files first using the -i option?'
        
#        return '\n%s %s\n' % (standard_msg, warning_msg if self.attempted == 0 and self.skipped == 0 else '')
    
    
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
