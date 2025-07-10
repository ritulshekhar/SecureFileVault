``` markdown

# SecureFileVault – Secure File Sharing Application

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
```

1. Create a virtual environment (optional but recommended)

```markdown

python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies

```markdown

pip install -r requirements.txt
```
3. Create a .env file

```markdown

cp .env.example .env
```

4. Initialize the database
   
```markdown
python main.py
```

5. Access the application
Open your browser and go to: http://localhost:5000

**Usage Guide**
1. Register
   Sign up with a username, email, and password.
2. Login
   Secure session-based login.
3. Upload a file
   Set optional password, download limit, and expiry time.
   Generate a secure link.
4. Share
   Distribute the link to intended recipients.
5. Manage
   View, track, and delete uploaded files from your dashboard.

**Supported File Types**
Documents: .txt, .pdf, .docx, .xlsx, .pptx
Images: .png, .jpg, .jpeg, .gif
Archives: .zip, .rar, .7z
Media: .mp3, .mp4, .avi, .mov, .wav

**PostgreSQL Support**

To switch to PostgreSQL:
```markdown
pip install psycopg2-binary
```

Set your .env:
```markdown
env
```

**Project Structure**

SecureFileVault/
├── app.py
├── main.py
├── models.py
├── requirements.txt
├── routes/
│   ├── auth.py
│   ├── upload.py
│   └── download.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
├── static/
│   └── style.css
├── uploads/
├── utils.py
└── .env.example

**Security Best Practices**
Passwords hashed with Werkzeug

Sessions securely managed

Uploads validated for type and size

Unique filenames prevent path guessing

CSRF and input validation built-in

**Development Mode**
```markdown
export FLASK_ENV=development
python main.py
```

**Deployment Tips**
Use Gunicorn or uWSGI for production
Use PostgreSQL instead of SQLite
Host static files with NGINX/CDN
Store files in S3 or similar object storage
Enable HTTPS and reverse proxy security

**License**
MIT License

**Contributing**
1. Fork this repo
2. Create a new branch
3. Commit your changes
4. Push and open a PR
