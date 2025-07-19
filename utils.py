from flask import render_template_string, url_for, request
from datetime import datetime
from models import BlogPost, FreeLink

def generate_sitemap():
    """Generate XML sitemap"""
    
    # Get all published posts
    posts = BlogPost.query.filter_by(published=True).all()
    
    sitemap_template = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{{ url_for('index', _external=True) }}</loc>
        <lastmod>{{ now.strftime('%Y-%m-%d') }}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{{ url_for('blog', _external=True) }}</loc>
        <lastmod>{{ now.strftime('%Y-%m-%d') }}</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{{ url_for('links', _external=True) }}</loc>
        <lastmod>{{ now.strftime('%Y-%m-%d') }}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{{ url_for('contact', _external=True) }}</loc>
        <lastmod>{{ now.strftime('%Y-%m-%d') }}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
    {% for post in posts %}
    <url>
        <loc>{{ url_for('post', slug=post.slug, _external=True) }}</loc>
        <lastmod>{{ post.updated_at.strftime('%Y-%m-%d') }}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    {% endfor %}
</urlset>'''
    
    from flask import Response
    xml = render_template_string(sitemap_template, posts=posts, now=datetime.now())
    response = Response(xml, mimetype='application/xml')
    return response

def generate_rss():
    """Generate RSS feed"""
    
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(20).all()
    
    rss_template = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Somali English Blog</title>
        <link>{{ url_for('index', _external=True) }}</link>
        <description>Latest blog posts in Somali and English</description>
        <language>en-us</language>
        <lastBuildDate>{{ now.strftime('%a, %d %b %Y %H:%M:%S +0000') }}</lastBuildDate>
        {% for post in posts %}
        <item>
            <title>{{ post.title_en }}</title>
            <link>{{ url_for('post', slug=post.slug, _external=True) }}</link>
            <description>{{ post.excerpt_en or post.content_en[:300] }}...</description>
            <pubDate>{{ post.created_at.strftime('%a, %d %b %Y %H:%M:%S +0000') }}</pubDate>
            <guid>{{ url_for('post', slug=post.slug, _external=True) }}</guid>
        </item>
        {% endfor %}
    </channel>
</rss>'''
    
    from flask import Response
    xml = render_template_string(rss_template, posts=posts, now=datetime.now())
    response = Response(xml, mimetype='application/rss+xml')
    return response
