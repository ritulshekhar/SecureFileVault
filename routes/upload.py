import os
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app, session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from app import db
from models import FileShare, User
import secrets
import string

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 
    'ppt', 'pptx', 'zip', 'rar', '7z', 'mp3', 'mp4', 'avi', 'mov', 'wav'
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_secure_filename(original_filename):
    """Generate a secure filename to prevent conflicts"""
    name, ext = os.path.splitext(original_filename)
    secure_name = secure_filename(name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    return f"{secure_name}_{timestamp}_{random_suffix}{ext}"

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # Check if user is logged in via session
    if 'user_id' not in session:
        flash('Please login to upload files', 'error')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        try:
            # Check if file was uploaded
            if 'file' not in request.files:
                flash('No file selected', 'error')
                return redirect(request.url)
            
            file = request.files['file']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(request.url)
            
            # Validate file type
            if not allowed_file(file.filename):
                flash('File type not allowed', 'error')
                return redirect(request.url)
            
            # Get form data
            password = request.form.get('password', '').strip()
            download_limit = request.form.get('download_limit', '').strip()
            expiry_hours = request.form.get('expiry_hours', '').strip()
            
            # Validate download limit
            if download_limit:
                try:
                    download_limit = int(download_limit)
                    if download_limit <= 0:
                        flash('Download limit must be a positive number', 'error')
                        return redirect(request.url)
                except ValueError:
                    flash('Invalid download limit', 'error')
                    return redirect(request.url)
            else:
                download_limit = None
            
            # Validate expiry time
            expires_at = None
            if expiry_hours:
                try:
                    expiry_hours = int(expiry_hours)
                    if expiry_hours <= 0:
                        flash('Expiry time must be a positive number', 'error')
                        return redirect(request.url)
                    expires_at = datetime.now(timezone.utc) + timedelta(hours=expiry_hours)
                except ValueError:
                    flash('Invalid expiry time', 'error')
                    return redirect(request.url)
            
            # Generate secure filename and save file
            secure_filename_generated = generate_secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename_generated)
            file.save(file_path)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Create file share record
            file_share = FileShare(
                filename=secure_filename_generated,
                original_filename=file.filename,
                file_path=file_path,
                file_size=file_size,
                download_limit=download_limit,
                expires_at=expires_at,
                user_id=session['user_id']
            )
            
            # Set password if provided
            if password:
                file_share.set_password(password)
            
            db.session.add(file_share)
            db.session.commit()
            
            # Generate share URL
            share_url = url_for('download.download_file', file_id=file_share.file_id, _external=True)
            
            flash(f'File uploaded successfully! Share URL: {share_url}', 'success')
            return redirect(url_for('dashboard'))
            
        except RequestEntityTooLarge:
            flash('File too large. Maximum size is 100MB.', 'error')
            return redirect(request.url)
        except Exception as e:
            current_app.logger.error(f"Upload error: {str(e)}")
            flash('An error occurred during upload. Please try again.', 'error')
            return redirect(request.url)
    
    return render_template('index.html')

@upload_bp.route('/delete/<file_id>', methods=['POST'])
def delete_file(file_id):
    """Delete a file share"""
    # Check if user is logged in via session
    if 'user_id' not in session:
        flash('Please login to delete files', 'error')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    file_share = FileShare.query.filter_by(file_id=file_id, user_id=user_id).first()
    
    if not file_share:
        flash('File not found', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # Delete physical file
        if os.path.exists(file_share.file_path):
            os.remove(file_share.file_path)
        
        # Delete database record
        db.session.delete(file_share)
        db.session.commit()
        
        flash('File deleted successfully', 'success')
    except Exception as e:
        current_app.logger.error(f"Delete error: {str(e)}")
        flash('An error occurred while deleting the file', 'error')
    
    return redirect(url_for('dashboard'))
