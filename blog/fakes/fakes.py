import random
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

from blog.extension import db
from blog.model.database import Category, Post, User, Visitor

fake = Faker()


def fake_user():
    User.create(
        username="username",
        password="password",
    )


def fake_category(count: int = 5):
    for _ in range(count):
        Category.create(
            title=fake.word(),
            body=fake.sentence(nb_words=20),
        )


def fake_post(count: int = 50):
    example_post = Path(__file__).parent.joinpath("example", "post.md")

    for _ in range(count):
        category = random.choice(Category.query.all())
        timestamp = fake.date_time_between(datetime(2023, 1, 1, 0, 0, 0))
        new_post = Post(
            title=fake.sentence(nb_words=15),
            body=example_post.read_text(),
            category=category,
            created=timestamp,
            updated=timestamp + timedelta(days=30),
        )
        db.session.add(new_post)
    db.session.commit()


def fake_visitor(count: int = 500):
    for _ in range(count):
        ip = fake.ipv4()
        post = random.choice(Post.query.all())
        url = f"/read/post/{post.id}"
        timestamp = fake.date_time_between(datetime(2023, 1, 1, 0, 0, 0))
        new_visitor = Visitor(
            ip=ip,
            url=url,
            timestamp=timestamp,
            page_type="post",
            detail=post.title,
        )
        db.session.add(new_visitor)
    db.session.commit()
