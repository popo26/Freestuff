from sqlite3 import IntegrityError
from faker import Faker
from . import db
from .models import User, Post
from random import randint
import string

def users(count=20):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username = fake.user_name(),
                 password_hash = "test",
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 bio=fake.text(),
                 last_seen=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def posts(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(title = string.capwords(fake.bs()),
                 description = fake.text(),
                 timestamp = fake.past_date(),
                 giver=u)
        db.session.add(p)
    db.session.commit()
    #Slug LATER
    # for p in Post.query.all():
    #     p.generate_slug()

