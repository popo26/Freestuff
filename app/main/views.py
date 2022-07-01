import datetime
import smtplib
from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, current_user
from app.main.forms import AdminLevelEditProfileForm, ContactGiverForm, EditProfileForm, PostForm, ReplyForm
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
    return render_template("main/index.html", posts=posts, year=YEAR)

@main.route("/search")
def search():
    keyword = request.args.get('query')
    print(keyword)
   
    results = Post.query.msearch(keyword, fields=['title','description']).all()
    print(results)
    return render_template('main/search.html', results=results, keyword=keyword)

# @main.route('/profile/<username>')
# @login_required
# def profile(username):
#     user = User.query.filter_by(username=username).first()
#     posts = Post.query.filter_by(giver=user)
#     return render_template('main/user.html', user=user, posts=posts)

@main.route("/home-living")
def home_living():
    items = Post.query.filter_by(category_type=Category.HOME_LIVING)
    category="Home&Living"
    return render_template("main/per_category.html", items=items, category=category)

@main.route("/kitchen")
def kitchen():
    items = Post.query.filter_by(category_type=Category.KITCHEN)
    category="Kitchen"
    return render_template("main/per_category.html", items=items, category=category)

@main.route("/baby")
def baby():
    items = Post.query.filter_by(category_type=Category.BABY)
    category="Baby"
    return render_template("main/per_category.html", items=items, category=category)

@main.route("/books")
def books():
    items = Post.query.filter_by(category_type=Category.BOOKS)
    category="Books"
    return render_template("main/per_category.html", items=items, category=category)

@main.route("/craft")
def craft():
    items = Post.query.filter_by(category_type=Category.CRAFT)
    category="Craft"
    return render_template("main/per_category.html", items=items, category=category)

@main.route("/electronics")
def electronics():
    items = Post.query.filter_by(category_type=Category.ELECTRONICS)
    category="Electronics"
    return render_template("main/per_category.html", items=items, category=category)

@main.route("/pets")
def pets():
    items = Post.query.filter_by(category_type=Category.PETS)
    category="Pets"
    return render_template("main/per_category.html", items=items, category=category)

@main.route("/clothing")
def clothing():
    items = Post.query.filter_by(category_type=Category.CLOTHING)
    category="clothing"
    return render_template("main/per_category.html", items=items, category=category)

@main.route("/bathroom")
def bathroom():
    items = Post.query.filter_by(category_type=Category.BATHROOM)
    category="Bathroom"
    return render_template("main/per_category.html", items=items, category=category)

@main.route("/toys")
def toys():
    items = Post.query.filter_by(category_type=Category.TOYS)
    category="Toys"
    return render_template("main/per_category.html", items=items, category=category)

@main.route("/jewellery")
def jewellery():
    items = Post.query.filter_by(category_type=Category.JEWELLERY)
    category="Jewellery"
    return render_template("main/per_category.html", items=items, category=category)

@main.route("/item/<int:item_id>")
def each_item(item_id):
    item = Post.query.filter_by(id=item_id).first()
    # messages = Message.query.filter_by(post_id=item_id).all()
    # reply_messages = Message.query.filter_by(reply=True)
    return render_template("main/each-item.html", item=item)

@main.route("/item/<int:item_id>/edit-post", methods=['GET', 'POST'])
@login_required
def edit_post(item_id):
    form = PostForm()
    item = Post.query.filter_by(id=item_id).first()
    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        item.category_type = form.category.data
        db.session.add(item)
        db.session.commit()
        flash("Successfully updated!")
        return redirect(url_for('.each_item', item_id=item.id))
    form.title.data = item.title
    form.category = item.category_type
    form.description = item.description #not appearing
    return render_template("main/edit-post.html", form=form)

@main.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(item_id):
    item = Post.query.filter_by(id=item_id).delete()
    print(f"to be delete item is ---{item}")
    db.session.commit()
    flash("Selected item is deleted.")
    return redirect(url_for("main.user", username=current_user.username))
    

@main.route('/item/<int:item_id>/reply', methods=['GET', 'POST'])
def reply(item_id):
    form = ReplyForm()
    item = Post.query.filter_by(id=item_id).first()
    if form.validate_on_submit():
        message = Message(description= request.form.get('description'),
                          user_id=current_user.id,
                          post_id=item.id,
                          reply=True)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('main.each_item', item_id=item.id))
    
    return render_template('main/reply.html', item=item, form=form)

@main.route("/contact-giver/<int:item_id>", methods=["GET", "POST"])
@login_required
def contact_giver(item_id):
    form = ContactGiverForm()
    item = Post.query.filter_by(id=item_id).first()
    
    if form.validate_on_submit():
        message = Message(description=request.form.get("description"), 
                          user_id=current_user.id, 
                          post_id=item.id)
        db.session.add(message)
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
    posts = Post.query.filter_by(giver=user)

    return render_template("main/user.html", user=user, posts=posts)

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