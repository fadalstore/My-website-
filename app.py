import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from flask_admin import Admin

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///blog.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    
    # Create default admin user if not exists
    from werkzeug.security import generate_password_hash
    admin_user = models.User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = models.User(
            username='admin',
            email=os.environ.get('ADMIN_EMAIL', 'admin@blog.com'),
            password_hash=generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'admin123')),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

# Import routes
from routes import *
from admin import setup_admin
setup_admin(app)
