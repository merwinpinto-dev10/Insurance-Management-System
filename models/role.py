from extensions import db
from datetime import datetime

class Role(db.Model):
    """Role model - represents roles table"""
    
    __tablename__ = 'roles'
    
    # Primary Key
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Role Information
    role_name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    role_desc = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    permissions = db.relationship('Permission', backref='role', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, role_name, role_desc=None):
        """Initialize Role object"""
        self.role_name = role_name
        self.role_desc = role_desc
    
    def is_admin(self):
        """Check if this is admin role"""
        return self.role_name.lower() == 'admin'
    
    def is_manager(self):
        """Check if this is manager role"""
        return self.role_name.lower() == 'manager'
    
    def is_agent(self):
        """Check if this is agent role"""
        return self.role_name.lower() == 'agent'
    
    def __repr__(self):
        """String representation"""
        return f'<Role {self.role_name}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'role_desc': self.role_desc,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
