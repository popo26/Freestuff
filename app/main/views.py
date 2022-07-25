import datetime
import smtplib
from operator import or_
import secrets
from PIL import Image
from flask import render_template, flash, redirect, request, url_for, current_app, session, send_file
from flask_login import login_required, current_user, fresh_login_required
from app.main.forms import (AdminLevelEditProfileForm, ContactGiverForm, EditProfileForm, 
                            PostForm, ReplyForm, PhotoForm, SearchForm, ContactAdminForm)
from . import main
from app.models import User, Post
from app import db
from ..decorators import permission_required, admin_required
from ..models import Permission, Category, Message, Photo
from app import config
from app.email import send_email
from config import Config
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from base64 import b64encode
import boto3

load_dotenv()


def save_photos(form_photos):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_photos.filename)
    photos_fn = random_hex + f_ext
    photos_path = os.path.join(current_app.root_path, 'static/uploads', photos_fn)
    bucket_name = current_app.config['S3_BUCKET_NAME']
    s3 = boto3.resource('s3')
    
    output_size = (500, 500)
    i = Image.open(form_photos)
    i.thumbnail(output_size)
    i.save(photos_path)
    
    s3.meta.client.upload_file(photos_path, bucket_name, photos_fn)
    
    return photos_fn

#Serve image from S3
@main.route('/download/<resource>')
def download_image(resource):
    """ resource: name of the file to download"""
    s3 = boto3.client('s3',
                      aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])

    url = s3.generate_presigned_url('get_object', Params = {'Bucket': current_app.config['S3_BUCKET_NAME'], 'Key': resource}, ExpiresIn = 100)
    return redirect(url, code=302)

@main.route("/", methods=['GET', "POST"])
def index():
    posts = Post.query.all()
    posts_count = Post.query.count()
    
    #Pagination
    page = request.args.get('page', 1, type=int)
    pagination = \
        Post.query.order_by(Post.timestamp.desc()).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/index.html", 
                            posts=posts, 
                            pagination=pagination,
                            posts_count = posts_count,
                            )

@main.context_processor
def base():
    form = SearchForm()
    YEAR = datetime.datetime.now().year
    return dict(form=form, year=YEAR) 

@main.route("/search", methods=['POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():        
        post_query = form.query.data
        results = db.session.query(Post).filter(or_(Post.title.ilike('%' + post_query + '%'), \
                                                (Post.description.ilike('%' + post_query + '%')))).all()
       
        page = request.args.get('page', 1, type=int)
        pagination = \
            db.session.query(Post).filter \
                (or_(Post.title.ilike('%' + post_query + '%'), \
                (Post.description.ilike('%' + post_query + '%')))).paginate(
                page,
                per_page=current_app.config['POSTS_PER_PAGE'],
                error_out=False
            )
        posts = pagination.items
        return render_template('main/search.html', 
                                results=results, 
                                keyword=post_query,
                                pagination=pagination, 
                                posts=posts,
                                )


@main.route("/home-living")
def home_living():
    items = Post.query.filter_by(category_type=Category.HOME_LIVING)
    category="Home&Living"
    page = request.args.get('page', 1, type=int)
   
    pagination = \
        Post.query.filter_by(category_type=Category.HOME_LIVING).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/per_category.html", 
                            items=items, 
                            pagination=pagination,
                            posts=posts,
                            category=category,
                            )

@main.route("/kitchen")
def kitchen():
    items = Post.query.filter_by(category_type=Category.KITCHEN)
    category="Kitchen"
    page = request.args.get('page', 1, type=int)

    pagination = \
        Post.query.filter_by(category_type=Category.KITCHEN).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/per_category.html", 
                            items=items, 
                            pagination=pagination,
                            posts=posts,
                            category=category,
                            )
@main.route("/baby")
def baby():
    items = Post.query.filter_by(category_type=Category.BABY)
    category="Baby"
    page = request.args.get('page', 1, type=int)
    
    pagination = \
        Post.query.filter_by(category_type=Category.BABY).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/per_category.html", 
                            items=items, 
                            pagination=pagination,
                            posts=posts,
                            category=category,
                            )

@main.route("/books")
def books():
    items = Post.query.filter_by(category_type=Category.BOOKS)
    category="Books"
    page = request.args.get('page', 1, type=int)

    pagination = \
        Post.query.filter_by(category_type=Category.BOOKS).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/per_category.html", 
                            items=items, 
                            pagination=pagination,
                            posts=posts,
                            category=category,
                            )

