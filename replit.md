# SecureShare - Secure File Sharing Application

## Overview

SecureShare is a Flask-based web application that provides secure file sharing capabilities with authentication, password protection, download limits, and expiration dates. Users can upload files and generate secure sharing links with various security options.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

- **Authentication System Update (July 10, 2025)**: Converted from JWT cookie-based authentication to session-based authentication to resolve cookie access issues during file uploads
- **README Documentation (July 10, 2025)**: Created comprehensive README.md with installation instructions, usage guide, security considerations, and project structure documentation

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens) with Flask-JWT-Extended
- **File Storage**: Local filesystem with secure filename generation
- **Session Management**: Flask sessions for user state

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with dark theme
- **Icons**: Font Awesome
- **JavaScript**: Minimal, relies on Bootstrap components

### Security Features
- Password hashing using Werkzeug's security utilities
- JWT tokens for API authentication
- Secure filename generation with timestamps and random suffixes
- File type validation and size limits
- Optional password protection for shared files
- Download limits and expiration dates
- CSRF protection through Flask's built-in mechanisms

## Key Components

### Models (`models.py`)
- **User Model**: Handles user authentication and profile data
  - Fields: id, username, email, password_hash, created_at
  - Methods: set_password(), check_password()
  - Relationships: One-to-many with FileShare

- **FileShare Model**: Manages file sharing metadata
  - Fields: file_id, filename, original_filename, file_path, file_size
  - Security: password_hash, download_limit, download_count, expires_at
  - Metadata: user_id, created_at, last_accessed

### Routes
- **Authentication (`routes/auth.py`)**: Login, register, logout functionality
- **Upload (`routes/upload.py`)**: File upload with security options
- **Download (`routes/download.py`)**: Secure file download with access controls

### Utilities (`utils.py`)
- Secure token generation
- File ID generation for URLs
- Filename sanitization and timestamp generation
- File size formatting
- Security validation functions

## Data Flow

1. **User Registration/Login**:
   - User submits credentials → Authentication validation → JWT token generation → Session storage

2. **File Upload**:
   - User selects file → File validation → Secure filename generation → Database record creation → File storage

3. **File Sharing**:
   - Generate secure file ID → Create shareable URL → Apply security settings (password, limits, expiration)

4. **File Download**:
   - Access via file ID → Security checks (password, limits, expiration) → File delivery → Usage tracking

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Flask-JWT-Extended: JWT authentication
- Werkzeug: Security utilities and file handling
- PostgreSQL adapter (psycopg2 or similar)

### Frontend Dependencies
- Bootstrap 5 (CDN): UI framework
- Font Awesome (CDN): Icons
- Bootstrap Agent Dark Theme (CDN): Dark mode styling

### System Dependencies
- PostgreSQL database server
- File system access for upload storage

## Deployment Strategy

### Configuration
- Environment variables for sensitive data (DATABASE_URL, JWT_SECRET_KEY, SESSION_SECRET)
- Configurable file upload limits and storage location
- Database connection pooling for performance

### Security Considerations
- ProxyFix middleware for reverse proxy compatibility
- Secure file storage outside web root
- Input validation and sanitization
- Rate limiting considerations (not implemented but recommended)

### Scalability Notes
- Local file storage limits horizontal scaling
- Database connection pooling configured
- Session storage in cookies (stateless JWT approach)
- Upload folder creation on startup

### Missing Components for Production
- Database migrations system
- Error handling and logging improvements
- File cleanup for expired shares
- Email notifications
- Admin interface
- API rate limiting
- Cloud storage integration
- SSL/HTTPS configuration