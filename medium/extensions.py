import logging

import scrapy
from twisted.internet import task


logger = logging.getLogger(__name__)


class LogDBStats(scrapy.extensions.logstats.LogStats):

    ''' Database Stasts'''

    def spider_opened(self, spider):
        spider.cur.execute('''
            SELECT COUNT(post_id)
            FROM post''')
        self.stats.set_value('total_posts', spider.cur.fetchone()[0])
        spider.cur.execute('''
            SELECT COUNT(post_id)
            FROM post
            WHERE available NOTNULL''')
        self.stats.set_value('already_updated_posts', spider.cur.fetchone()[0])

        self.task = task.LoopingCall(self.log, spider)
        self.task.start(self.interval)

    def log(self, spider):
        already_updated_posts = self.stats.get_value('already_updated_posts', 0)
        session_updated_posts = self.stats.get_value('item_scraped_count', 0)
        updated_posts = already_updated_posts + session_updated_posts
        total_posts = self.stats.get_value('total_posts', 0)
        update_percentage = updated_posts / total_posts * 100

        msg = (f'Updated posts {updated_posts}, '
               f'Total posts {total_posts}, '
               f'Update percentage {update_percentage:.2f} %')

        logger.info(msg, extra={'spider': spider})
