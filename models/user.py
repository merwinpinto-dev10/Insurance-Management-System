from extensions import db
from datetime import datetime

class User(db.Model):
    """User model - represents user table"""
    
    __tablename__ = 'user'
    
    # Primary Key
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    login_id = db.Column(db.Integer, db.ForeignKey('login.login_id'), unique=True, nullable=False)
    
    # User Information
    user_name = db.Column(db.String(100), nullable=False)
    user_mobile = db.Column(db.String(15), nullable=False, index=True)
    user_email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_address = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, login_id, user_name, user_mobile, user_email, user_address=None):
        """Initialize User object"""
        self.login_id = login_id
        self.user_name = user_name
        self.user_mobile = user_mobile
        self.user_email = user_email
        self.user_address = user_address
    
    def __repr__(self):
        """String representation"""
        return f'<User {self.user_name}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'login_id': self.login_id,
            'user_name': self.user_name,
            'user_mobile': self.user_mobile,
            'user_email': self.user_email,
            'user_address': self.user_address,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
