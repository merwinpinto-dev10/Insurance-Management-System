"""
Database Setup Script
Run this script to initialize the database tables and create the admin user.
"""

from app import app
from extensions import db
from create_admin import create_admin_user

def setup():
    with app.app_context():
        print("\n" + "="*50)
        print("  Initializing Insurance Management System Database")
        print("="*50 + "\n")
        
        try:
            # Create all database tables
            print("Step 1: Creating database tables...")
            db.create_all()
            print("   ✅ Tables created successfully!")
            
            # Create admin user
            create_admin_user()
            
            print("\n" + "="*50)
            print("  🎉 Setup Complete! You can now run the application.")
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"\n❌ Error setting up database: {str(e)}")
            print("Please ensure your .env file has the correct database credentials.")

if __name__ == "__main__":
    setup()
