# -*- coding:utf-8 -*-

from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user



class MyView(BaseView):
    @expose('/',methods=['GET', 'POST'])
    def index(self):
        return self.render('admin.html')


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.name=='Administrators'
