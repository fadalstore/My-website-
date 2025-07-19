from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy import Text, Boolean

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_so = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_so = db.Column(db.String(200), nullable=False)
    content_en = db.Column(Text, nullable=False)
    content_so = db.Column(Text, nullable=False)
    excerpt_en = db.Column(db.String(300))
    excerpt_so = db.Column(db.String(300))
    slug = db.Column(db.String(200), unique=True, nullable=False)
    published = db.Column(Boolean, default=False)
    featured = db.Column(Boolean, default=False)
    meta_description_en = db.Column(db.String(160))
    meta_description_so = db.Column(db.String(160))
    meta_keywords = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')

class FreeLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_so = db.Column(db.String(200), nullable=False)
    description_en = db.Column(Text)
    description_so = db.Column(Text)
    url = db.Column(db.String(500), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    approved = db.Column(Boolean, default=False)
    featured = db.Column(Boolean, default=False)
    submitted_by = db.Column(db.String(100))
    submitter_email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    category = db.relationship('Category', backref=db.backref('links', lazy=True))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    content = db.Column(Text, nullable=False)
    approved = db.Column(Boolean, default=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(Text, nullable=False)
    read = db.Column(Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
