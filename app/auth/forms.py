# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from flask_babel import gettext as _


class LoginForm(FlaskForm):
    username = StringField(label=u'用户名', validators=[DataRequired(message=u'请输入用户名')])
    password = PasswordField(label=u'密码', validators=[DataRequired(message=u'请输入密码')])
    submit = SubmitField(u'提交')


class RegistrationForm(FlaskForm):
    email = StringField(label=u'邮箱地址', validators=[DataRequired(), Length(1, 50), Email(message=u'请输入正确的邮箱地址')])
    username = StringField(label=u'用户名', validators=[DataRequired(), Length(1, 50),
                                                     Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, u'用户名必须由字母、数字、下划线组成')])
    password = PasswordField(label=u'密码', validators=[DataRequired()])
    password2 = PasswordField(label=u'确认密码', validators=[DataRequired(), EqualTo('password', message=u'两次填写的密码不一致')])
    submit = SubmitField(label=u'注册')