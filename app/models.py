from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from markdown import markdown


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=True)
    users = db.relationship('User', backref='role')

    @staticmethod
    def seed():
        db.session.add_all(map(lambda r: Role(name=r), ['Guests', 'Administrators']))
        db.session.commit()



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=True)
    email = db.Column(db.String(length=50), nullable=True)
    password = db.Column(db.String(length=50), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    articles = db.relationship('Article', backref='author')
    comments = db.relationship('Comment', backref='author')

    @staticmethod
    def on_created(target, value, oldvalue, initiator):
        target.role = Role.query.filter_by(name='Guests').first()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db.event.listen(User.name, 'set', User.on_created)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50), nullable=True)
    body = db.Column(db.Text, nullable=True)
    body_html = db.Column(db.Text)
    created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='article')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        if value is None or value is '':
            target.body_html = ''
        else:
            target.body_html = markdown(value)


db.event.listen(Article.body, 'set', Article.on_body_changed)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
