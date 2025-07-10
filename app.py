import os
import logging
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, set_access_cookies
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False  # Set to True in production with HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Simplified for development
jwt = JWTManager(app)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///secureshare.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# File upload configuration
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100MB max file size
app.config["UPLOAD_FOLDER"] = "uploads"

# Initialize extensions
db.init_app(app)
jwt.init_app(app)

# Create upload folder if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Import and register blueprints
from routes.upload import upload_bp
from routes.download import download_bp
from routes.auth import auth_bp

app.register_blueprint(upload_bp)
app.register_blueprint(download_bp)
app.register_blueprint(auth_bp)

# Main routes
from flask import render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@jwt_required()
def dashboard():
    from models import FileShare, User
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    files = FileShare.query.filter_by(user_id=user_id).order_by(FileShare.created_at.desc()).all()
    return render_template('dashboard.html', user=user, files=files)

@app.route('/download-project')
def download_project():
    """Download the entire project as a zip file"""
    from flask import send_file
    import os
    
    zip_path = 'secureshare.zip'
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True, download_name='secureshare-project.zip')
    else:
        flash('Project zip file not found', 'error')
        return redirect(url_for('index'))

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
