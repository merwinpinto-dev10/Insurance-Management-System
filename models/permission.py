from extensions import db
from datetime import datetime

class Permission(db.Model):
    """Permission model - represents permission table"""
    
    __tablename__ = 'permission'
    
    # Primary Key
    per_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    per_role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    
    # Permission Information
    per_name = db.Column(db.String(100), nullable=False)
    per_module = db.Column(db.String(50), nullable=False, index=True)
    
    # CRUD Permissions
    can_create = db.Column(db.Boolean, default=False, nullable=False)
    can_read = db.Column(db.Boolean, default=False, nullable=False)
    can_update = db.Column(db.Boolean, default=False, nullable=False)
    can_delete = db.Column(db.Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Unique constraint for role and module combination
    __table_args__ = (
        db.UniqueConstraint('per_role_id', 'per_module', name='unique_role_module'),
    )
    
    def __init__(self, per_role_id, per_name, per_module, 
                 can_create=False, can_read=False, can_update=False, can_delete=False):
        """Initialize Permission object"""
        self.per_role_id = per_role_id
        self.per_name = per_name
        self.per_module = per_module
        self.can_create = can_create
        self.can_read = can_read
        self.can_update = can_update
        self.can_delete = can_delete
    
    def has_access(self, action):
        """Check if permission allows specific action"""
        action = action.lower()
        if action == 'create':
            return self.can_create
        elif action == 'read':
            return self.can_read
        elif action == 'update':
            return self.can_update
        elif action == 'delete':
            return self.can_delete
        return False
    
    def grant_all(self):
        """Grant all permissions"""
        self.can_create = True
        self.can_read = True
        self.can_update = True
        self.can_delete = True
        self.updated_at = datetime.utcnow()
    
    def revoke_all(self):
        """Revoke all permissions"""
        self.can_create = False
        self.can_read = False
        self.can_update = False
        self.can_delete = False
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        """String representation"""
        return f'<Permission {self.per_name} - {self.per_module}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'per_id': self.per_id,
            'per_role_id': self.per_role_id,
            'role_name': self.role.role_name if self.role else None,
            'per_name': self.per_name,
            'per_module': self.per_module,
            'can_create': self.can_create,
            'can_read': self.can_read,
            'can_update': self.can_update,
            'can_delete': self.can_delete
        }
