from flask import Blueprint, render_template
from flask_login import login_required
from models.customer import Customer
from models.insurance import Insurance
from models.bill import Bill
from models.payment import Payment
from extensions import db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard with summary statistics"""
    total_customers = Customer.query.count()
    active_policies = Insurance.query.filter_by(ins_status='Active').count()
    total_revenue_result = db.session.query(func.sum(Payment.pay_amount)).scalar()
    total_revenue = float(total_revenue_result) if total_revenue_result else 0.0
    pending_bills = Bill.query.filter_by(bill_status='Pending').count()
    
    # Recent items
    recent_customers = Customer.query.order_by(Customer.created_at.desc()).limit(5).all()
    recent_payments = Payment.query.order_by(Payment.pay_date.desc()).limit(5).all()
    
    return render_template('dashboard/index.html',
                          total_customers=total_customers,
                          active_policies=active_policies,
                          total_revenue=total_revenue,
                          pending_bills=pending_bills,
                          recent_customers=recent_customers,
                          recent_payments=recent_payments)
