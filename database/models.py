from typing import List

from sqlalchemy import Integer, String, Table, Column, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped, relationship


class Base(DeclarativeBase):
    pass


illust_tag = Table(
    't_illust_tag',
    Base.metadata,
    Column('illust_id', ForeignKey('t_illust.id'), primary_key=True),
    Column('tag_id', ForeignKey('t_tag.id'), primary_key=True),
)


class Tag(Base):
    __tablename__ = 't_tag'
    __table_args__ = {'comment': '内容标签表'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='主键')
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='标签名称')
    website: Mapped[str] = mapped_column(String(50), nullable=False, comment='站点标识')

    def __repr__(self):
        return f"Tag(id={self.id}, website='{self.website}', name='{self.name}')"


class Illust(Base):
    __tablename__ = 't_illust'
    __table_args__ = {'comment': '作品表'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='主键')
    website: Mapped[str] = mapped_column(String(50), nullable=False, comment='站点标识')
    illust_code: Mapped[str] = mapped_column(String(50), nullable=False, comment='站点作品编码')
    illust_type: Mapped[str] = mapped_column(String(1), nullable=True, comment='作品类型 0:插画 1:漫画 2:动图')
    title: Mapped[str] = mapped_column(String(255), nullable=True, comment='作品标题')
    description: Mapped[str] = mapped_column(Text, nullable=True, comment='作品描述')
    thumbnail_url: Mapped[str] = mapped_column(String(255), nullable=True, comment='作品缩略图URL')
    tags: Mapped[List['Tag']] = relationship(secondary=illust_tag)
    restrict: Mapped[str] = mapped_column(String(1), nullable=True, comment='限制级别 0:公开 1:R18 2:R18G')
    ai_type: Mapped[str] = mapped_column(String(1), nullable=True, comment='AI类型 0:未知 1:非AI 2:AI')
    width: Mapped[int] = mapped_column(Integer, nullable=True, comment='作品宽度')
    height: Mapped[int] = mapped_column(Integer, nullable=True, comment='作品高度')
    page_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment='作品页数')
    like_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment='喜欢数')
    bookmark_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment='添加书签数')
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment='浏览数')
    author_id: Mapped[int] = mapped_column(ForeignKey('t_author.id'), nullable=False, comment='作者ID')
    author: Mapped['Author'] = relationship(back_populates='illusts')
    images: Mapped[List['IllustImage']] = relationship(back_populates='illust', cascade='save-update, merge')
    create_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                  comment='创建时间')
    update_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                  comment='更新时间')

    def __repr__(self):
        return f"Illust(id={self.id}, website='{self.website}', illust_code='{self.illust_code}', title='{self.title}')"


class Author(Base):
    __tablename__ = 't_author'
    __table_args__ = {'comment': '作者表'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='主键')
    website: Mapped[str] = mapped_column(String(50), nullable=False, comment='站点标识')
    user_code: Mapped[str] = mapped_column(String(50), nullable=False, comment='站点作者编码')
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='作者名称')
    image_url: Mapped[str] = mapped_column(String(255), nullable=True, comment='作者头像URL')
    illusts: Mapped[List['Illust']] = relationship(back_populates='author', cascade='save-update, merge')

    def __repr__(self):
        return f"Author(id={self.id}, website='{self.website}', user_code='{self.user_code}', name='{self.name}')"


class IllustImage(Base):
    __tablename__ = 't_illust_image'
    __table_args__ = {'comment': '作品图片表'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='主键')
    website: Mapped[str] = mapped_column(String(50), nullable=False, comment='站点标识')
    illust_id: Mapped[int] = mapped_column(ForeignKey('t_illust.id'), nullable=False, comment='作品ID')
    illust: Mapped['Illust'] = relationship(back_populates='images')
    mini_url: Mapped[str] = mapped_column(String(255), nullable=True, comment='作品缩略图URL')
    small_url: Mapped[str] = mapped_column(String(255), nullable=True, comment='作品小图URL')
    regular_url: Mapped[str] = mapped_column(String(255), nullable=True, comment='作品正图URL')
    original_url: Mapped[str] = mapped_column(String(255), nullable=True, comment='作品原图URL')
    width: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment='作品宽度')
    height: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment='作品高度')

    def __repr__(self):
        return f"IllustImage(id={self.id}, website='{self.website}', illust_id={self.illust_id}, small_url='{self.small_url}')"
