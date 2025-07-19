# Somali English Blog - Project Overview

## Overview

This is a bilingual Flask web application that serves as a blog and resources platform for the Somali community. The application supports both English and Somali languages, featuring blog posts, free links directory, user comments, and contact functionality. It includes a comprehensive admin panel for content management.

**Current Status**: Fully functional with sample content, PostgreSQL database connected, admin panel operational, and ready for deployment.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a traditional Flask MVC architecture with the following key characteristics:

- **Web Framework**: Flask with Jinja2 templating
- **Database**: SQLAlchemy ORM with support for PostgreSQL (production) and SQLite (development)
- **Authentication**: Flask-Login for user authentication and admin access control
- **Admin Interface**: Flask-Admin for content management
- **Frontend**: Bootstrap 5 with custom CSS and JavaScript
- **Internationalization**: Custom translation system for bilingual content

## Key Components

### Backend Components

1. **Application Factory** (`app.py`)
   - Flask app configuration and initialization
   - Database setup with automatic table creation
   - Login manager configuration
   - Default admin user creation

2. **Database Models** (`models.py`)
   - User model with admin role support
   - BlogPost model with bilingual content fields
   - Category model for organizing content
   - FreeLink model for resource directory
   - Comment model with approval system
   - ContactMessage model for user inquiries

3. **Admin Interface** (`admin.py`)
   - Secure admin views with authentication
   - Custom model views for each entity
   - Role-based access control

4. **Forms** (`forms.py`)
   - WTForms for user input validation
   - Comment submission forms
   - Contact forms
   - Link submission forms with dynamic category selection

5. **Routes** (`routes.py`)
   - Home page with featured content
   - Blog listing and individual post pages
   - Free links directory
   - Search functionality
   - Contact page
   - Language switching

6. **Utilities** (`utils.py`)
   - SEO utilities (sitemap generation, RSS feeds)
   - Helper functions for content management

### Frontend Components

1. **Templates** (`templates/`)
   - Base template with responsive navigation
   - Individual page templates
   - Admin interface templates
   - Bilingual content support

2. **Static Assets** (`static/`)
   - Custom CSS with Bootstrap integration
   - JavaScript for enhanced user experience
   - Responsive design with mobile-first approach

3. **Internationalization** (`translations.py`)
   - Translation dictionary for English and Somali
   - Helper functions for language switching
   - Session-based language persistence

## Data Flow

### Content Management Flow
1. Admin users log in through secure authentication
2. Content is created/edited through Flask-Admin interface
3. Blog posts and links support both English and Somali content
4. Content approval workflow for user-submitted links and comments

### User Experience Flow
1. Users visit the site and can switch between English/Somali
2. Language preference is stored in session
3. Content is displayed in selected language
4. Users can comment on posts (with moderation)
5. Users can submit links for inclusion in directory
6. Contact form allows direct communication

### Search and Discovery
1. Global search across posts and links
2. Category-based filtering
3. Featured content promotion
4. SEO optimization with sitemaps and meta tags

## External Dependencies

### Python Packages
- **Flask**: Core web framework
- **SQLAlchemy**: ORM and database abstraction
- **Flask-Login**: User authentication
- **Flask-Admin**: Admin interface
- **Flask-WTF**: Form handling and validation
- **Werkzeug**: WSGI utilities and security

### Frontend Libraries
- **Bootstrap 5**: CSS framework and components
- **Font Awesome**: Icon library
- **Custom CSS**: Application-specific styling
- **Vanilla JavaScript**: Client-side functionality

### Database Support
- **PostgreSQL**: Production database (via DATABASE_URL environment variable)
- **SQLite**: Development database (fallback)

## Deployment Strategy

### Environment Configuration
- Environment-based configuration using `os.environ`
- Support for both development (SQLite) and production (PostgreSQL) databases
- Session secret key configuration
- ProxyFix middleware for deployment behind reverse proxies

### Database Migration Strategy
- Automatic table creation on first run
- Default admin user creation
- Support for database URL transformation (Heroku compatibility)
- Connection pooling and health checks

### Security Considerations
- Role-based admin access control
- CSRF protection on forms
- Password hashing using Werkzeug security
- Secure session management
- Input validation and sanitization

### Performance Optimizations
- Database connection pooling
- Static asset optimization
- Lazy loading for images
- Efficient database queries with proper relationships
- Caching considerations for production deployment

### SEO and Analytics
- Meta tag optimization
- Open Graph protocol support
- XML sitemap generation
- RSS feed support
- Google AdSense integration placeholders
- Structured data for search engines

The application is designed to be easily deployable on platforms like Heroku, Railway, or similar PaaS providers, with automatic database detection and configuration.