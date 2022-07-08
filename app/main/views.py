from base64 import b64encode
import datetime
import smtplib
import secrets
from PIL import Image
from flask import render_template, flash, redirect, request, url_for, current_app, session, send_file
from flask_login import login_required, current_user
from app.main.forms import AdminLevelEditProfileForm, ContactGiverForm, EditProfileForm, PostForm, ReplyForm, PhotoForm
from . import main
from app.models import User, Post
from app import db
from ..decorators import permission_required, admin_required
from ..models import Permission, Category, Message, Photo
from app import config
from app.email import send_email
from config import Config
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from base64 import b64encode

# UPLOAD_FOLDER = '/static/uploads'
# ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

YEAR = datetime.datetime.now().year

def save_photos(form_photos):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_photos.filename)
    photos_fn = random_hex + f_ext
    photos_path = os.path.join(current_app.root_path, 'static/uploads', photos_fn)
    output_size = (500, 500)
    i = Image.open(form_photos)
    i.thumbnail(output_size)
    i.save(photos_path)
    return photos_fn

@main.route("/", methods=['GET', "POST"])
def index():
    posts = Post.query.all()
    posts_count = Post.query.count()
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
    '''work in progress'''
    # photos = Photo.query.filter_by(post_id=item_id).first()
    # img1 = url_for('static', filename='uploads/' + photos.photo_one)
    # for p in posts:
    #     photo = Photo.query.filter_by(post_id=p.id).first()
    #     img = url_for('static', filename='uploads/' + photo.photo_one)
    #     print(img)
 
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
                            year=YEAR,
                            photos_path = photos_path,
                            # img=img,
                            )

@main.route("/search")
def search():
    keyword = request.args.get('query')
    results = Post.query.msearch(keyword, fields=['title','description']).all()
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
    #pagination seems to be working?
    page = request.args.get('page', 1, type=int)
    pagination = \
         Post.query.msearch(keyword, fields=['title','description']).paginate(
            page,
            per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
        )
    posts = pagination.items
    return render_template('main/search.html', 
                            results=results, 
                            keyword=keyword,
                            pagination=pagination, 
                            posts=posts,
                            photos_path = photos_path,
                            year=YEAR)


@main.route("/home-living")
def home_living():
    items = Post.query.filter_by(category_type=Category.HOME_LIVING)
    category="Home&Living"
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path = photos_path,
                            year=YEAR)

@main.route("/kitchen")
def kitchen():
    items = Post.query.filter_by(category_type=Category.KITCHEN)
    category="Kitchen"
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path = photos_path,
                            year=YEAR)
@main.route("/baby")
def baby():
    items = Post.query.filter_by(category_type=Category.BABY)
    category="Baby"
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path = photos_path,
                            year=YEAR)

@main.route("/books")
def books():
    items = Post.query.filter_by(category_type=Category.BOOKS)
    category="Books"
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path = photos_path,
                            year=YEAR)

@main.route("/craft")
def craft():
    items = Post.query.filter_by(category_type=Category.CRAFT)
    category="Craft"
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path = photos_path,
                            year=YEAR)

@main.route("/electronics")
def electronics():
    items = Post.query.filter_by(category_type=Category.ELECTRONICS)
    category="Electronics"
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path = photos_path,
                            year=YEAR)

@main.route("/pets")
def pets():
    items = Post.query.filter_by(category_type=Category.PETS)
    category="Pets"
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path = photos_path,
                            year=YEAR)

@main.route("/clothing")
def clothing():
    items = Post.query.filter_by(category_type=Category.CLOTHING)
    category="clothing"
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path = photos_path,
                            year=YEAR)

@main.route("/bathroom")
def bathroom():
    items = Post.query.filter_by(category_type=Category.BATHROOM)
    category="Bathroom"
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path = photos_path,
                            year=YEAR)

@main.route("/toys")
def toys():
    items = Post.query.filter_by(category_type=Category.TOYS)
    category="Toys"
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path = photos_path,
                            year=YEAR)

@main.route("/jewellery")
def jewellery():
    items = Post.query.filter_by(category_type=Category.JEWELLERY)
    category="Jewellery"
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path = photos_path,
                            year=YEAR)

