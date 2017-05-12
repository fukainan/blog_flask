# -*- coding:utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from app import db
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm
from flask_babel import gettext as _


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # flash(u'登陆成功')
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data, password=form.password.data).first()
        if user is not None:
            login_user(user)
            return redirect(url_for('main.index'))
    return render_template('login.html', title=u'登陆', form=form)


@auth.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # flash(u'注册成功')
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', title=u'注册', form=form)
