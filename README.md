# SecureShare - Secure File Sharing Application

A Flask-based web application for secure file sharing with authentication, password protection, download limits, and expiration features.

## Features

### Core Functionality
- **Secure File Upload**: Upload files up to 100MB with secure filename generation
- **User Authentication**: Complete registration and login system with session management
- **Password Protection**: Optional password protection for shared files
- **Download Limits**: Set maximum number of downloads per file
- **Expiration Dates**: Set time limits for file availability
- **Secure URLs**: Generate unique, secure sharing links

### Security Features
- Session-based authentication
- Password hashing using Werkzeug security utilities
- Secure filename generation with timestamps and random suffixes
- File type validation
- CSRF protection through Flask's built-in mechanisms
- Input validation and sanitization

### User Interface
- Clean, responsive Bootstrap 5 design with dark theme
- User dashboard for managing uploaded files
- File upload form with security options
- Download interface with access controls

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (easily configurable for PostgreSQL)
- **Frontend**: Bootstrap 5 with dark theme, Jinja2 templates
- **Authentication**: Session-based with Flask sessions
- **File Storage**: Local filesystem with secure handling

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Setup

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd secureshare
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables** (optional)
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   export DATABASE_URL="sqlite:///secureshare.db"
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Usage

### Getting Started

1. **Register a new account**
   - Click "Register" on the login page
   - Fill in username, email, and password
   - Submit the form to create your account

2. **Login**
   - Use your credentials to login
   - You'll be redirected to your dashboard

3. **Upload a file**
   - Click "Upload File" from the dashboard
   - Select a file (max 100MB)
   - Optionally set:
     - Password protection
     - Download limit (number of allowed downloads)
     - Expiration time (in hours)
   - Click "Upload" to generate a secure sharing link

4. **Share files**
   - Copy the generated sharing URL
   - Share it with intended recipients
   - Recipients can access the file through the link

5. **Manage files**
   - View all your uploaded files in the dashboard
   - See download statistics and expiration status
   - Delete files when no longer needed

### File Sharing Options

- **No Protection**: File is accessible to anyone with the link
- **Password Protection**: Recipients need a password to download
- **Download Limits**: Limit how many times the file can be downloaded
- **Expiration**: Set when the sharing link expires

## File Types Supported

The application supports a wide range of file types including:
- Documents: txt, pdf, doc, docx, xls, xlsx, ppt, pptx
- Images: png, jpg, jpeg, gif
- Archives: zip, rar, 7z
- Media: mp3, mp4, avi, mov, wav

## Configuration

### Environment Variables

- `SESSION_SECRET`: Secret key for session management (default: auto-generated)
- `DATABASE_URL`: Database connection URL (default: SQLite)
- `JWT_SECRET_KEY`: JWT secret key (if using JWT features)

### Database Configuration

The application uses SQLite by default for easy setup. To use PostgreSQL:

1. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Set the DATABASE_URL:
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost/secureshare"
   ```

## Project Structure

```
secureshare/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── routes/
│   ├── auth.py          # Authentication routes
│   ├── upload.py        # File upload routes
│   └── download.py      # File download routes
├── templates/
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── login.html       # Login/register page
│   └── dashboard.html   # User dashboard
├── static/
│   └── style.css        # Custom styles
├── uploads/             # File storage directory
└── utils.py             # Utility functions
```

## Security Considerations

### Production Deployment

For production use, consider:

1. **Use HTTPS**: Enable SSL/TLS encryption
2. **Secure Database**: Use PostgreSQL with proper authentication
3. **Environment Variables**: Store sensitive data in environment variables
4. **File Storage**: Consider cloud storage for scalability
5. **Rate Limiting**: Implement rate limiting for uploads and downloads
6. **Backup Strategy**: Regular database and file backups

### Security Best Practices

- Files are stored with secure, randomized filenames
- User passwords are hashed using Werkzeug's security utilities
- Session management prevents unauthorized access
- File type validation prevents malicious uploads
- Input validation and sanitization throughout the application

## Troubleshooting

### Common Issues

1. **Upload fails**: Check file size (max 100MB) and file type
2. **Authentication issues**: Clear browser cookies and try again
3. **Database errors**: Ensure database is accessible and has proper permissions
4. **File not found**: Check if file has expired or reached download limit

### Development

To run in development mode:
```bash
export FLASK_ENV=development
python main.py
```

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section
- Review the code documentation
- Create an issue in the project repository

---

**Note**: This application is designed for secure file sharing. Always follow security best practices when deploying to production environments.