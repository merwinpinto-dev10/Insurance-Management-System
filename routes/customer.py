from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.customer import Customer
from datetime import datetime

# Create blueprint
customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

# ==================== LIST ALL CUSTOMERS ====================
@customer_bp.route('/')
@customer_bp.route('/list')
@login_required
def index():
    """Display list of all customers"""
    
    # Get search query if any
    search_query = request.args.get('search', '').strip()
    
    # Build query
    if search_query:
        # Search by name, mobile, or email
        customers = Customer.query.filter(
            db.or_(
                Customer.cus_name.like(f'%{search_query}%'),
                Customer.cus_mobile.like(f'%{search_query}%'),
                Customer.cus_email.like(f'%{search_query}%')
            )
        ).order_by(Customer.created_at.desc()).all()
    else:
        # Get all customers
        customers = Customer.query.order_by(Customer.created_at.desc()).all()
    
    return render_template('customer/list.html', 
                         customers=customers, 
                         search_query=search_query)


# ==================== ADD NEW CUSTOMER ====================
@customer_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new customer"""
    
    if request.method == 'POST':
        # Get form data
        cus_name = request.form.get('cus_name', '').strip()
        cus_mobile = request.form.get('cus_mobile', '').strip()
        cus_email = request.form.get('cus_email', '').strip()
        cus_add = request.form.get('cus_add', '').strip()
        
        # Validation
        errors = []
        
        if not cus_name:
            errors.append('Customer name is required')
        
        if not cus_mobile:
            errors.append('Mobile number is required')
        elif len(cus_mobile) != 10 or not cus_mobile.isdigit():
            errors.append('Mobile number must be 10 digits')
        
        if cus_email:
            # Check if email already exists
            existing = Customer.query.filter_by(cus_email=cus_email).first()
            if existing:
                errors.append('Email already exists')
            # Basic email validation
            if '@' not in cus_email or '.' not in cus_email:
                errors.append('Invalid email format')
        
        # If validation fails
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('customer/add.html',
                                 cus_name=cus_name,
                                 cus_mobile=cus_mobile,
                                 cus_email=cus_email,
                                 cus_add=cus_add)
        
        try:
            # Create new customer
            new_customer = Customer(
                cus_name=cus_name,
                cus_mobile=cus_mobile,
                cus_email=cus_email if cus_email else None,
                cus_add=cus_add if cus_add else None,
                created_by=current_user.user.user_id if current_user.user else None
            )
            
            # Save to database
            db.session.add(new_customer)
            db.session.commit()
            
            flash(f'Customer "{cus_name}" added successfully!', 'success')
            return redirect(url_for('customer.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding customer: {str(e)}', 'danger')
            return render_template('customer/add.html',
                                 cus_name=cus_name,
                                 cus_mobile=cus_mobile,
                                 cus_email=cus_email,
                                 cus_add=cus_add)
    
    # GET request - show form
    return render_template('customer/add.html')


# ==================== EDIT CUSTOMER ====================
@customer_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit existing customer"""
    
    # Get customer by ID
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        # Get form data
        cus_name = request.form.get('cus_name', '').strip()
        cus_mobile = request.form.get('cus_mobile', '').strip()
        cus_email = request.form.get('cus_email', '').strip()
        cus_add = request.form.get('cus_add', '').strip()
        is_active = request.form.get('is_active') == 'on'
        
        # Validation
        errors = []
        
        if not cus_name:
            errors.append('Customer name is required')
        
        if not cus_mobile:
            errors.append('Mobile number is required')
        elif len(cus_mobile) != 10 or not cus_mobile.isdigit():
            errors.append('Mobile number must be 10 digits')
        
        if cus_email:
            # Check if email exists for another customer
            existing = Customer.query.filter(
                Customer.cus_email == cus_email,
                Customer.cus_id != id
            ).first()
            if existing:
                errors.append('Email already exists')
            if '@' not in cus_email or '.' not in cus_email:
                errors.append('Invalid email format')
        
        # If validation fails
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('customer/edit.html', customer=customer)
        
        try:
            # Update customer
            customer.cus_name = cus_name
            customer.cus_mobile = cus_mobile
            customer.cus_email = cus_email if cus_email else None
            customer.cus_add = cus_add if cus_add else None
            customer.is_active = is_active
            customer.updated_at = datetime.utcnow()
            
            # Save to database
            db.session.commit()
            
            flash(f'Customer "{cus_name}" updated successfully!', 'success')
            return redirect(url_for('customer.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating customer: {str(e)}', 'danger')
            return render_template('customer/edit.html', customer=customer)
    
    # GET request - show form with existing data
    return render_template('customer/edit.html', customer=customer)


# ==================== VIEW CUSTOMER DETAILS ====================
@customer_bp.route('/view/<int:id>')
@login_required
def view(id):
    """View customer details with related records"""
    
    customer = Customer.query.get_or_404(id)
    
    # Get related records
    insurances = customer.insurances
    bills = customer.bills
    payments = customer.payments
    
    # Calculate statistics
    total_insurance_amt = sum([float(ins.ins_amt) for ins in insurances if ins.ins_status == 'Active'])
    total_bill_amt = sum([float(bill.bill_amount) for bill in bills])
    pending_bills = [bill for bill in bills if bill.bill_status == 'Pending']
    total_payment_amt = sum([float(pay.pay_amount) for pay in payments])
    
    return render_template('customer/view.html',
                         customer=customer,
                         insurances=insurances,
                         bills=bills,
                         payments=payments,
                         total_insurance_amt=total_insurance_amt,
                         total_bill_amt=total_bill_amt,
                         pending_bills=pending_bills,
                         total_payment_amt=total_payment_amt)


# ==================== DELETE CUSTOMER ====================
@customer_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Delete customer"""
    
    customer = Customer.query.get_or_404(id)
    customer_name = customer.cus_name
    
    try:
        # Check if customer has related records
        if customer.insurances or customer.bills or customer.payments:
            flash(f'Cannot delete customer "{customer_name}" as they have related records. Deactivate instead.', 'warning')
            return redirect(url_for('customer.index'))
        
        # Delete customer
        db.session.delete(customer)
        db.session.commit()
        
        flash(f'Customer "{customer_name}" deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting customer: {str(e)}', 'danger')
    
    return redirect(url_for('customer.index'))


# ==================== TOGGLE ACTIVE STATUS ====================
@customer_bp.route('/toggle-status/<int:id>', methods=['POST'])
@login_required
def toggle_status(id):
    """Activate or deactivate customer"""
    
    customer = Customer.query.get_or_404(id)
    
    try:
        if customer.is_active:
            customer.deactivate()
            flash(f'Customer "{customer.cus_name}" deactivated!', 'info')
        else:
            customer.activate()
            flash(f'Customer "{customer.cus_name}" activated!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error changing status: {str(e)}', 'danger')
    
    return redirect(url_for('customer.index'))
