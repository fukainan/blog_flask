# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, InputRequired
from flask_babel import gettext as _


class ArticleForm(FlaskForm):
    title = StringField(label=u'标题', validators=[InputRequired()])
    body = PageDownField(label=u'正文', validators=[InputRequired()])
    submit = SubmitField(label=u'发表')


class CommentForm(FlaskForm):
    body = PageDownField(label=u'评论', validators=[InputRequired()])
    submit = SubmitField(label=u'发表')