@main.route("/craft")
def craft():
    items = Post.query.filter_by(category_type=Category.CRAFT)
    category="Craft"
    page = request.args.get('page', 1, type=int)

    pagination = \
        Post.query.filter_by(category_type=Category.CRAFT).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/per_category.html", 
                            items=items, 
                            pagination=pagination,
                            posts=posts,
                            category=category,
                            )

@main.route("/electronics")
def electronics():
    items = Post.query.filter_by(category_type=Category.ELECTRONICS)
    category="Electronics"
    page = request.args.get('page', 1, type=int)

    pagination = \
        Post.query.filter_by(category_type=Category.ELECTRONICS).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/per_category.html", 
                            items=items, 
                            pagination=pagination,
                            posts=posts,
                            category=category,
                            )

@main.route("/pets")
def pets():
    items = Post.query.filter_by(category_type=Category.PETS)
    category="Pets"
    page = request.args.get('page', 1, type=int)

    pagination = \
        Post.query.filter_by(category_type=Category.PETS).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/per_category.html", 
                            items=items, 
                            pagination=pagination,
                            posts=posts,
                            category=category,
                            )

@main.route("/clothing")
def clothing():
    items = Post.query.filter_by(category_type=Category.CLOTHING)
    category="Clothing"
    page = request.args.get('page', 1, type=int)

    pagination = \
        Post.query.filter_by(category_type=Category.CLOTHING).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/per_category.html", 
                            items=items, 
                            pagination=pagination,
                            posts=posts,
                            category=category,
                            )

@main.route("/bathroom")
def bathroom():
    items = Post.query.filter_by(category_type=Category.BATHROOM)
    category="Bathroom"
    page = request.args.get('page', 1, type=int)

    pagination = \
        Post.query.filter_by(category_type=Category.BATHROOM).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/per_category.html", 
                            items=items, 
                            pagination=pagination,
                            posts=posts,
                            category=category,
                            )

@main.route("/toys")
def toys():
    items = Post.query.filter_by(category_type=Category.TOYS)
    category="Toys"
    page = request.args.get('page', 1, type=int)

    pagination = \
        Post.query.filter_by(category_type=Category.TOYS).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/per_category.html", 
                            items=items, 
                            pagination=pagination,
                            posts=posts,
                            category=category,
                            )

@main.route("/jewellery")
def jewellery():
    items = Post.query.filter_by(category_type=Category.JEWELLERY)
    category="Jewellery"
    page = request.args.get('page', 1, type=int)

    pagination = \
        Post.query.filter_by(category_type=Category.JEWELLERY).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/per_category.html", 
                            items=items, 
                            pagination=pagination,
                            posts=posts,
                            category=category,
                            )


@main.route('/item/<slug>')
def each_slug_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    messages = Message.query.filter_by(post_id=post.id).all()
    photos = Photo.query.filter_by(post_id=post.id).first()
  
    if photos == None:
        img1 = url_for('main.download_image', resource='cart.jpg')
    else:
        img1 = url_for('main.download_image', resource=photos.photo_one)
    if photos == None:
        img2 = url_for('main.download_image', resource='cart.jpg')
    else:
        img2 = url_for('main.download_image', resource=photos.photo_two)
    if photos == None:
        img3 = url_for('main.download_image', resource='cart.jpg')
    else:
        img3 = url_for('main.download_image', resource=photos.photo_three)
   

    return render_template("main/each_slug_post.html", 
                            post=post, 
                            messages=messages, 
                            img1=img1,
                            img2=img2,
                            img3=img3,
                            )
    