@main.route("/item/<int:item_id>")
def each_item(item_id):
    item = Post.query.filter_by(id=item_id).first()
    messages = Message.query.filter_by(post_id=item_id).all()
    # print(item.id)
    # print(item.photos)
    photos = Photo.query.filter_by(post_id=item_id).first()
    # print(photos)
    # print(photos.photo_one)
    if photos == None:
        img1 = url_for('static', filename='uploads/cart.jpg' )
    else:
        img1 = url_for('static', filename='uploads/' + photos.photo_one)
    if photos == None:
        img2 = url_for('static', filename='uploads/cart.jpg' )
    else:
        img2 = url_for('static', filename='uploads/' + photos.photo_two)
    if photos == None:
        img3 = url_for('static', filename='uploads/cart.jpg' )
    else:
        img3 = url_for('static', filename='uploads/' + photos.photo_three)
   

    return render_template("main/each-item.html", 
                            item=item, 
                            messages=messages, 
                            year=YEAR, 
                            img1=img1,
                            img2=img2,
                            img3=img3,
                            )

@main.route("/post-new-item", methods=['GET', "POST"])
@login_required
def post_new_item():
    '''Single photo upload'''
    # form = PostForm()
    # if current_user.can(Permission.PUBLISH) \
    #     and form.validate_on_submit():
    #     if form.photos.data:
    #         photos_file = save_photos(form.photos.data)
    #         form.photos = photos_file
    #     post = Post(category_type=form.category.data,
    #                 title=form.title.data,
    #                 description=form.description.data,
    #                 photos=form.photos,
    #                 giver=current_user._get_current_object())
    #     db.session.add(post)
    #     db.session.commit()
    #     flash("Thank you for posting a new free stuff!")
    #     return redirect(url_for('.index'))
    # return render_template("main/post-new-item.html", form=form, year=YEAR)

    form = PostForm()
    p_form = PhotoForm()
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
              
            
        post = Post(category_type=form.category.data,
                    title=form.title.data,
                    description=form.description.data,
                    giver=current_user._get_current_object(),
                    photos=p_form.photo_one)
        photo = Photo(photo_one=p_form.photo_one,
                      photo_two=p_form.photo_two,
                      photo_three=p_form.photo_three, 
                      photo_one_name=p_form.photo_one,
                      photo_two_name=p_form.photo_two,
                      photo_three_name=p_form.photo_three,)
    
        db.session.add(post)
        db.session.add(photo)
        db.session.commit()
        photo.post_id = post.id
        db.session.add(photo)
        db.session.commit()
        flash("Thank you for posting a new free stuff!")
        return redirect(url_for('.index'))
    return render_template("main/post-new-item.html", form=form, year=YEAR, p_form=p_form)


