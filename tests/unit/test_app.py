from app import create_app, current_app
from app.models import User
from app import db
from app.models import User, Role, Post, Photo, Message

#For creating dev-test.sqlite db line 97 and 98 in app/__init__.py needs to be commented.
def test_app_creation():
    app = current_app('testing')
    assert app


def test_database_insert():
    app = current_app('testing')
    assert app.config['TESTING']
    assert 'text.sqlite'
    app.app_context().push()
  
    db.create_all()
    Role.insert_roles()
    user = User(email='text@example.com', username='testuser')
    db.session.add(user)
    db.session.commit()

    db.session.remove()
    db.drop_all()

def test_hash_password_creation():
    app = current_app('testing')
    app.app_context().push()
    db.create_all()

    user = User()
    user.set_password('testpassword')
    user.verify_password('testpassword')
    assert True

    db.session.remove()
    db.drop_all()

def test_slug_creation():
    app = current_app('testing')
    app.app_context().push()
    db.create_all()
    post = Post(title="Test Title@Pytest")
    db.session.add(post)
    db.session.commit()
    post.generate_slug()
    assert post.slug == '1-test-title-pytest'

    db.session.remove()
    db.drop_all()
    



