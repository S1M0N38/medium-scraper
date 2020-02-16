import logging
import sqlite3

logger = logging.getLogger(__name__)


class PostPipeline:
    def __init__(self, db_uri):
        self.db_uri = db_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(db_uri=crawler.settings.get('SQLITE_URI'))

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.db_uri)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        post_id = (item['post_id'],)
        self.cur.execute('SELECT * FROM post WHERE post_id=?', post_id)
        if self.cur.fetchone():
            logger.debug("Item already in database: %s" % item['post_id'])
        else:
            self.cur.execute('INSERT INTO post VALUES (?)', (item['post_id'],))
            logger.debug("Item stored: %s" % item['post_id'])
        return item
