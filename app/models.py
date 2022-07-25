from . import db, login_manager
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin, current_user
from datetime import datetime, timedelta
from app import create_app
import hashlib
import os
import re
from itsdangerous import SignatureExpired, URLSafeTimedSerializer as Serializer


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    bio = db.Column(db.Text())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship("Post", backref="giver", lazy="dynamic")
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    messages = db.relationship("Message", backref="asker", lazy="dynamic")
    question_received = db.Column(db.Integer, nullable=False, default=0)
    question_answered = db.Column(db.Integer, nullable=False, default=0)
   
   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.email == os.getenv("MAIL_USERNAME"):
            self.role = Role.query.filter_by(name="Administrator").first()
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    #for last_seen
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username }>"

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    #Check if can be used for saved emails #Future idea
    # def email_hash(self):
    #     return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({"user_id":self.id})
 
        

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=300)['user_id']
        except SignatureExpired:
            return "The token link is expired"
        except:
            return None
        return User.query.get(user_id)



class Category:
    HOME_LIVING = 1
    KITCHEN = 2
    BABY = 3
    BOOKS = 4
    CRAFT = 5
    ELECTRONICS = 6
    PETS = 7
    CLOTHING = 8
    BATHROOM = 9
    TOYS = 10
    JEWELLERY = 11

class Post(db.Model):
    __tablename__ = 'posts'
    # __searchable__ = ['title', 'description'] for flask-msearch
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    category_type = db.Column(db.Integer)
    giver_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    messages = db.relationship("Message", backref=db.backref("question", cascade='all, delete'), lazy="dynamic")
    photos = db.Column(db.String(40), default='cart.jpg')
    photoss = db.relationship("Photo", backref=db.backref("post", cascade='all, delete-orphan', single_parent=True), lazy="dynamic")
    slug = db.Column(db.String(126), unique=True, index=True)

    def generate_slug(self):
        self.slug = f"{self.id}-" + re.sub(r'[^\w]+', '-', self.title.lower())
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Post:{}>'.format(self.title)


class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    photo_one_name = db.Column(db.String(100), default='default')
    photo_one = db.Column(db.String(40), default='cart.jpg')
    photo_two_name = db.Column(db.String(100), default='default')
    photo_two = db.Column(db.String(40), default='cart.jpg')
    photo_three_name = db.Column(db.String(100), default='default')
    photo_three = db.Column(db.String(40), default='cart.jpg')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return '<Photo:{}>'.format(self.id)

class Permission:
    FOLLOW = 1
    REVIEW = 2
    PUBLISH = 4
    ADMIN = 8

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref='role', lazy='dynamic')   

    #overwrite Role class
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return f"<Role {self.name}>"

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

#This is handy to run by Role.insert_roles() when freshly start a db

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW,
                     Permission.REVIEW,
                     Permission.PUBLISH],

            'Administrator': [Permission.FOLLOW,
                              Permission.REVIEW,
                              Permission.PUBLISH,
                              Permission.ADMIN],
        }
        
        default_role = 'User'
        for r in roles:
            # see if role is already in table
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            # add whichever permissions the role needs
            for perm in roles[r]:
                role.add_permission(perm)
            # if role is the default one, default is True
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_administrator(self):
        return False

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, index=True)
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))#not working when i use db.session.delete
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'))
    reply = db.Column(db.Boolean, default=False)
    replied = db.Column(db.Boolean, default=False)
    read = db.Column(db.Boolean, default=False)
    answered_user = db.Column(db.Integer, default=0)
    answered_user2 = db.Column(db.String(64), index=True, default=0)

    def get_slug_for_post_related_to_message(self):
        post = Post.query.filter_by(id = self.post_id).first()
        return post.slug
 
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





