from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user


from app.models import User, Organization


from app.mod_admin.forms import UserCreateForm, UserInfoForm, EmailForm, PasswordForm, OrgCreateForm

from app import db


mod_admin = Blueprint('admin', __name__, url_prefix='/')



@mod_admin.route("/layout", methods=["GET", "POST"])
def layout():
	return render_template('layout.html')


@mod_admin.route("/list", methods=["GET"])
def show_panel():
	users = User.query.all()
	return render_template("admin_panel/list_users.html", users=users)



@mod_admin.route("/", methods=["GET", "POST"])
def base():
	return render_template('admin_panel/base.html')



@mod_admin.route("/add_user", methods=["GET", "POST"])
def add_user():
    form = UserCreateForm()
    orgs = Organization.query.all()
    form.organizations.choices = [(org.id, org.name) for org in orgs]
   
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    is_admin=form.is_admin.data,
                    )
        user.set_password(form.password.data)
        orgs = []

        for org_id in form.organizations.data:
        	org = Organization.query.filter_by(id=org_id).first()
        	orgs.append(org)

        db.session.add(user)
        db.session.commit()
        flash('user added')
        return redirect(url_for("admin.show_panel"))

    return render_template('admin_panel/create_user.html', form=form)




@mod_admin.route("/edit_user/<user_id>/password", methods=["GET", "POST"])
def change_password(user_id):
    form = PasswordForm()
    user = User.query.filter_by(id=user_id).first()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        session_commit()

        return redirect(url_for("admin.base"))

    return render_template("admin_panel/change_password.html", form=form, user=user)




@mod_admin.route("/delete_user/<user_id>", methods=["GET", "POST"])
def delete_user(user_id):
	user = User.query.filter_by(id=user_id).first()
	db.session.delete(user)
	db.session.commit()

	return redirect(url_for("admin.show_panel"))



@mod_admin.route("/add_organization", methods=["GET", "POST"])
def add_organization():
	form = OrgCreateForm()
	users = User.query.all()

	form.users.choices = [(user.id, user.email) for user in users]

	if form.validate_on_submit():
		org = Organization(name=form.name.data,
			data_dir=form.data_dir.data)

		users = []

		for user_id in form.users.data:
			user = User.query.filter_by(id=user_id).first()
			users.append(user)

		org.users = users
		db.session.add(org)
		db.session.commit()

		return redirect(url_for("admin.add_organization"))

	return render_template("admin_panel/create_organization.html", form=form)