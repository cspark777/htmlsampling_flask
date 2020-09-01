# users/views.py

from sqlalchemy.orm.exc import NoResultFound
from sampling.users.forms import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, request, flash, redirect, redirect, Blueprint
import os
from sampling.models import User

users = Blueprint('users', __name__)

# login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(u'Invalid username or password', 'alert alert-danger')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('page.list_pages')
        return redirect(next_page)

    return render_template('login.html', form=form)


# logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))
