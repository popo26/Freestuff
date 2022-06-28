import datetime
from nturl2path import url2pathname
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.main.forms import AdminLevelEditProfileForm, EditProfileForm
from . import main
from app.models import User, Post
from app import db
from ..decorators import permission_required, admin_required

YEAR = datetime.datetime.now().year

@main.route("/")
def index():
    
    return render_template("main/index.html")


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