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
        if spider.name == 'post_id':
            self.insert_post_id(item)
        elif spider.name == 'post':
            self.update_post(item)
            self.insert_content(item)
            self.insert_virtuals(item)
        return item

    def insert_post_id(self, item):
        post_id = (item['post_id'],)
        self.cur.execute('SELECT * FROM post WHERE post_id=?', post_id)
        if self.cur.fetchone():
            logger.debug(f'Item already in database: {item["post_id"]}')
        else:
            self.cur.execute('INSERT INTO post (post_id) VALUES (?)', post_id)
            logger.debug(f'Post id stored: {item["post_id"]}')

    def update_post(self, item):
        post = (
            item['creator_id'],
            item['language'],
            item['first_published_at'],
            item['post_id'],
        )
        self.cur.execute(
            '''
            UPDATE post
            SET creator_id = ?, language = ?, first_published_at = ?
            WHERE ID = ? ''',
            post,
        )
        logger.debug('Post data updated: {", ".join(post)}')

    def insert_content(self, item):
        pass

    def insert_virtuals(self, item):
        pass
