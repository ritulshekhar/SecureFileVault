``` markdown
# Define the README content without emojis
readme_content_plain = """
# SecureShare – Secure File Sharing Application

A Flask-based web application for secure file sharing with authentication, password protection, download limits, and expiration features.

## Features

### Core Functionality
- Secure File Upload: Upload files up to 100MB with secure, unique filenames
- User Authentication: Full registration and login system with session management
- Password Protection: Optional password protection for shared files
- Download Limits: Set the maximum number of downloads per file
- Expiration Dates: Set file expiration time (hours or days)
- Secure URLs: Generate unique, non-guessable sharing links

### Security Features
- Password hashing with Werkzeug security utilities
- Session-based user authentication
- CSRF protection via Flask
- File name & type validation
- Input sanitization and validation

### User Interface
- Clean, responsive Bootstrap 5 design with dark mode
- Dashboard for managing uploaded files
- Upload form with security options
- Download interface with password and link validation

## Tech Stack

- Backend: Flask (Python)
- Database: SQLite by default (PostgreSQL supported)
- Frontend: Bootstrap 5 + Jinja2 Templates
- Authentication: Flask Sessions (JWT support possible)
- File Storage: Local file system (S3 optional for production)

## Installation

### Prerequisites
- Python 3.8 or later
- pip package manager

### Local Setup

1. Clone the repository
   ```bash
   git clone https://github.com/your-username/SecureShare.git
   cd SecureShare
```
