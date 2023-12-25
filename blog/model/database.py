from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from blog.extension import db


class Visitor(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ip: Mapped[str] = mapped_column(String(255))
    country: Mapped[str] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    banned: Mapped[bool] = mapped_column(Boolean, default=False)
    url: Mapped[str] = mapped_column(String(255))
    page_type: Mapped[str] = mapped_column(String(255), nullable=True)
    detail: Mapped[str] = mapped_column(String(255), nullable=True)

    @classmethod
    def create(cls, ip, url, page_type=None, detail=None, banned=False, country=None):
        new_visitor = Visitor(
            ip=ip,
            url=url,
            page_type=page_type,
            banned=banned,
            country=country,
            detail=detail,
        )
        db.session.add(new_visitor)
        db.session.commit()
        return Visitor.query.get(new_visitor.id)

    def to_dict(self):
        return dict(
            id=self.id,
            ip=self.ip,
            country=self.country,
            timestamp=self.timestamp,
            banned=self.banned,
            url=self.url,
            page_type=self.page_type,
            detail=self.detail,
        )


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    about: Mapped[str] = mapped_column(Text, nullable=True)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, username, password):
        password_hash = generate_password_hash(password)
        new_user = User(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return User.query.get(new_user.id)

    def to_dict(self):
        return dict(id=self.id, username=self.username, about=self.about)


class Category(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text, nullable=True)

    posts = relationship("Post", back_populates="category")

    @classmethod
    def create(cls, title, body=None):
        new_category = Category(title=title, body=body)
        db.session.add(new_category)
        db.session.commit()
        return Category.query.get(new_category.id)

    def update(self, title, body=None):
        self.title = title
        self.body = body
        db.session.add(self)
        db.session.commit()
        return Category.query.get(self.id)


class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"))

    category = relationship("Category", back_populates="posts")

    @classmethod
    def create(cls, title, body, category):
        new_post = Post(title=title, body=body, category=category)
        db.session.add(new_post)
        db.session.commit()
        return Post.query.get(new_post.id)

    def update(self, title, body, category):
        self.title = title
        self.body = body
        self.category = category
        self.updated = datetime.now()

        db.session.add(self)
        db.session.commit()
        return Post.query.get(self.id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            body=self.body,
            created=self.created,
            updated=self.updated,
            category_id=self.category_id,
        )