@main.route("/post-new-item", methods=['GET', "POST"])
@fresh_login_required
# @login_required
def post_new_item():
    form = PostForm()
    p_form = PhotoForm()
    last_photo_id = Photo.query.order_by(Photo.id.desc()).first()

    if current_user.can(Permission.PUBLISH) \
        and form.validate_on_submit() \
        and p_form.validate_on_submit():
        if p_form.photo_one.data\
            or p_form.photo_two.data\
            or p_form.photo_three.data:
            if p_form.photo_one.data:
                photo_file_one = save_photos(p_form.photo_one.data)
                p_form.photo_one = photo_file_one
            else:
                photo_file_one = None
                p_form.photo_one = photo_file_one

            if p_form.photo_two.data:   
                photo_file_two = save_photos(p_form.photo_two.data)
                p_form.photo_two = photo_file_two
            else:
                photo_file_two = None
                p_form.photo_two = photo_file_two  

            if p_form.photo_three.data:
                photo_file_three = save_photos(p_form.photo_three.data)
                p_form.photo_three = photo_file_three
            else:
                photo_file_three = None
                p_form.photo_three = photo_file_three
              
            photo = Photo(photo_one=p_form.photo_one,
                        photo_two=p_form.photo_two,
                        photo_three=p_form.photo_three, 
                        photo_one_name=p_form.photo_one,
                        photo_two_name=p_form.photo_two,
                        photo_three_name=p_form.photo_three,)

        else:
            photo_file_one = None
            p_form.photo_one = photo_file_one
            photo_file_two = None
            p_form.photo_two = photo_file_two  
            photo_file_three = None
            p_form.photo_three = photo_file_three

            photo = Photo(id = last_photo_id.id + 1,
                    photo_one=p_form.photo_one,
                    photo_two=p_form.photo_two,
                    photo_three=p_form.photo_three, 
                    photo_one_name=p_form.photo_one,
                    photo_two_name=p_form.photo_two,
                    photo_three_name=p_form.photo_three,)

        post = Post(category_type=form.category.data,
            title=form.title.data,
            description=form.description.data,
            giver=current_user._get_current_object(),
            photos=p_form.photo_one)

        db.session.add(post)
        db.session.commit()
        photo.post_id = post.id
        db.session.add(photo)
        db.session.commit()

        post.generate_slug()

        flash("Thank you for posting a new free stuff!")
        return redirect(url_for('.index'))
    return render_template("main/post-new-item.html", form=form, p_form=p_form)


@main.route("/item/<int:item_id>/edit-post", methods=['GET', 'POST'])
@fresh_login_required
# @login_required
def edit_post(item_id):
    form = PostForm()
    p_form = PhotoForm()
    item = Post.query.filter_by(id=item_id).first()
    photos = Photo.query.filter_by(post_id=item_id).first()

    bucket_name = current_app.config['S3_BUCKET_NAME']
    bucket_path = current_app.config['S3_BUCKET_PATH']
    s3 = boto3.resource('s3')  
    s3_bucket = s3.Bucket(bucket_name)
    s3_client = boto3.client('s3')
        
    if form.validate_on_submit()\
        and p_form.validate_on_submit():
    
        if p_form.photo_one.data\
            or p_form.photo_two.data\
            or p_form.photo_three.data:

            if p_form.photo_one.data == None\
                and photos.photo_one:
                pass

            elif p_form.photo_one.data\
                 and p_form.photo_one.data != photos.photo_one\
                 and photos.photo_one == 'cart.jpg':
          
                photo_file_one = save_photos(p_form.photo_one.data)
                p_form.photo_one = photo_file_one
                photos.photo_one = photo_file_one
                photos.photo_one_name = photo_file_one
            
            elif p_form.photo_one.data\
                 and p_form.photo_one.data != photos.photo_one\
                 and photos.photo_one != 'cart.jpg':
                old_photo_one_path = os.path.join('app/static/uploads', photos.photo_one)
                os.remove(old_photo_one_path)
                s3_client.delete_object(Bucket=bucket_name, Key=photos.photo_one)
                photo_file_one = save_photos(p_form.photo_one.data)
                p_form.photo_one = photo_file_one
                photos.photo_one = photo_file_one
                photos.photo_one_name = photo_file_one

            else:
                photo_file_one = None
                p_form.photo_one = photo_file_one

            if p_form.photo_two.data == None\
                and photos.photo_two:
                pass

            elif p_form.photo_two.data\
                 and p_form.photo_two.data != photos.photo_two\
                 and photos.photo_two == 'cart.jpg':
            
                photo_file_two = save_photos(p_form.photo_two.data)
                p_form.photo_two = photo_file_two
                photos.photo_two = photo_file_two
                photos.photo_two_name = photo_file_two
                
            elif p_form.photo_two.data\
                 and p_form.photo_two.data != photos.photo_two\
                 and photos.photo_two != 'cart.jpg': 
                old_photo_two_path = os.path.join('app/static/uploads', photos.photo_two)
                os.remove(old_photo_two_path)
                s3_client.delete_object(Bucket=bucket_name, Key=photos.photo_two) 
                photo_file_two = save_photos(p_form.photo_two.data)
                p_form.photo_two = photo_file_two
                photos.photo_two = photo_file_two
                photos.photo_two_name = photo_file_two
                
            else:
                photo_file_two = None
                p_form.photo_two = photo_file_two

            if p_form.photo_three.data == None\
                and photos.photo_three:
                pass

            elif p_form.photo_three.data\
                 and p_form.photo_three.data != photos.photo_three\
                 and photos.photo_three == 'cart.jpg':
             
                photo_file_three = save_photos(p_form.photo_three.data)
                p_form.photo_three = photo_file_three
                photos.photo_three = photo_file_three
                photos.photo_three_name = photo_file_three

            elif p_form.photo_three.data\
                 and p_form.photo_three.data != photos.photo_three\
                 and photos.photo_three != 'cart.jpg':
                old_photo_three_path = os.path.join('app/static/uploads', photos.photo_three)
                os.remove(old_photo_three_path)
                s3_client.delete_object(Bucket=bucket_name, Key=photos.photo_three) 
                photo_file_three = save_photos(p_form.photo_three.data)
                p_form.photo_three = photo_file_three
                photos.photo_three = photo_file_three
                photos.photo_three_name = photo_file_three
                
            else:
                photo_file_three = None
                p_form.photo_three = photo_file_three

        item.photos = photos.photo_one
       
        if item.photos:
            item.photos == photos.photo_one
    
        elif not item.photos:
            item.photos = 'cart.jpg'
        
        elif item.photos == 'cart.jpg':
            if photo_file_one == None:
                item.photos == 'cart.jpg'
            elif photo_file_one:
                item.photos == photo_file_one
            else:
                item.photos == photo_file_one
        else:
            item.photos == photo_file_one
            
        item.title = form.title.data
        item.description = form.description.data
        item.category_type = form.category.data
   
        db.session.add(photos)
        db.session.add(item)
        db.session.commit()

        item.generate_slug()

        flash("Successfully updated!", 'success')
        return redirect(url_for('.each_slug_post', slug=item.slug))
    
    form.title.data = item.title
    form.category.data = item.category_type
    form.description.data = item.description 
 

    if photos:
        p_form.photo_one_name.data = photos.photo_one
        p_form.photo_two_name.data = photos.photo_two
        p_form.photo_three_name.data = photos.photo_three
    else:
        p_form.photo_one.data = None
        p_form.photo_two.data = None
        p_form.photo_three.data = None
        
    return render_template("main/edit-post.html", form=form, p_form=p_form, item=item)

