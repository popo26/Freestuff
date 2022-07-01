from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import datetime, timedelta
from app import create_app
import hashlib
import os


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

    #Check if can be used for saved emails
    # def email_hash(self):
    #     return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

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
    __searchable__ = ['title', 'description']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    category_type = db.Column(db.Integer)
    giver_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    messages = db.relationship("Message", backref=db.backref("question", cascade='all, delete'), lazy="dynamic")

    def __repr__(self):
        return '<Post:{}>'.format(self.title)


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
                # it's not so make a new one
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'))
    reply = db.Column(db.Boolean, default=False)

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


