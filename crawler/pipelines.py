import logging

from sqlalchemy import select

from database.db import Session
from database.models import Author, Illust, Tag, IllustImage


class SavePixivDataPipeline:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def process_item(self, item, spider):
        if spider.name == 'pixiv':
            with Session() as session:
                with session.begin():
                    stmt = select(Illust).where(Illust.illust_code == item['illust_code'])
                    illust = session.scalars(stmt).first()
                    if illust is None:
                        # 保存标签
                        tag_str_list = item['tags']
                        existing_tags = session.scalars(
                            select(Tag).where(Tag.name.in_(tag_str_list))
                        ).all()
                        existing_tag_names = {tag.name for tag in existing_tags}
                        tags = list(existing_tags)
                        for tag_str in tag_str_list:
                            if tag_str not in existing_tag_names:
                                tag = Tag(website='pixiv', name=tag_str)
                                session.add(tag)
                                tags.append(tag)
                                self.log.info(f'Saved tag [{tag.name}] to database')
                        # 保存作者
                        author_item = item['author']
                        stmt = select(Author).where(Author.user_code == author_item['user_code'])
                        author = session.scalars(stmt).first()
                        if author is None:
                            author = Author(
                                website='pixiv',
                                user_code=author_item['user_code'],
                                name=author_item['name'],
                                image_url=author_item['image_url'],
                            )
                            session.add(author)
                            self.log.info(f'Saved author [{author.name}] to database')
                        # 保存作品
                        illust = Illust(
                            website='pixiv',
                            illust_code=item['illust_code'],
                            illust_type=item['illust_type'],
                            title=item['title'],
                            description=item['description'],
                            thumbnail_url=item['thumbnail_url'],
                            tags=tags,
                            restrict=item['restrict'],
                            ai_type=item['ai_type'],
                            width=item['width'],
                            height=item['height'],
                            page_count=item['page_count'],
                            like_count=item['like_count'],
                            bookmark_count=item['bookmark_count'],
                            view_count=item['view_count'],
                            author=author,
                            create_time=item['create_time'],
                            update_time=item['update_time'],
                        )
                        session.add(illust)
                        self.log.info(f'Saved illust [{illust.title}] to database')
                        # 保存图片
                        for image_item in item['images']:
                            illust_image = IllustImage(
                                website='pixiv',
                                illust=illust,
                                mini_url=image_item['mini_url'],
                                small_url=image_item['small_url'],
                                regular_url=image_item['regular_url'],
                                original_url=image_item['original_url'],
                                width=image_item['width'],
                                height=image_item['height'],
                            )
                            session.add(illust_image)
                            self.log.info(f'Saved illust image [{illust_image.small_url}] to database')
        return item
