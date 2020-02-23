import json

import scrapy

from medium.items import Post, Paragraph


class PostSpider(scrapy.Spider):

    ''' Exstract post data starting from post_id '''

    name = 'post'
    handle_httpstatus_list = [302, 410]
    custom_settings = {'EXTENSIONS': {'medium.extensions.LogDBStats': 0}}

    def start_requests(self):
        self.cur.execute(
            '''
            SELECT post_id
            FROM post
            WHERE available is NULL'''
        )
        for post_id in self.cur.fetchall():
            url = f'https://medium.com/_/api/posts/{post_id[0]}'
            yield scrapy.Request(url, self.parse_post)

    def parse_post(self, response):
        code = response.status

        if code == 200:
            yield self._post_200(response)

        elif code == 302:
            yield self._post_302(response)

        elif code == 410:
            yield self._post_410(response)

        # add here other requests code if necessary

    def _post_200(self, response):
        data = json.loads(response.text[16:])
        post = data['payload']['value']

        paragraphs = []
        for par in post['content']['bodyModel']['paragraphs']:
            paragraphs.append(
                Paragraph(name=par['name'], type_=par['type'], text=par['text'])
            )

        tags = []
        for t in post['virtuals']['tags']:
            if t['type'] == 'Tag':
                tags.append(t['slug'])

        return Post(
            post_id=post['id'],
            available=1,
            creator_id=post['creatorId'],
            language=post['detectedLanguage'],
            first_published_at=post['firstPublishedAt'],
            title=post['title'],
            word_count=post['virtuals']['wordCount'],
            tags=','.join(tags),
            paragraphs=paragraphs,
        )

    def _post_302(self, response):
        post_id = response.url.split('/')[-1]
        self.logger.debug('The post {post_id} removed (user is blacklisted)')
        return Post(post_id=post_id, available=0)

    def _post_410(self, response):
        post_id = response.url.split('/')[-1]
        self.logger.debug('The post {post_id} removed (user removed it)')
        return Post(post_id=post_id, available=0)
