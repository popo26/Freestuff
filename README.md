# FreeStuff

## What this app does:
FreeStuff is a simple and intuitive app that provides a place to exchange unwanted free stuff.
[Demo site](https://demo-freestuff.herokuapp.com/)

## Technology:
- Python 3
- Flask

## Preparation:
1. Once clone or download this code, [create a virtualenv](https://docs.python.org/3/library/venv.html).
2. Acticate the virtualenv.
3. From terminal, install all the requirements with `pip install -r requirements.txt`.
4. Set up [AWS S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html). Fill related sections in the `.env_example` file.
5. I use [python-dotenv](https://pypi.org/project/python-dotenv/) to access environment variables.
6. Use `.env_example` file to populate settings required for python-dotenv above(see following instructions for environment variables to add).
7. SECRET_KEY, DANGEROUS_SECRET, and SALTIES need whatever keys you enter. e.g. SECRET_KEY=asidfwieidf;askjwiejfasdjfwiejfaskdljfawioejfadkjf.
7. If you don't have PostgreSQL installed on your computer, please refer to this [page](https://www.postgresql.org/docs/current/installation.html). Then add required information to `.env_example` file.
   e.g. DATABASE_URL=postgresql://*your_db_username*:*your_db_password*@localhost:5432/*your_db_name*
8. I use gmail for MAIL_USERNAME in .env_example. MAIL_PASSWORD uses App Password, which is different from your normal gmail password.
   Please find instructions for how to generate [App Password](https://support.google.com/mail/answer/185833?hl=en).

## Database setup:

1. Enter following commands in CLI.
- `flask shell`
- `from app import db, fake`
- `from app.models import Role, User, Post, Photo`
2. Set roles.
- `Role.insert_roles()`
3. Add sample users and posts.
- `fake.users(20)`
- `fake.posts(30)`
- `exit()`

## Run the app:
1. From terminal, run below commands to launch the site, then go to `127.0.0.1:5000`.:
- `export FLASK_APP=freestuff.py`
- `export FLASK_DEBUG=1`
- `export FLASK_ENV=development`
- `flask run`


## Run tests(db insersion, hashed password creation, and slug creation):
- Run this command `python -m pytest tests/` in CLI.

## Hightlights:
1. There are 2 search methods - Category search & Keyword search.
2. Only registered users are allowed to see members' profiles, sending and receiving messages about a post, and contacting FreeStuff admin.
3. Password reset is availiable by sending reset link at login screen or after an user logs in at Profile page.
4. Admin is allowed to edit user profiles and user posts in the site.
5. A new user needs to confirm a token email before login first time.
6. Emain notification will be sent when an user asks question and also receives an answer.






