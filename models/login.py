from extensions import db
from flask_login import UserMixin
from datetime import datetime

class Login(db.Model, UserMixin):
    """Login model - represents login table"""
    
    __tablename__ = 'login'
    
    # Primary Key
    login_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    login_role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    
    # Credentials
    login_username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_password = db.Column(db.String(255), nullable=False)
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    role = db.relationship('Role', backref=db.backref('logins', lazy=True))
    user = db.relationship('User', backref='login', uselist=False, cascade='all, delete-orphan')
    
    def __init__(self, login_username, user_password, login_role_id, is_active=True):
        """Initialize Login object"""
        self.login_username = login_username
        self.user_password = user_password
        self.login_role_id = login_role_id
        self.is_active = is_active
    
    # Flask-Login required methods
    def get_id(self):
        """Return user ID for Flask-Login"""
        return str(self.login_id)
    
    @property
    def is_authenticated(self):
        """Return True if user is authenticated"""
        return True
    
    @property
    def is_anonymous(self):
        """Return False - user is not anonymous"""
        return False
    
    # Utility methods
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def deactivate(self):
        """Deactivate this login account"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def activate(self):
        """Activate this login account"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def set_password(self, password):
        """Hash and set password"""
        from extensions import bcrypt
        self.user_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        from extensions import bcrypt
        return bcrypt.check_password_hash(self.user_password, password)
    
    def has_permission(self, module, action):
        """Check if user has specific permission"""
        # Admin has all permissions
        if self.role and self.role.role_name == 'Admin':
            return True
        
        # Check specific permissions (will implement later with Permission model)
        return False
    
    def __repr__(self):
        """String representation"""
        return f'<Login {self.login_username}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'login_id': self.login_id,
            'login_username': self.login_username,
            'login_role_id': self.login_role_id,
            'role_name': self.role.role_name if self.role else None,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None
        }
