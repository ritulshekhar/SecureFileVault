from flask import Blueprint, request, render_template, redirect, url_for, flash, session, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, set_access_cookies
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
            # Create JWT token
            access_token = create_access_token(identity=user.id)
            
            # Store token in session for template access
            session['access_token'] = access_token
            session['user_id'] = user.id
            session['username'] = user.username
            
            # Create response with JWT cookie
            response = make_response(redirect(url_for('dashboard')))
            set_access_cookies(response, access_token)
            
            flash('Login successful', 'success')
            return response
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
@jwt_required()
def logout():
    # Clear session
    session.clear()
    
    # Create response and unset JWT cookies
    response = make_response(redirect(url_for('index')))
    unset_jwt_cookies(response)
    
    flash('You have been logged out', 'info')
    return response

@auth_bp.route('/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
