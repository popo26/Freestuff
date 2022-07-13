#FreeStuff is a website to exchange unwanted free stuff.

##Technology:
- Python 3
- Flask

##How to run this application:
1. Once clone or download this code, [create a virtualenv](https://docs.python.org/3/library/venv.html).
2. Acticate the virtualenv.
3. From terminal, install all the requirements with `pip install -r requirements.txt`.
4. I use [python-dotenv](https://pypi.org/project/python-dotenv/) to access environment variables.
5. Use `.env_example` file to populate settings required for python-dotenv above(see following instructions for environment variables to add).

##How to use this application:

##How to run tests(db insersion, hashed password creation, and slug creation):
- Run this command `python -m pytest tests/` in CLI.

##Database setup:
1. Comment Line 60 and 61 of app/__init__.py:
2. Enter following commands in CLI.
- `flask shell`
- `from app import db, fake`
- `from app.models import Role, User, Post, Photo`
3. Set roles.
- `Role.insert_roles()`
4. Add sample users and posts.
- `fake.users(20)`
- `fake.posts(30)`
- `exit()`
- `. dev_setup.sh`
- `flask run`

