from extensions import db
from datetime import datetime, date

class Insurance(db.Model):
    """Insurance model - represents insurance table"""
    
    __tablename__ = 'insurance'
    
    # Primary Key
    ins_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    ins_cus_id = db.Column(db.Integer, db.ForeignKey('customer.cus_id'), nullable=False)
    
    # Insurance Information
    ins_type = db.Column(db.String(100), nullable=False, index=True)
    ins_num = db.Column(db.String(50), unique=True, nullable=False, index=True)
    ins_date = db.Column(db.Date, nullable=False, index=True)
    ins_amt = db.Column(db.Numeric(10, 2), nullable=False)
    ins_status = db.Column(db.String(20), default='Active', nullable=False, index=True)
    expiry_date = db.Column(db.Date, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, ins_cus_id, ins_type, ins_num, ins_date, ins_amt, expiry_date=None):
        """Initialize Insurance object"""
        self.ins_cus_id = ins_cus_id
        self.ins_type = ins_type
        self.ins_num = ins_num
        self.ins_date = ins_date
        self.ins_amt = ins_amt
        self.expiry_date = expiry_date
        self.ins_status = 'Active'
    
    def is_expired(self):
        """Check if insurance is expired"""
        if self.expiry_date:
            return date.today() > self.expiry_date
        return False
    
    def days_until_expiry(self):
        """Calculate days until expiry"""
        if self.expiry_date:
            delta = self.expiry_date - date.today()
            return delta.days
        return None
    
    def mark_expired(self):
        """Mark insurance as expired"""
        self.ins_status = 'Expired'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def renew(self, new_expiry_date):
        """Renew insurance"""
        self.ins_status = 'Active'
        self.expiry_date = new_expiry_date
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def cancel(self):
        """Cancel insurance"""
        self.ins_status = 'Cancelled'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        """String representation"""
        return f'<Insurance {self.ins_num}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'ins_id': self.ins_id,
            'ins_cus_id': self.ins_cus_id,
            'customer_name': self.customer.cus_name if self.customer else None,
            'ins_type': self.ins_type,
            'ins_num': self.ins_num,
            'ins_date': self.ins_date.strftime('%Y-%m-%d') if self.ins_date else None,
            'ins_amt': float(self.ins_amt) if self.ins_amt else 0,
            'ins_status': self.ins_status,
            'expiry_date': self.expiry_date.strftime('%Y-%m-%d') if self.expiry_date else None,
            'is_expired': self.is_expired(),
            'days_until_expiry': self.days_until_expiry()
        }
