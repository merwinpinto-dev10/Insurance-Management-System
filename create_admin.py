"""
Create Admin User Script
Run this to create the initial admin user in your database
"""

from app import app
from extensions import db
from models.login import Login
from models.role import Role
from models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

def create_admin_user():
    """Create admin role and user"""
    
    with app.app_context():
        print("\n" + "="*50)
        print("Creating Admin User for Insurance Management System")
        print("="*50 + "\n")
        
        # Step 1: Create Admin Role if not exists
        print("Step 1: Checking for Admin role...")
        admin_role = Role.query.filter_by(role_name='Admin').first()
        
        if not admin_role:
            print("   Creating Admin role...")
            admin_role = Role(
                role_name='Admin',
                role_desc='System Administrator with full access'
            )
            db.session.add(admin_role)
            db.session.commit()
            print("   ✅ Admin role created! (ID: {})".format(admin_role.role_id))
        else:
            print("   ✅ Admin role already exists! (ID: {})".format(admin_role.role_id))
        
        # Step 2: Create Admin Login if not exists
        print("\nStep 2: Checking for admin login...")
        admin_login = Login.query.filter_by(login_username='admin').first()
        
        if not admin_login:
            print("   Creating admin login...")
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin_login = Login(
                login_username='admin',
                user_password=hashed_password,
                login_role_id=admin_role.role_id,
                is_active=True
            )
            db.session.add(admin_login)
            db.session.commit()
            print("   ✅ Admin login created! (ID: {})".format(admin_login.login_id))
        else:
            print("   ✅ Admin login already exists! (ID: {})".format(admin_login.login_id))
        
        # Step 3: Create Admin User if not exists
        print("\nStep 3: Checking for admin user profile...")
        admin_user = User.query.filter_by(login_id=admin_login.login_id).first()
        
        if not admin_user:
            print("   Creating admin user profile...")
            admin_user = User(
                login_id=admin_login.login_id,
                user_name='System Administrator',
                user_mobile='0000000000',
                user_email='admin@insurance.com',
                user_address='System'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("   ✅ Admin user profile created! (ID: {})".format(admin_user.user_id))
        else:
            print("   ✅ Admin user profile already exists! (ID: {})".format(admin_user.user_id))
        
        # Summary
        print("\n" + "="*50)
        print("SUCCESS! Admin user is ready!")
        print("="*50)
        print("\n📋 Login Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n🌐 Access your application at:")
        print("   http://localhost:5000/auth/login")
        print("\n⚠️  IMPORTANT: Change the password after first login!")
        print("="*50 + "\n")


if __name__ == '__main__':
    try:
        create_admin_user()
    except Exception as e:
        print("\n❌ Error creating admin user:")
        print(f"   {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL is running")
        print("2. Check database connection in .env file")
        print("3. Verify database 'insurance_management' exists")
        print("4. Make sure all required packages are installed")
        print("   Run: pip install -r requirements.txt")
