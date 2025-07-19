from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from sqlalchemy import or_
from app import app, db
from models import BlogPost, FreeLink, Category, Comment, ContactMessage, User
from forms import CommentForm, ContactForm, LinkSubmissionForm
from utils import generate_sitemap, generate_rss
from translations import get_text

@app.route('/')
def index():
    lang = request.args.get('lang', session.get('language', 'en'))
    session['language'] = lang
    
    # Get featured blog posts
    featured_posts = BlogPost.query.filter_by(published=True, featured=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    
    # Get recent blog posts
    recent_posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(6).all()
    
    # Get featured links
    featured_links = FreeLink.query.filter_by(approved=True, featured=True).order_by(FreeLink.created_at.desc()).limit(6).all()
    
    return render_template('index.html', 
                         featured_posts=featured_posts, 
                         recent_posts=recent_posts,
                         featured_links=featured_links,
                         lang=lang)

@app.route('/blog')
def blog():
    lang = request.args.get('lang', session.get('language', 'en'))
    session['language'] = lang
    
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    
    query = BlogPost.query.filter_by(published=True)
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    posts = query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    categories = Category.query.all()
    
    return render_template('blog.html', posts=posts, categories=categories, 
                         selected_category=category_id, lang=lang)

@app.route('/blog/<slug>')
def post(slug):
    lang = request.args.get('lang', session.get('language', 'en'))
    session['language'] = lang
    
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    comments = Comment.query.filter_by(post_id=post.id, approved=True).order_by(Comment.created_at.asc()).all()
    
    form = CommentForm()
    
    return render_template('post.html', post=post, comments=comments, form=form, lang=lang)

@app.route('/blog/<slug>/comment', methods=['POST'])
def add_comment(slug):
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            name=form.name.data,
            email=form.email.data,
            content=form.content.data,
            post_id=post.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been submitted and is pending approval.', 'success')
    
    return redirect(url_for('post', slug=slug))

@app.route('/links')
def links():
    lang = request.args.get('lang', session.get('language', 'en'))
    session['language'] = lang
    
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    
    query = FreeLink.query.filter_by(approved=True)
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    links = query.order_by(FreeLink.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    categories = Category.query.all()
    form = LinkSubmissionForm()
    
    return render_template('links.html', links=links, categories=categories, 
                         selected_category=category_id, form=form, lang=lang)

@app.route('/submit-link', methods=['POST'])
def submit_link():
    form = LinkSubmissionForm()
    
    if form.validate_on_submit():
        link = FreeLink(
            title_en=form.title_en.data,
            title_so=form.title_so.data,
            description_en=form.description_en.data,
            description_so=form.description_so.data,
            url=form.url.data,
            category_id=form.category_id.data,
            submitted_by=form.submitted_by.data,
            submitter_email=form.submitter_email.data
        )
        db.session.add(link)
        db.session.commit()
        flash('Your link has been submitted and is pending approval.', 'success')
    
    return redirect(url_for('links'))

@app.route('/search')
def search():
    lang = request.args.get('lang', session.get('language', 'en'))
    session['language'] = lang
    
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    posts = []
    links = []
    
    if query:
        # Search blog posts
        if lang == 'so':
            posts = BlogPost.query.filter(
                BlogPost.published == True,
                or_(BlogPost.title_so.contains(query), 
                    BlogPost.content_so.contains(query),
                    BlogPost.excerpt_so.contains(query))
            ).order_by(BlogPost.created_at.desc()).paginate(
                page=page, per_page=5, error_out=False)
        else:
            posts = BlogPost.query.filter(
                BlogPost.published == True,
                or_(BlogPost.title_en.contains(query), 
                    BlogPost.content_en.contains(query),
                    BlogPost.excerpt_en.contains(query))
            ).order_by(BlogPost.created_at.desc()).paginate(
                page=page, per_page=5, error_out=False)
        
        # Search links
        if lang == 'so':
            links = FreeLink.query.filter(
                FreeLink.approved == True,
                or_(FreeLink.title_so.contains(query), 
                    FreeLink.description_so.contains(query))
            ).order_by(FreeLink.created_at.desc()).limit(10).all()
        else:
            links = FreeLink.query.filter(
                FreeLink.approved == True,
                or_(FreeLink.title_en.contains(query), 
                    FreeLink.description_en.contains(query))
            ).order_by(FreeLink.created_at.desc()).limit(10).all()
    
    return render_template('search.html', query=query, posts=posts, links=links, lang=lang)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    lang = request.args.get('lang', session.get('language', 'en'))
    session['language'] = lang
    
    form = ContactForm()
    
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form, lang=lang)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password) and user.is_admin:
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/sitemap.xml')
def sitemap():
    return generate_sitemap()

@app.route('/rss.xml')
def rss():
    return generate_rss()

# Language switching
@app.route('/set-language/<lang>')
def set_language(lang):
    session['language'] = lang
    return redirect(request.referrer or url_for('index'))

# Template context processors
@app.context_processor
def inject_globals():
    return {
        'get_text': get_text,
        'current_lang': session.get('language', 'en'),
        'categories': Category.query.all()
    }
