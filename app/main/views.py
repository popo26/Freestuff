import datetime
import smtplib
from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, current_user
from app.main.forms import AdminLevelEditProfileForm, ContactGiverForm, EditProfileForm, PostForm, SearchForm
from . import main
from app.models import User, Post
from app import db
from ..decorators import permission_required, admin_required
from ..models import Permission, Category, Message
from app import config


YEAR = datetime.datetime.now().year

@main.route("/", methods=['GET', "POST"])
def index():
    posts = Post.query.all()
    return render_template("main/index.html", posts=posts)

@main.route("/search")
def search():
    keyword = request.args.get('query')
    print(keyword)
   
    results = Post.query.msearch(keyword, fields=['title','description']).all()
    print(results)
    return render_template('main/search.html', results=results, keyword=keyword)

@main.route("/home-living")
def home_living():
    items = Post.query.filter_by(category_type=Category.HOME_LIVING)
    #Work in progress. 
    return render_template("main/home_living.html", items=items)

@main.route("/item/<int:item_id>")
def each_item(item_id):
    item = Post.query.filter_by(id=item_id).first()
    return render_template("main/each-item.html", item=item)

@main.route("/contact-giver/<int:item_id>", methods=["GET", "POST"])
@login_required
def contact_giver(item_id):
    form = ContactGiverForm()
    item = Post.query.filter_by(id=item_id).first()
    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        db.session.add(item)
        db.session.commit()
        flash("successfully submitted!")
        #how to send email in progress
        return redirect(url_for("main.each_item", item_id=item.id))
    return render_template("main/contact-giver.html", form=form, item=item)

#In progress
@main.route("/messages/<username>")
@login_required
def check_messages(username):
    messages = Message.query.all()
    return render_template("main/messages.html", username=current_user, message=messages)
    
    

@main.route("/post-new-item", methods=['GET', "POST"])
@login_required
def post_new_item():
    form = PostForm()
    if current_user.can(Permission.PUBLISH) \
        and form.validate_on_submit():
        post = Post(category_type=form.category.data,
                    title=form.title.data,
                    description=form.description.data,
                    giver=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash("Thank you for posting a new free stuff!")
        return redirect(url_for('.index'))
    # posts = Post.query.order_by(Post.timestamp.desc())
    return render_template("main/post-new-item.html", form=form)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # posts = Post.query.filter_by(giver=user)

    return render_template("main/user.html", user=user)

@main.route("/edit-profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.add(current_user)
        db.session.commit()
        flash("Your profile has been updated! Well Done!")
        return redirect(url_for(".user", username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template("main/user_edit_profile.html", form=form)

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
        return redirect(url_for('.user', username=user.username))
    form.name.data = user.name
    form.location.data = user.location
    form.bio.data = user.bio
    form.confirmed.data = user.confirmed
    form.role.data = user.role
    form.username.data = user.username
    return render_template("main/admin_edit_profile.html", form=form)