@main.route('/delete/<int:item_id>/photo', methods=["GET", "POST"])
@fresh_login_required
# @login_required
def delete_all_photos(item_id):
    item = Post.query.filter_by(id=item_id).first()
    photos = Photo.query.filter_by(post_id=item.id)

    bucket_name = current_app.config['S3_BUCKET_NAME']
    bucket_path = current_app.config['S3_BUCKET_PATH']
    s3 = boto3.resource('s3')  
    s3_bucket = s3.Bucket(bucket_name)
    s3_client = boto3.client('s3')

    for p in photos:
        if p.photo_one:
            photo1_path = os.path.join('app/static/uploads', p.photo_one)
            
            if os.path.exists(photo1_path):
                if photo1_path == os.path.join('app/static/uploads', 'cart.jpg'):
                    pass
                else:
                    os.remove(photo1_path)
                    s3_client.delete_object(Bucket=bucket_name, Key=p.photo_one)
            p.photo_one = 'cart.jpg'
            p.photo_one_name = 'default'
            db.session.commit()
        if p.photo_two:
            photo2_path = os.path.join('app/static/uploads', p.photo_two)
        
            if os.path.exists(photo2_path):
                if photo2_path == os.path.join('app/static/uploads', 'cart.jpg'):
                    pass
                else:
                    os.remove(photo2_path)
                    s3_client.delete_object(Bucket=bucket_name, Key=p.photo_two)
            p.photo_two = 'cart.jpg'
            p.photo_two_name = 'default'
            db.session.commit()
        if p.photo_three:
            photo3_path = os.path.join('app/static/uploads', p.photo_three)
            # photo3_path_s3 = os.path.join(bucket_path, p.photo_three)
            if os.path.exists(photo3_path):
                if photo3_path == os.path.join('app/static/uploads', 'cart.jpg'):
                    pass
                else:
                    os.remove(photo3_path)
                    s3_client.delete_object(Bucket=bucket_name, Key=p.photo_three)
            p.photo_three = 'cart.jpg'
            p.photo_three_name = 'default'
            db.session.commit()
    
        item.photos = p.photo_one
        db.session.add(item)
        db.session.commit()

    return redirect(url_for('main.edit_post', item_id=item.id))



