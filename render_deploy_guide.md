# Render.com Deployment Guide for Somali English Blog

## Step 1: Repository Setup
1. Create a new repository on GitHub with all the project files
2. Upload these files to your repository:
   - All Python files (app.py, main.py, models.py, routes.py, etc.)
   - All template files (templates/ folder)
   - All static files (static/ folder)
   - render_requirements.txt (rename to requirements.txt)
   - render.yaml (deployment configuration)

## Step 2: Create Web Service on Render
1. Go to https://dashboard.render.com
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:

### Build Settings:
- **Name**: somali-english-blog
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`

### Environment Variables:
Add these environment variables in Render dashboard:
- `SESSION_SECRET`: Generate a random secret key (use Render's auto-generate)
- `ADMIN_EMAIL`: Your admin email (e.g., admin@yourdomain.com)
- `ADMIN_PASSWORD`: Your admin password (use Render's auto-generate)
- `DATABASE_URL`: Will be provided when you create the database

## Step 3: Create PostgreSQL Database
1. In Render dashboard, click "New" → "PostgreSQL"
2. Configure:
   - **Name**: somali-blog-db
   - **Database**: somali_english_blog
   - **User**: blog_user
   - **Plan**: Free

3. After creation, copy the "Internal Database URL"
4. Add it as `DATABASE_URL` environment variable in your web service

## Step 4: Deploy
1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start the application
   - Create database tables automatically
   - Generate SSL certificate

## Step 5: Post-Deployment Setup
1. **Access Admin Panel**: Go to https://your-app.onrender.com/admin
2. **Login**: Use the auto-generated admin credentials from environment variables
3. **Add Content**:
   - Create categories (e.g., Education, Technology, Community)
   - Write your first blog posts in both languages
   - Add initial free links

## Step 6: Google AdSense Integration
1. Apply for Google AdSense approval
2. Once approved, replace AdSense placeholders in templates with real ad codes
3. Update these files:
   - `templates/base.html` (sidebar ads)
   - `templates/index.html` (hero section ad)
   - `templates/post.html` (in-content ads)

## Step 7: Custom Domain (Optional)
1. In Render dashboard, go to your service settings
2. Add your custom domain
3. Update DNS records as instructed by Render
4. SSL certificate will be auto-generated

## Important Files for Deployment:

### requirements.txt
```
Flask>=3.1.1
Flask-SQLAlchemy>=3.1.1
Flask-Login>=0.6.3
Flask-Admin>=1.6.1
Flask-WTF>=1.2.2
WTForms>=3.2.1
Werkzeug>=3.1.3
gunicorn>=23.0.0
psycopg2-binary>=2.9.10
SQLAlchemy>=2.0.41
email-validator>=2.2.0
```

### Key Features Ready for Production:
- ✅ Bilingual content (Somali/English)
- ✅ Admin panel with authentication
- ✅ Free links directory with user submissions
- ✅ Comment system with moderation
- ✅ Contact form
- ✅ SEO optimization (sitemaps, meta tags)
- ✅ Mobile-responsive design
- ✅ AdSense integration ready
- ✅ Database with PostgreSQL support
- ✅ Security headers and HTTPS

### Expected Costs:
- **Render Web Service**: Free tier (limited)
- **Render PostgreSQL**: Free tier (1GB storage)
- **Custom Domain**: $10-15/year (optional)
- **Paid Render Plans**: $7+/month for better performance

The website is fully ready for deployment and monetization with Google AdSense!