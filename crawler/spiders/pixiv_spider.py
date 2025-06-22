from datetime import datetime, timezone
from urllib.parse import quote

import scrapy
from scrapy.http import JsonRequest

from crawler.items import IllustDetailItem, IllustImageItem, AuthorItem


class PixivSpider(scrapy.Spider):
    name = 'pixiv'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Referer': 'https://www.pixiv.net/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }

    def __init__(self, tag_str=None, phpsessid=None, **kwargs):
        super().__init__(**kwargs)
        self.tag_str = quote(tag_str, safe='')
        self.phpsessid = phpsessid

    def start_requests(self):
        start_url = f'https://www.pixiv.net/ajax/search/artworks/{self.tag_str}?order=date_d&mode=all&p=1&s_mode=s_tag&type=all&ai_type=0'
        cookies = {
            'PHPSESSID': self.phpsessid
        }
        yield JsonRequest(url=start_url, cookies=cookies, callback=self.parse,
                          meta={'tag_str': self.tag_str, 'page': 1})

    def parse(self, response, **kwargs):
        resp_data = response.json()['body']
        # 遍历检索结果列表
        for data in resp_data['illustManga']['data']:
            illust_code = data['id']
            # 请求作品详情
            detail_url = f'https://www.pixiv.net/ajax/illust/{illust_code}'
            yield JsonRequest(url=detail_url, callback=self.parse_illust_detail)
        # 请求下一页
        last_page = resp_data['illustManga']['lastPage']
        if response.meta['page'] < last_page:
            next_url = f'https://www.pixiv.net/ajax/search/artworks/{self.tag_str}?order=date_d&mode=all&p={response.meta["page"] + 1}&s_mode=s_tag&type=all&ai_type=0'
            yield JsonRequest(url=next_url, callback=self.parse,
                              meta={'tag_str': response.meta["tag_str"], 'page': response.meta["page"] + 1})

    def parse_illust_detail(self, response, **kwargs):
        resp_data = response.json()['body']
        illust_detail = IllustDetailItem(
            illust_code=resp_data['illustId'],
            illust_type=resp_data['illustType'],
            title=resp_data['title'],
            description=resp_data['description'],
            thumbnail_url=resp_data['urls']['thumb'],
            tags=[tag_obj['tag'] for tag_obj in resp_data['tags']['tags']],
            restrict=resp_data['xRestrict'],
            ai_type=resp_data['aiType'],
            width=resp_data['width'],
            height=resp_data['height'],
            page_count=resp_data['pageCount'],
            like_count=resp_data['likeCount'],
            bookmark_count=resp_data['bookmarkCount'],
            view_count=resp_data['viewCount'],
            create_time=datetime.fromisoformat(resp_data['createDate']).astimezone(timezone.utc),
            update_time=datetime.fromisoformat(resp_data['createDate']).astimezone(timezone.utc),
        )
        # 请求作者信息
        user_code = resp_data['userId']
        author_url = f'https://www.pixiv.net/ajax/user/{user_code}'
        yield JsonRequest(url=author_url, callback=self.parse_author, dont_filter=True,
                          meta={'illust_detail': illust_detail})

    def parse_author(self, response, **kwargs):
        illust_detail = response.meta['illust_detail']
        resp_data = response.json()['body']
        author = AuthorItem(
            user_code=resp_data['userId'],
            name=resp_data['name'],
            image_url=resp_data['image'],
        )
        illust_detail['author'] = author
        # 请求详情图片列表
        images_url = f'https://www.pixiv.net/ajax/illust/{illust_detail["illust_code"]}/pages'
        yield JsonRequest(url=images_url, callback=self.parse_illust_images,
                          meta={'illust_detail': illust_detail})

    def parse_illust_images(self, response, **kwargs):
        illust_detail = response.meta['illust_detail']
        illust_images = []
        resp_data = response.json()['body']
        for data in resp_data:
            illust_image = IllustImageItem(
                illust_code=illust_detail['illust_code'],
                mini_url=data['urls']['thumb_mini'],
                small_url=data['urls']['small'],
                regular_url=data['urls']['regular'],
                original_url=data['urls']['original'],
                width=data['width'],
                height=data['height'],
            )
            illust_images.append(illust_image)
        illust_detail['images'] = illust_images
        yield illust_detail