@main.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
@fresh_login_required
# @login_required
def delete_post(item_id):
    photos = Photo.query.filter_by(post_id=item_id).first()
    
    #delete files from static folder
    photo1_path = os.path.join('app/static/uploads', photos.photo_one)
    photo2_path = os.path.join('app/static/uploads', photos.photo_two)
    photo3_path = os.path.join('app/static/uploads', photos.photo_three)
    
    bucket_name = current_app.config['S3_BUCKET_NAME']
    bucket_path = current_app.config['S3_BUCKET_PATH']
    s3 = boto3.resource('s3')  
    s3_bucket = s3.Bucket(bucket_name)
    s3_client = boto3.client('s3')

    if os.path.exists(photo1_path):
        if photo1_path == os.path.join('app/static/uploads', 'cart.jpg'):
            pass
        else:
            os.remove(photo1_path)
            s3_client.delete_object(Bucket=bucket_name, Key=photos.photo_one)
    
    if os.path.exists(photo2_path):
        if photo2_path == os.path.join('app/static/uploads', 'cart.jpg'):
            pass
        else:
            os.remove(photo2_path)
            s3_client.delete_object(Bucket=bucket_name, Key=photos.photo_two)

    if os.path.exists(photo3_path):
        if photo3_path == os.path.join('app/static/uploads', 'cart.jpg'):
            pass
        else:
            os.remove(photo3_path)
            s3_client.delete_object(Bucket=bucket_name, Key=photos.photo_three)

    post = Post.query.filter_by(id=item_id).first()
    related_messages = Message.query.filter(Message.post_id==post.id)
    for m in related_messages:
        if m.replied == False and m.reply == False:
            posted_user = User.query.filter_by(id=current_user.id).first()
            posted_user.question_received -= 1
            if posted_user.question_received < 0:
                posted_user.question_received = 0
            db.session.add(posted_user)
            db.session.commit()
        if m.read == False and m.reply==True:
            answered_user = User.query.filter_by(id=m.answered_user).first()
            answered_user.question_answered -= 1 
            if answered_user.question_received < 0:
                answered_user.question_received = 0
            db.session.add(answered_user)
            db.session.commit()       

    Photo.query.filter_by(post_id=item_id).delete()
    Post.query.filter_by(id=item_id).delete()
    db.session.commit()
    html = render_template('mail/admin_post_deleted.html', user=current_user)
    send_email(os.getenv('MAIL_USERNAME'), "A post deleted", html)
    
    flash("Selected item is deleted.")
    return redirect(url_for("main.user", username=current_user.username))
    

@main.route('/item/<int:item_id>/reply/<int:message_id>', methods=['GET', 'POST'])
def reply(item_id, message_id):
    form = ReplyForm()
    item = Post.query.filter_by(id=item_id).first()
    if form.validate_on_submit():
        message = Message(description=request.form.get('description'),
                          user_id=current_user.id,
                          post_id=item.id,
                          reply=True,
                          replied=True,
                          )
        db.session.add(message)
        db.session.commit()
       
        original_message = Message.query.filter_by(id=message_id).first()
        original_message.replied = True
        original_message.read = True
        message.answered_user = original_message.asker.id
        message.answered_user2 = original_message.asker.username
        db.session.add(message)
        original_message.asker.question_answered += 1
        db.session.add(original_message)
        current_user.question_received -= 1
        if current_user.question_received < 0:
            current_user.question_received = 0
        db.session.add(current_user)
        db.session.commit()

        link = url_for('main.each_slug_post', _external=True, slug=item.slug)
        html = render_template('mail/user_answer_received.html', asker=original_message.asker, link=link, item=item)
        send_email(original_message.asker.email, "You received an answer!", html)
        flash(f'We sent an email to notify {original_message.asker.username}.')
        return redirect(url_for('main.each_slug_post', slug=item.slug, message_id=message.id))
    
    return render_template('main/reply.html', item=item, form=form)

