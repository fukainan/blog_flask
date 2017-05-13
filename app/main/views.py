# -*- coding:utf-8 -*-

from os import path

from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user, AnonymousUserMixin
from . import main
from .. import db
from ..models import Article, Comment
from .forms import ArticleForm, CommentForm
from random import randint
from flask_babel import gettext as _


@main.route('/')
@main.route('/index')
def index():
    # articles = Article.query.all()
    articles = []
    for i in range(20):
        article = Article.query.get_or_404(randint(1, len(Article.query.all())))
        articles.append(article)
    return render_template('index.html', title=u'欢迎来到博客', articles=articles)


@main.route('/articles/all')
def articles():
    page_index = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        query = Article.query.filter_by(author_id=current_user.id).order_by(Article.created_time.desc())
        title = u'%s的文章' % current_user.name
    else:
        query = Article.query.order_by(Article.created_time.desc())
        title = u'全部文章'
    pagination = query.paginate(page_index, per_page=20, error_out=False)
    articles = pagination.items
    return render_template('articles.html', title=title, articles=articles, pagination=pagination)


@main.route('/articles/<int:id>', methods=['GET', 'POST'])
def detail(id):
    article = Article.query.get_or_404(id)
    # 评论窗体
    form = CommentForm()
    # 保存评论
    if form.is_submitted():
        comment = Comment(body=form.body.data, article=article, author=current_user)
        db.session.add(comment)
        db.session.commit()

    return render_template('articles/detail.html', title=article.title, form=form, article=article)


@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    form = ArticleForm()
    if id == 0:
        article = Article(author_id=current_user.id)
    else:
        article = Article.query.get_or_404(id)
        if request.method=='GET':
            form.title.data = article.title
            form.body.data = article.body
    if form.validate_on_submit():
        article.title = form.title.data
        article.body = form.body.data
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('.detail', id=article.id))
    title = u'添加新文章'
    if id > 0:
        title = u'编辑 - %s' % article.title
    return render_template('articles/edit.html', title=title, form=form, article=article)


@main.route('/delete/article/<int:id>')
@login_required
def del_art(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/delete/comment/<int:id>')
@login_required
def del_com(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/user/<regex("[a-z]{3}"):user_id>')
def user(user_id):
    return 'User %s' % user_id


@main.route('/admin')
@login_required
def admin():
    return 'Admin'


@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath, 'static/uploads')
        f.save(path.join(upload_path, filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# @main.template_test('current_link')
# def is_current_link(link):
#     return link == request.path


# @main.template_filter('md')
# def markdown_to_html(txt):
#     from markdown import markdown
#     return markdown(txt)


def read_md(filename):
    with open(filename) as md_file:
        content = reduce(lambda x, y: x + y, md_file.readline)
    return content.decode('utf-8')


@main.context_processor
def inject_methods():
    return dict(read_md=read_md)
