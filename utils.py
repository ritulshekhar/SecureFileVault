import os
import secrets
import string
from datetime import datetime, timezone
from werkzeug.utils import secure_filename

def generate_secure_token(length=32):
    """Generate a secure random token"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_file_id(length=12):
    """Generate a secure file ID for URLs"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def secure_filename_with_timestamp(filename):
    """Generate a secure filename with timestamp"""
    name, ext = os.path.splitext(filename)
    secure_name = secure_filename(name)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    random_suffix = generate_secure_token(6)
    return f"{secure_name}_{timestamp}_{random_suffix}{ext}"

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def is_safe_filename(filename):
    """Check if filename is safe for storage"""
    if not filename:
        return False
    
    # Check for dangerous characters
    dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in dangerous_chars:
        if char in filename:
            return False
    
    # Check if filename is too long
    if len(filename) > 255:
        return False
    
    return True

def validate_file_type(filename, allowed_extensions):
    """Validate file type against allowed extensions"""
    if not filename:
        return False
    
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions

def clean_old_files(upload_folder, max_age_days=30):
    """Clean up old files from upload folder"""
    if not os.path.exists(upload_folder):
        return
    
    now = datetime.now(timezone.utc)
    cutoff_time = now.timestamp() - (max_age_days * 24 * 60 * 60)
    
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        if os.path.isfile(file_path):
            file_time = os.path.getmtime(file_path)
            if file_time < cutoff_time:
                try:
                    os.remove(file_path)
                    print(f"Cleaned up old file: {filename}")
                except OSError as e:
                    print(f"Error cleaning up file {filename}: {e}")

def get_file_mime_type(filename):
    """Get MIME type for file"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    mime_types = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'ppt': 'application/vnd.ms-powerpoint',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'zip': 'application/zip',
        'rar': 'application/x-rar-compressed',
        '7z': 'application/x-7z-compressed',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'mp4': 'video/mp4',
        'avi': 'video/x-msvideo',
        'mov': 'video/quicktime'
    }
    
    return mime_types.get(ext, 'application/octet-stream')