@main.route('/item/<int:item_id>/replied/<int:message_id>', methods=['GET', 'POST'])
def mark_as_replied(item_id, message_id):
    replied_message = Message.query.filter_by(id=message_id).first()
    item = Post.query.filter_by(id=item_id).first()
    replied_message.replied = True
    db.session.add(replied_message)
    item.giver.question_received -= 1
    if item.giver.question_received < 0:
        item.giver.question_received = 0
    replied_message.read = True
    db.session.add(replied_message)
    db.session.add(item)
    db.session.commit()
    
    return redirect(url_for('main.check_messages', username=current_user.username))

@main.route('/item/<int:item_id>/answered/<int:message_id>', methods=['GET', 'POST'])
def mark_as_read(item_id, message_id):
    answered_message = Message.query.filter_by(id=message_id).first()
    item = Post.query.filter_by(id=item_id).first()
    current_user.question_answered -=1
    if current_user.question_answered < 0:
        current_user.question_answered = 0
    answered_message.read = True
    db.session.add(current_user)
    db.session.add(answered_message)
    db.session.commit()
    return redirect(url_for('main.check_messages', username=current_user.username))

@main.route("/contact-giver/<int:item_id>", methods=["GET", "POST"])
@login_required
def contact_giver(item_id):
    form = ContactGiverForm()
    item = Post.query.filter_by(id=item_id).first()
    
    if form.validate_on_submit():
        message = Message(description=request.form.get("description"), 
                          user_id=current_user.id, 
                          post_id=item.id)        
        item.giver.question_received += 1
        
        db.session.add(message)
        db.session.add(item)
        db.session.commit()

        link = url_for('main.each_slug_post', _external=True, slug=item.slug)
        html = render_template('mail/user_question_recieved.html', giver=item.giver, link=link, item=item)
        send_email(item.giver.email, "You received a question!", html)
        flash("successfully submitted!")
        return redirect(url_for("main.each_slug_post", slug=item.slug))
   
    return render_template("main/contact-giver.html", form=form, item=item)


@main.route("/messages/<username>")
@login_required
def check_messages(username):
    messages = Message.query.filter(Message.replied==False)
    posts = Post.query.filter_by(giver=current_user)  
    posted_questions = Message.query.filter(Message.answered_user==current_user.id, 
                                            Message.reply==True,
                                            Message.replied==True, 
                                            Message.read==False)

   
    return render_template("main/messages.html", 
                            posts=posts, 
                            username=current_user.username, 
                            messages=messages, 
                            posted_questions=posted_questions,
                            )
    

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
   
    pagination = \
        Post.query.filter_by(giver=user).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template("main/user.html", 
                            user=user, 
                            pagination=pagination,
                            posts=posts,
                            )

@main.route("/edit-profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.add(current_user)
        db.session.commit()
        flash("Your profile has been updated! Well Done!")
        return redirect(url_for(".user", username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    form.email.data = current_user.email
    return render_template("main/user_edit_profile.html", form=form)

@main.route("/admin-edit-profile/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_profile(id):
    
    user = User.query.filter_by(id=id).first()
    form = AdminLevelEditProfileForm(
        original_username=user.username, 
        original_email=user.email
        )

    if form.validate_on_submit():
        user.name = request.form.get('name')
        user.location = request.form.get('location')
        user.bio = request.form.get('bio')
        user.confirmed = form.confirmed.data
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.role_id = request.form.get('role')
        db.session.add(user)
        db.session.commit()
        flash("This user profile has been updated by Administrator.")
        return redirect(url_for('.user', username=user.username))

    form.name.data = user.name
    form.location.data = user.location
    form.bio.data = user.bio
    form.confirmed.data = user.confirmed
    form.role.data = user.role
    form.username.data = user.username
    form.email.data = user.email
    return render_template("main/admin_edit_profile.html", form=form, user=user)

@login_required
@main.route('/contact_admin', methods=['GET', 'POST'])
def contact_admin():
    form = ContactAdminForm()

    if request.method == "POST":
        if form.validate_on_submit():
            name = current_user.username
            email = current_user.email
            title = request.form['title']
            description = request.form['description']

            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
                connection.sendmail(
                    from_addr= email, 
                    to_addrs=os.getenv('MAIL_USERNAME'), 
                    msg=f'Subject:Received a message about "{title}"\n\n{description}\nfrom: {name}')
                flash("Successfully submitted!")

            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for('main.index')
            return redirect(next)
    
    return render_template("main/contact_admin.html", form=form, user=current_user)

