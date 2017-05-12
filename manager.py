from flask_script import Manager
from app import create_app, db
from app.models import Role, Comment, Article, User
from flask_migrate import Migrate, MigrateCommand, upgrade

app = create_app()
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)


@manager.command
def forged():
    from forgery_py import basic, lorem_ipsum, name, internet, date
    from random import randint

    db.drop_all()
    db.create_all()

    Role.seed()

    guests = Role.query.first()

    def generate_comment(func_author, func_article):
        return Comment(body=lorem_ipsum.paragraphs(),
                       created_time=date.date(past=True),
                       author=func_author(),
                       article=func_article())

    def generate_article(func_author):
        return Article(title=lorem_ipsum.title(),
                       body=lorem_ipsum.paragraphs(),
                       created_time=date.date(past=True),
                       author=func_author())

    def generate_user():
        return User(name=internet.user_name(),
                    email=internet.email_address(),
                    password=basic.text(length=6, at_least=6, spaces=False),
                    role=guests)

    users = [generate_user() for i in range(0, 5)]
    db.session.add_all(users)

    random_user = lambda: users[randint(0, 4)]

    articles = [generate_article(random_user) for i in range(0, randint(50, 200))]
    db.session.add_all(articles)

    random_article = lambda: articles[randint(0, len(articles) - 1)]

    comments = [generate_comment(random_user, random_article) for i in range(0, randint(2, 100))]
    db.session.add_all(comments)

    db.session.commit()

@manager.command
def test():
    pass


@manager.command
def deploy():
    from app.models import Role
    upgrade()
    Role.seed()


if __name__ == '__main__':
    manager.run()
# app.run(debug=True)
