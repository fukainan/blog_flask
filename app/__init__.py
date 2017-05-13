# -*- coding:utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_gravatar import Gravatar
from flask_admin import Admin
from admin import MyView, MyModelView
from flask_babel import Babel, gettext as _


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


bootstrap = Bootstrap()
nav = Nav()
db = SQLAlchemy()
admin = Admin()
pagedown = PageDown()
babel = Babel()
gravatar = Gravatar()
gravatar.size = 64
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    app.secret_key = 'hard to guess string'
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/blog_flask'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

    # nav.register_element('top', Navbar(u'博客首页',
    #                                    View(u'主页', 'main.index'),
    #                                    View(u'关于', 'main.about'),
    #                                    View(u'服务', 'main.services'),
    #                                    View(u'项目', 'main.projects'),
    #                                    View(u'登陆', 'auth.login'),
    #                                    View(u'注册', 'auth.register')
    #                                    ))
    nav.init_app(app)
    pagedown.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    babel.init_app(app)
    gravatar.init_app(app)
    login_manager.init_app(app)

    admin.init_app(app)
    admin.add_view(MyView(name=u'Custom'))
    from models import Role, User, Article, Comment
    models = [Role, User, Article, Comment]
    for model in models:
        admin.add_view(MyModelView(model, db.session, category='Models'))

    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint, static_folder='static')

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    return app
