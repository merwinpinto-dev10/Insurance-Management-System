from extensions import db
from datetime import datetime, date

class Bill(db.Model):
    """Bill model - represents bill table"""
    
    __tablename__ = 'bill'
    
    # Primary Key
    bill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    bill_cus_id = db.Column(db.Integer, db.ForeignKey('customer.cus_id'), nullable=False)
    
    # Bill Information
    bill_num = db.Column(db.String(50), unique=True, nullable=False, index=True)
    bill_amount = db.Column(db.Numeric(10, 2), nullable=False)
    bill_date = db.Column(db.Date, nullable=False, index=True)
    due_date = db.Column(db.Date, nullable=True)
    bill_status = db.Column(db.String(20), default='Pending', nullable=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    payments = db.relationship('Payment', backref='bill', lazy=True)
    
    def __init__(self, bill_cus_id, bill_num, bill_amount, bill_date, due_date=None):
        """Initialize Bill object"""
        self.bill_cus_id = bill_cus_id
        self.bill_num = bill_num
        self.bill_amount = bill_amount
        self.bill_date = bill_date
        self.due_date = due_date
        self.bill_status = 'Pending'
    
    def is_overdue(self):
        """Check if bill is overdue"""
        if self.due_date and self.bill_status == 'Pending':
            return date.today() > self.due_date
        return False
    
    def days_overdue(self):
        """Calculate days overdue"""
        if self.is_overdue():
            delta = date.today() - self.due_date
            return delta.days
        return 0
    
    def mark_paid(self):
        """Mark bill as paid"""
        self.bill_status = 'Paid'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def mark_overdue(self):
        """Mark bill as overdue"""
        self.bill_status = 'Overdue'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def get_paid_amount(self):
        """Calculate total paid amount from payments"""
        total = sum([float(payment.pay_amount) for payment in self.payments])
        return total
    
    def get_balance(self):
        """Calculate remaining balance"""
        return float(self.bill_amount) - self.get_paid_amount()
    
    def __repr__(self):
        """String representation"""
        return f'<Bill {self.bill_num}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'bill_id': self.bill_id,
            'bill_cus_id': self.bill_cus_id,
            'customer_name': self.customer.cus_name if self.customer else None,
            'bill_num': self.bill_num,
            'bill_amount': float(self.bill_amount) if self.bill_amount else 0,
            'bill_date': self.bill_date.strftime('%Y-%m-%d') if self.bill_date else None,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'bill_status': self.bill_status,
            'is_overdue': self.is_overdue(),
            'days_overdue': self.days_overdue(),
            'paid_amount': self.get_paid_amount(),
            'balance': self.get_balance()
        }