@main.route("/item/<int:item_id>/edit-post", methods=['GET', 'POST'])
@login_required
def edit_post(item_id):
    form = PostForm()
    p_form = PhotoForm()
    item = Post.query.filter_by(id=item_id).first()
    photos = Photo.query.filter_by(post_id=item_id).first()
    print(f"Item ID is {item.id}")
    # print(f"Photos ID is {photos.id}")
        
    if form.validate_on_submit()\
        and p_form.validate_on_submit():
        # if form.photos.data:
        #     photos_file = save_photos(form.photos.data)
        #     item.photos = photos_file
        if p_form.photo_one.data\
            or p_form.photo_two.data\
            or p_form.photo_three.data:
            if p_form.photo_one.data:
                photo_file_one = save_photos(p_form.photo_one.data)
                p_form.photo_one = photo_file_one
                photos.photo_one = photo_file_one
                photos.photo_one_name = photo_file_one
            else:
                photo_file_one = None
                p_form.photo_one = photo_file_one
            if p_form.photo_two.data:   
                photo_file_two = save_photos(p_form.photo_two.data)
                p_form.photo_two = photo_file_two
                photos.photo_two = photo_file_two
                photos.photo_two_name = photo_file_one
            else:
                photo_file_two = None
                p_form.photo_two = photo_file_two
            if p_form.photo_three.data:
                photo_file_three = save_photos(p_form.photo_three.data)
                p_form.photo_three = photo_file_three
                photos.photo_three = photo_file_three
                photos.photo_three_name = photo_file_one
            else:
                photo_file_three = None
                p_form.photo_three = photo_file_three
                
        item.title = form.title.data
        item.description = form.description.data
        item.category_type = form.category.data
        if not item.photos:
            item.photos = 'cart.jpg'
        else:
            item.photos = photo_file_one
        db.session.add(photos)
        db.session.add(item)
        print(f"Item ID is {item.id}")
        
        db.session.commit()
        flash("Successfully updated!", 'success')
        return redirect(url_for('.each_item', item_id=item.id))
    
    form.title.data = item.title
    form.category.data = item.category_type
    form.description.data = item.description 
    # img_file = url_for('static', filename='uploads/' + item.photos)
    
    # if not photos:
    #     p_form.photo_one.data = 'cart.jpg'
    #     p_form.photo_two.data = 'cart.jpg'
    #     p_form.photo_three.data = 'cart.jpg'
    # else:
    #     p_form.photo_one.data = photos.photo_one
    #     p_form.photo_two.data = photos.photo_two
    #     p_form.photo_three.data = photos.photo_three
    # print(photos.photo_one)
    # p_form.photo_one.data = request.files.get(photos.photo_one)
    # p_form.photo_two.data = photos.photo_two.data
    # p_form.photo_three.data = photos.photo_three.data

    if photos:
        p_form.photo_one_name.data = photos.photo_one
        p_form.photo_two_name.data = photos.photo_two
        p_form.photo_three_name.data = photos.photo_three
    else:
        p_form.photo_one.data = None
        p_form.photo_two.data = None
        p_form.photo_three.data = None
        
    return render_template("main/edit-post.html", form=form, p_form=p_form, item=item, year=YEAR)

@main.route('/delete/<int:item_id>/photo', methods=["GET", "POST"])
@login_required
def delete_all_photos(item_id):
    item = Post.query.filter_by(id=item_id).first()
    photos = Photo.query.filter_by(post_id=item.id)
    for p in photos:
        print(p.photo_one)
        if p.photo_one:
            p.photo_one = 'cart.jpg'
            p.photo_one_name = 'default'
            db.session.commit()
        if p.photo_two:
            p.photo_two = 'cart.jpg'
            p.photo_two_name = 'default'
            db.session.commit()
        if p.photo_three:
            p.photo_three = 'cart.jpg'
            p.photo_three_name = 'default'
            db.session.commit()
    
        item.photos = p.photo_one
        db.session.add(item)
        db.session.commit()

    return redirect(url_for('main.edit_post', item_id=item.id))



@main.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(item_id):
    photos = Photo.query.filter_by(post_id=item_id).first()
    
    photo1 = url_for('static', filename='uploads/' + photos.photo_one)
    print(photo1)
    if photo1:
        os.remove(photo2)
  
    photo2 = url_for('static', filename='uploads/' + photos.photo_two)
    if photo2:
        os.remove(photo2)
    photo3 = url_for('static', filename='uploads/' + photos.photo_three)
    if photo3:
        os.remove(photo3)
    
    Photo.query.filter_by(post_id=item_id).delete()
    Post.query.filter_by(id=item_id).delete()
    db.session.commit()
    html = render_template('mail/admin_post_deleted.html', user=current_user)
    send_email(os.getenv('MAIL_USERNAME'), "A post deleted", html)
    
    flash("Selected item is deleted.")
    return redirect(url_for("main.user", username=current_user.username, year=YEAR))
    

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
                        #   answered_user = message.asker,
                        #   answered_user2 = message.asker.username,
                          )
        db.session.add(message)
        db.session.commit()
        # message.answered_user = message.asker
        # message.answered_user2 = message.asker
        # print(message.asker)
        
        #work in progress
        # original_message = Message.query.filter_by(post_id=item.id, replied=False).first()
        original_message = Message.query.filter_by(id=message_id).first()
        print(original_message)
        print(original_message.id)
        # print(original_message.replied)
        # print(original_message.reply)
        original_message.replied = True
        print(original_message.asker)
        print(message.asker)
        message.answered_user = original_message.asker.id
        # x = str(original_message.asker)
        # asker_username = x.replace(x, f'{original_message.asker.username}')
        message.answered_user2 = original_message.asker.username
        db.session.add(message)
        # original_message.answered_user = message.asker
        original_message.asker.question_answered += 1
        db.session.add(original_message)
        current_user.question_received -= 1
        if current_user.question_received < 0:
            current_user.question_received = 0
        db.session.add(current_user)
        # db.session.commit()
        # message.answered_user = message.asker
        # message.answered_user2 = message.asker.username
        # db.session.add(message)
        db.session.commit()
        return redirect(url_for('main.each_item', item_id=item.id, message_id=message.id, year=YEAR))
    
    return render_template('main/reply.html', item=item, form=form, year=YEAR)

