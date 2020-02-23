import logging
import sqlite3

import scrapy

logger = logging.getLogger(__name__)


class PostPipeline:
    def __init__(self, db):
        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        db = crawler.settings.get('DB')
        if not db:
            raise scrapy.exceptions.NotConfigured
        return cls(db)

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()

        if spider.name == 'post':
            spider.conn = self.conn
            spider.cur = self.cur

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if spider.name == 'post_id':
            self.insert_post_id(item)
            self.conn.commit()
        elif spider.name == 'post':
            self.update_post(item)
            self.insert_paragraphs(item)
            self.conn.commit()
        return item

    def insert_post_id(self, item):
        post_id = (item.get("post_id"),)
        self.cur.execute('SELECT * FROM post WHERE post_id=?', post_id)
        if self.cur.fetchone():
            logger.debug(f'Item already in database: {item.get("post_id")}')
        else:
            self.cur.execute('INSERT INTO post (post_id) VALUES (?)', post_id)
            logger.debug(f'Post id stored: {item.get("post_id")}')

    def update_post(self, item):
        post = (
            item.get('available'),
            item.get('creator_id'),
            item.get('language'),
            item.get('first_published_at'),
            item.get('title'),
            item.get('word_count'),
            item.get('tags'),
            item.get('post_id'),
        )
        self.cur.execute(
            '''
            UPDATE post
            SET available = ?, creator_id = ?, language = ?,
                first_published_at = ?,  title = ?,
                word_count = ?, tags = ?
            WHERE post_id = ? ''',
            post,
        )
        logger.debug(f'Post data updated: {item.get("post_id")}')

    def insert_paragraphs(self, item):
        post_id = item.get('post_id')

        if not item.get('available'):
            return

        for p in item.get('paragraphs'):
            paragraph = (
                post_id,
                p.get('index'),
                p.get('name'),
                p.get('type_'),
                p.get('text'),
            )
            self.cur.execute(
                '''
                INSERT INTO paragraph (post_id, "index", name, type, text)
                VALUES (?, ?, ?, ?, ?) ''',
                paragraph,
            )
            msg = (
                f'Paragraph insert (name - post_id):'
                f'{p.get("name")} - {item.get("post_id")}'
            )
            logger.debug(msg)
