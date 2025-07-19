from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from app import db
from models import User, BlogPost, Category, FreeLink, Comment, ContactMessage

class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('admin_login'))
        return super(SecureAdminIndexView, self).index()

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login'))

class UserModelView(SecureModelView):
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['password_hash', 'posts']
    column_searchable_list = ['username', 'email']

class BlogPostModelView(SecureModelView):
    column_list = ['title_en', 'title_so', 'author', 'category', 'published', 'featured', 'created_at']
    column_searchable_list = ['title_en', 'title_so', 'content_en', 'content_so']
    column_filters = ['published', 'featured', 'category', 'author']
    form_columns = ['title_en', 'title_so', 'content_en', 'content_so', 'excerpt_en', 'excerpt_so', 
                   'slug', 'published', 'featured', 'meta_description_en', 'meta_description_so', 
                   'meta_keywords', 'author', 'category']

class CategoryModelView(SecureModelView):
    column_list = ['name_en', 'name_so', 'slug', 'created_at']
    form_columns = ['name_en', 'name_so', 'slug']

class FreeLinkModelView(SecureModelView):
    column_list = ['title_en', 'title_so', 'url', 'category', 'approved', 'featured', 'submitted_by', 'created_at']
    column_searchable_list = ['title_en', 'title_so', 'url', 'submitted_by']
    column_filters = ['approved', 'featured', 'category']
    form_columns = ['title_en', 'title_so', 'description_en', 'description_so', 'url', 
                   'category', 'approved', 'featured', 'submitted_by', 'submitter_email']

class CommentModelView(SecureModelView):
    column_list = ['name', 'email', 'post', 'approved', 'created_at']
    column_searchable_list = ['name', 'email', 'content']
    column_filters = ['approved', 'post']
    form_columns = ['name', 'email', 'content', 'approved', 'post']

class ContactMessageModelView(SecureModelView):
    column_list = ['name', 'email', 'subject', 'read', 'created_at']
    column_searchable_list = ['name', 'email', 'subject', 'message']
    column_filters = ['read']
    form_columns = ['name', 'email', 'subject', 'message', 'read']

def setup_admin(app):
    admin = Admin(app, name='Blog Admin', template_mode='bootstrap4', index_view=SecureAdminIndexView())
    
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(BlogPostModelView(BlogPost, db.session))
    admin.add_view(CategoryModelView(Category, db.session))
    admin.add_view(FreeLinkModelView(FreeLink, db.session))
    admin.add_view(CommentModelView(Comment, db.session))
    admin.add_view(ContactMessageModelView(ContactMessage, db.session))
