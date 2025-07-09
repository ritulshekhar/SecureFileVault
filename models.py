from app import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import string

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationship with file shares
    file_shares = db.relationship('FileShare', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class FileShare(db.Model):
    __tablename__ = 'file_shares'
    
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    
    # Security settings
    password_hash = db.Column(db.String(256), nullable=True)
    download_limit = db.Column(db.Integer, nullable=True)
    download_count = db.Column(db.Integer, default=0)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    # Metadata
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_accessed = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.file_id:
            self.file_id = self.generate_file_id()
    
    @staticmethod
    def generate_file_id():
        """Generate a secure random file ID"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(12))
    
    def set_password(self, password):
        """Set password protection for the file"""
        if password:
            self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches"""
        if not self.password_hash:
            return True  # No password protection
        return check_password_hash(self.password_hash, password)
    
    def is_expired(self):
        """Check if the file link has expired"""
        if not self.expires_at:
            return False
        return datetime.now(timezone.utc) > self.expires_at
    
    def is_download_limit_reached(self):
        """Check if download limit has been reached"""
        if not self.download_limit:
            return False
        return self.download_count >= self.download_limit
    
    def can_download(self):
        """Check if file can be downloaded"""
        return not self.is_expired() and not self.is_download_limit_reached()
    
    def increment_download_count(self):
        """Increment download count and update last accessed time"""
        self.download_count += 1
        self.last_accessed = datetime.now(timezone.utc)
        db.session.commit()
    
    def __repr__(self):
        return f'<FileShare {self.file_id}: {self.original_filename}>'
