import json

import scrapy

from medium.items import Post


class PostIdSpider(scrapy.Spider):

    ''' Crawl xml sitemap looking for post_id '''

    name = 'post_id'

    def start_requests(self):
        url = 'https://medium.com/sitemap/sitemap.xml'
        yield scrapy.Request(url, self.parse_sitemap)

    def parse_sitemap(self, response):
        s = scrapy.utils.sitemap.Sitemap(response.body)

        if s.type == 'sitemapindex':
            for loc in s:
                if self.url_filter() in loc['loc']:
                    yield scrapy.Request(
                        loc['loc'], callback=self.parse_sitemap
                    )
        elif s.type == 'urlset':
            for loc in s:
                post_id = loc['loc'].split('/')[-1].split('-')[-1]
                yield Post(post_id=post_id)

    def url_filter(self):
        url = '/posts/'
        if hasattr(self, 'year'):
            url += f'{self.year}/'
            if hasattr(self, 'month'):
                url += f'posts-{self.year}-{self.month}-'
                if hasattr(self, 'day'):
                    url += f'{self.day}'
        return url


class PostSpider(scrapy.Spider):

    ''' Exstract post data starting from post_id '''

    name = 'post'

    def start_requests(self):
        self.cur.execute(
            '''
            SELECT post_id
            FROM post
            WHERE creator_id is NULL'''
        )
        for post_id in self.cur.fetchall():
            url = f'https://medium.com/_/api/posts/{post_id[0]}'
            yield scrapy.Request(url, self.parse_post)

    def parse_post(self, response):
        data = json.loads(response.text[16:])

        if not data.get('success'):
            raise scrapy.exceptions.IgnoreRequest

        post = data['payload']['value']

        yield Post(
            post_id=post['id'],
            creator_id=post['creatorId'],
            language=post['detectedLanguage'],
            first_published_at=post['firstPublishedAt'],
        )

        # TODO handle requets (write middleware)
        # TODO content = post['content']
        # TODO virtuals = post['virtuals']
