from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from app import db
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Store user info in session
            session['user_id'] = user.id
            session['username'] = user.username
            
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('login.html', show_register=True)
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('login.html', show_register=True)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('login.html', show_register=True)
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('login.html', show_register=True)
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('login.html', show_register=True)
        
        # Create new user
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('login.html', show_register=True)
    
    return render_template('login.html', show_register=True)

@auth_bp.route('/logout')
def logout():
    # Clear session
    session.clear()
    
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/profile')
def profile():
    # Check if user is logged in via session
    if 'user_id' not in session:
        flash('Please login to view profile', 'error')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
