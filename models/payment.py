from extensions import db
from datetime import datetime, date

class Payment(db.Model):
    """Payment model - represents payment table"""
    
    __tablename__ = 'payment'
    
    # Primary Key
    pay_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    pay_cus_id = db.Column(db.Integer, db.ForeignKey('customer.cus_id'), nullable=False)
    pay_bill_id = db.Column(db.Integer, db.ForeignKey('bill.bill_id'), nullable=True)
    
    # Payment Information
    pay_type = db.Column(db.String(50), nullable=False)
    pay_desc = db.Column(db.Text, nullable=True)
    pay_date = db.Column(db.Date, nullable=False, index=True)
    pay_amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=True)
    transaction_ref = db.Column(db.String(100), nullable=True, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, pay_cus_id, pay_type, pay_date, pay_amount, 
                 pay_bill_id=None, pay_desc=None, payment_method=None, transaction_ref=None):
        """Initialize Payment object"""
        self.pay_cus_id = pay_cus_id
        self.pay_bill_id = pay_bill_id
        self.pay_type = pay_type
        self.pay_date = pay_date
        self.pay_amount = pay_amount
        self.pay_desc = pay_desc
        self.payment_method = payment_method
        self.transaction_ref = transaction_ref
    
    def __repr__(self):
        """String representation"""
        return f'<Payment {self.pay_id} - {self.transaction_ref}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'pay_id': self.pay_id,
            'pay_cus_id': self.pay_cus_id,
            'customer_name': self.customer.cus_name if self.customer else None,
            'pay_bill_id': self.pay_bill_id,
            'bill_num': self.bill.bill_num if self.bill else None,
            'pay_type': self.pay_type,
            'pay_desc': self.pay_desc,
            'pay_date': self.pay_date.strftime('%Y-%m-%d') if self.pay_date else None,
            'pay_amount': float(self.pay_amount) if self.pay_amount else 0,
            'payment_method': self.payment_method,
            'transaction_ref': self.transaction_ref,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
