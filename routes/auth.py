from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, login_manager
from models.login import Login
from models.user import User

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(login_id):
    """Load user by login_id"""
    return Login.query.get(int(login_id))

@auth_bp.route('/')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        # Validation
        if not username or not password:
            flash('Please enter both username and password', 'danger')
            return render_template('auth/login.html')
        
        # Find user
        login = Login.query.filter_by(login_username=username).first()
        
        if login and login.check_password(password):
            # Check if account is active
            if not login.is_active:
                flash('Your account has been deactivated. Please contact administrator.', 'warning')
                return render_template('auth/login.html')
            
            # Update last login
            login.update_last_login()
            
            # Login user
            login_user(login, remember=remember)
            
            # Store additional info in session
            if login.user:
                session['user_name'] = login.user.user_name
                session['role_name'] = login.role.role_name if login.role else 'Unknown'
            
            flash(f'Welcome back, {username}!', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    username = current_user.login_username if current_user.is_authenticated else 'User'
    logout_user()
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password page"""
    
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not all([current_password, new_password, confirm_password]):
            flash('All fields are required', 'danger')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return render_template('auth/change_password.html')
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return render_template('auth/change_password.html')
        
        # Verify current password
        if not current_user.check_password(current_password):
            flash('Current password is incorrect', 'danger')
            return render_template('auth/change_password.html')
        
        # Update password
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('dashboard.index'))
    
    return render_template('auth/change_password.html')
