from flask import Blueprint, render_template, request, send_file, flash
from flask_login import login_required
from extensions import db
from models.customer import Customer
from models.insurance import Insurance
from models.bill import Bill
from models.payment import Payment
from models.user import User
from datetime import datetime
from sqlalchemy import func

report_bp = Blueprint('report', __name__, url_prefix='/report')

@report_bp.route('/')
@login_required
def index():
    """Report dashboard with stats"""
    # Calculate stats
    total_customers = Customer.query.count()
    active_policies = Insurance.query.filter_by(ins_status='Active').count()
    
    # Calculate total revenue (sum of payments)
    total_revenue_result = db.session.query(func.sum(Payment.pay_amount)).scalar()
    total_revenue = float(total_revenue_result) if total_revenue_result else 0.0
    
    pending_bills = Bill.query.filter_by(bill_status='Pending').count()
    
    return render_template('report/index.html', 
                          total_customers=total_customers,
                          active_policies=active_policies,
                          total_revenue=total_revenue,
                          pending_bills=pending_bills)

@report_bp.route('/customers')
@login_required
def customers():
    """Customer report"""
    customers = Customer.query.order_by(Customer.cus_name).all()
    
    headers = ['ID', 'Name', 'Mobile', 'Email', 'Address', 'Status', 'Created']
    data = []
    
    for c in customers:
        data.append([
            c.cus_id,
            c.cus_name,
            c.cus_mobile,
            c.cus_email or '-',
            c.cus_add or '-',
            'Active' if c.is_active else 'Inactive',
            c.created_at.strftime('%Y-%m-%d')
        ])
        
    return render_template('report/view_report.html', 
                          title='Customer Report',
                          headers=headers,
                          data=data)

@report_bp.route('/insurance')
@login_required
def insurance():
    """Insurance report"""
    insurances = Insurance.query.order_by(Insurance.created_at.desc()).all()
    
    headers = ['Policy #', 'Customer', 'Type', 'Amount', 'Issue Date', 'Expiry Date', 'Status']
    data = []
    
    for i in insurances:
        customer_name = i.customer.cus_name if i.customer else 'Unknown'
        data.append([
            i.ins_num,
            customer_name,
            i.ins_type,
            f"₹{float(i.ins_amt):.2f}",
            i.ins_date.strftime('%Y-%m-%d'),
            i.expiry_date.strftime('%Y-%m-%d') if i.expiry_date else '-',
            i.ins_status
        ])
        
    return render_template('report/view_report.html', 
                          title='Insurance Policy Report',
                          headers=headers,
                          data=data)

@report_bp.route('/financial')
@login_required
def financial():
    """Financial report (Payments)"""
    payments = Payment.query.order_by(Payment.pay_date.desc()).all()
    
    headers = ['Receipt #', 'Date', 'Customer', 'Type', 'Amount', 'Method', 'Reference']
    data = []
    
    for p in payments:
        customer_name = p.customer.cus_name if p.customer else 'Unknown'
        data.append([
            f"#{p.pay_id:04d}",
            p.pay_date.strftime('%Y-%m-%d'),
            customer_name,
            p.pay_type,
            f"₹{float(p.pay_amount):.2f}",
            p.payment_method or '-',
            p.transaction_ref or '-'
        ])
        
    return render_template('report/view_report.html', 
                          title='Financial Report (Payments)',
                          headers=headers,
                          data=data)
