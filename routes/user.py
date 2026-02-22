from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models.user import User
from models.login import Login
from models.role import Role
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
@login_required
def index():
    """List all users"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('user/list.html', users=users)

@user_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new user"""
    if request.method == 'POST':
        try:
            # Personal Info
            user_name = request.form.get('user_name')
            user_mobile = request.form.get('user_mobile')
            user_email = request.form.get('user_email')
            user_address = request.form.get('user_address')
            
            # Login Info
            login_username = request.form.get('login_username')
            user_password = request.form.get('user_password')
            login_role_id = request.form.get('login_role_id')
            is_active = request.form.get('is_active', '0') == '1' # Default to '0' if not present, then check if '1'
            
            # Validation
            if not all([user_name, user_mobile, user_email, login_username, user_password, login_role_id]):
                flash('Please fill in all required fields.', 'danger')
                return redirect(url_for('user.add'))
            
            # Check duplicates
            if Login.query.filter_by(login_username=login_username).first():
                flash('Username already exists.', 'danger')
                return redirect(url_for('user.add'))
            
            if User.query.filter_by(user_email=user_email).first():
                flash('Email already registered.', 'danger')
                return redirect(url_for('user.add'))
            
            # Create Login First
            new_login = Login(
                login_username=login_username,
                login_role_id=int(login_role_id),
                is_active=is_active
            )
            new_login.set_password(user_password) # This method should hash the password
            
            db.session.add(new_login)
            db.session.flush() # Flush to get login_id
            
            # Create User linked to Login
            new_user = User(
                login_id=new_login.login_id,
                user_name=user_name,
                user_mobile=user_mobile,
                user_email=user_email,
                user_address=user_address
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('User account created successfully!', 'success')
            return redirect(url_for('user.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}', 'danger')
            return redirect(url_for('user.add'))

    roles = Role.query.all()
    return render_template('user/add.html', roles=roles)


@user_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit user"""
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Update Personal Info
            user.user_name = request.form.get('user_name')
            user.user_mobile = request.form.get('user_mobile')
            user.user_email = request.form.get('user_email')
            user.user_address = request.form.get('user_address')
            
            # Update Login Info
            login_role_id = request.form.get('login_role_id')
            is_active = request.form.get('is_active') == '1'
            
            if user.login:
                user.login.login_role_id = int(login_role_id)
                user.login.is_active = is_active
            
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('User updated successfully!', 'success')
            return redirect(url_for('user.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'danger')
            return redirect(url_for('user.edit', id=id))
            
    roles = Role.query.all()
    return render_template('user/edit.html', user=user, roles=roles)


@user_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Delete user"""
    try:
        user = User.query.get_or_404(id)
        # Login is parent of User, but User has Foreign Key to Login.
        # Actually User refers to Login. Login does NOT refer to User in DB (User has login_id).
        # But `User` model has a relationship?
        # If we delete User, we should probably delete Login too?
        # Or just deactivate? logic says "Delete" so let's delete both.
        
        login_record = user.login
        
        db.session.delete(user)
        if login_record:
            db.session.delete(login_record)
            
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'danger')
        
    return redirect(url_for('user.index'))