@main.route('/item/<int:item_id>/replied/<int:message_id>', methods=['GET', 'POST'])
def mark_as_replied(item_id, message_id):
    replied_message = Message.query.filter_by(id=message_id).first()
    item = Post.query.filter_by(id=item_id).first()
    print(message_id)
    print(replied_message)
    replied_message.replied = True
    db.session.add(replied_message)
    item.giver.question_received -= 1
    if item.giver.question_received < 0:
        item.giver.question_received = 0
    replied_message.read = True
    db.session.add(replied_message)
    db.session.add(item)
    db.session.commit()
    
    return redirect(url_for('main.check_messages', username=current_user.username, year=YEAR))

@main.route('/item/<int:item_id>/answered/<int:message_id>', methods=['GET', 'POST'])
def mark_as_read(item_id, message_id):
    answered_message = Message.query.filter_by(id=message_id).first()
    item = Post.query.filter_by(id=item_id).first()
    print(message_id)
    current_user.question_answered -=1
    if current_user.question_answered < 0:
        current_user.question_answered = 0
    answered_message.read = True
    db.session.add(current_user)
    db.session.add(answered_message)
    db.session.commit()
    # return render_template('main/messages.html', username=current_user.username)
    return redirect(url_for('main.check_messages', username=current_user.username, year=YEAR))

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
        link = url_for('main.each_item', _external=True, item_id=item.id)
        html = render_template('mail/user_question_recieved.html', giver=item.giver, link=link, item=item)
        send_email(item.giver.email, "You received a question!", html)
        flash("successfully submitted!")
        return redirect(url_for("main.each_item", item_id=item.id))
    return render_template("main/contact-giver.html", form=form, item=item, year=YEAR)

#In progress
@main.route("/messages/<username>")
@login_required
def check_messages(username):
    messages = Message.query.filter(Message.replied==False)
    posts = Post.query.filter_by(giver=current_user)  
    posted_questions = Message.query.filter(Message.user_id==current_user.id, 
                                            Message.replied==True, 
                                            Message.read==False).all()
        
    print(current_user.id)
    print(current_user.username)
    print(posted_questions)

    return render_template("main/messages.html", 
                            posts=posts, 
                            username=current_user.username, 
                            messages=messages, 
                            posted_questions=posted_questions,
                            year=YEAR)
    

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # posts = Post.query.filter_by(giver=user)
    page = request.args.get('page', 1, type=int)
    photos_path = os.path.join(current_app.root_path, '/static/uploads/')
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
                            photos_path=photos_path,
                            year=YEAR)

@main.route("/edit-profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        db.session.add(current_user)
        db.session.commit()
        flash("Your profile has been updated! Well Done!")
        return redirect(url_for(".user", username=current_user.username, year=YEAR))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template("main/user_edit_profile.html", form=form, year=YEAR)

@main.route("/admin-edit-profile/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_profile(id):
    form = AdminLevelEditProfileForm()
    user = User.query.filter_by(id=id).first()
    if form.validate_on_submit():
        user.name = form.name.data
        user.location = form.location.data
        user.bio = form.bio.data
        user.confirmed = form.confirmed.data
        user.username = form.username.data
        user.role_id = form.role.data 
        db.session.add(user)
        db.session.commit()
        flash("This user profile has been updated by Administrator.")
        return redirect(url_for('.user', username=user.username, year=YEAR))
    form.name.data = user.name
    form.location.data = user.location
    form.bio.data = user.bio
    form.confirmed.data = user.confirmed
    form.role.data = user.role
    form.username.data = user.username
    return render_template("main/admin_edit_profile.html", form=form, year=YEAR)