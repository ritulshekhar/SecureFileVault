import os
from datetime import datetime, timezone
from flask import Blueprint, request, render_template, send_file, flash, redirect, url_for, current_app
from app import db
from models import FileShare

download_bp = Blueprint('download', __name__)

@download_bp.route('/d/<file_id>', methods=['GET', 'POST'])
def download_file(file_id):
    """Handle file download with security checks"""
    file_share = FileShare.query.filter_by(file_id=file_id).first()
    
    if not file_share:
        flash('File not found or link is invalid', 'error')
        return render_template('download.html', error='File not found')
    
    # Check if file expired
    if file_share.is_expired():
        flash('Download link has expired', 'error')
        return render_template('download.html', error='Link expired', file_share=file_share)
    
    # Check if download limit reached
    if file_share.is_download_limit_reached():
        flash('Download limit has been reached', 'error')
        return render_template('download.html', error='Download limit reached', file_share=file_share)
    
    # Check if file exists on disk
    if not os.path.exists(file_share.file_path):
        flash('File no longer exists on server', 'error')
        return render_template('download.html', error='File not found on server', file_share=file_share)
    
    # Handle password protection
    if file_share.password_hash:
        if request.method == 'POST':
            password = request.form.get('password', '')
            if not file_share.check_password(password):
                flash('Incorrect password', 'error')
                return render_template('download.html', 
                                     file_share=file_share, 
                                     password_required=True, 
                                     error='Incorrect password')
        else:
            # Show password form
            return render_template('download.html', 
                                 file_share=file_share, 
                                 password_required=True)
    
    # All checks passed - serve the file
    try:
        # Increment download count
        file_share.increment_download_count()
        
        # Send file
        return send_file(
            file_share.file_path,
            as_attachment=True,
            download_name=file_share.original_filename
        )
    except Exception as e:
        current_app.logger.error(f"Download error: {str(e)}")
        flash('An error occurred while downloading the file', 'error')
        return render_template('download.html', error='Download error', file_share=file_share)

@download_bp.route('/info/<file_id>')
def file_info(file_id):
    """Show file information without downloading"""
    file_share = FileShare.query.filter_by(file_id=file_id).first()
    
    if not file_share:
        flash('File not found', 'error')
        return render_template('download.html', error='File not found')
    
    return render_template('download.html', 
                         file_share=file_share, 
                         show_info=True)
