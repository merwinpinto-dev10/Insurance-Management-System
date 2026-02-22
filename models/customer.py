from extensions import db
from datetime import datetime

class Customer(db.Model):
    """Customer model - represents customer table"""
    
    __tablename__ = 'customer'
    
    # Primary Key
    cus_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Customer Information
    cus_name = db.Column(db.String(100), nullable=False, index=True)
    cus_mobile = db.Column(db.String(15), nullable=False, index=True)
    cus_email = db.Column(db.String(100), unique=True, nullable=True, index=True)
    cus_add = db.Column(db.Text, nullable=True)
    cus_pass = db.Column(db.String(255), nullable=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Foreign Key - created by which user
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    insurances = db.relationship('Insurance', backref='customer', lazy=True, cascade='all, delete-orphan')
    bills = db.relationship('Bill', backref='customer', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='customer', lazy=True, cascade='all, delete-orphan')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_customers')
    
    def __init__(self, cus_name, cus_mobile, cus_email=None, cus_add=None, created_by=None):
        """Initialize Customer object"""
        self.cus_name = cus_name
        self.cus_mobile = cus_mobile
        self.cus_email = cus_email
        self.cus_add = cus_add
        self.created_by = created_by
        self.is_active = True
    
    def deactivate(self):
        """Deactivate customer"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def activate(self):
        """Activate customer"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def get_total_insurance_amount(self):
        """Calculate total insurance amount for this customer"""
        total = sum([ins.ins_amt for ins in self.insurances if ins.ins_status == 'Active'])
        return total
    
    def get_pending_bill_amount(self):
        """Calculate total pending bill amount"""
        total = sum([bill.bill_amount for bill in self.bills if bill.bill_status == 'Pending'])
        return total
    
    def __repr__(self):
        """String representation"""
        return f'<Customer {self.cus_name}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'cus_id': self.cus_id,
            'cus_name': self.cus_name,
            'cus_mobile': self.cus_mobile,
            'cus_email': self.cus_email,
            'cus_add': self.cus_add,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'total_insurances': len(self.insurances),
            'total_bills': len(self.bills),
            'total_payments': len(self.payments)
        }
