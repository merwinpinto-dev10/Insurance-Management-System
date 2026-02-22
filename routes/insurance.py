from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models.insurance import Insurance
from models.customer import Customer
from datetime import datetime

insurance_bp = Blueprint('insurance', __name__, url_prefix='/insurance')

@insurance_bp.route('/')
@login_required
def index():
    """List all insurance policies with search and filter"""
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', 'all')
    
    query = Insurance.query
    
    if search_query:
        query = query.join(Customer).filter(
            db.or_(
                Insurance.ins_num.like(f'%{search_query}%'),
                Insurance.ins_type.like(f'%{search_query}%'),
                Customer.cus_name.like(f'%{search_query}%')
            )
        )
    
    if status_filter != 'all':
        query = query.filter(Insurance.ins_status == status_filter)
        
    insurances = query.order_by(Insurance.created_at.desc()).all()
    return render_template('insurance/list.html', 
                          insurances=insurances, 
                          search_query=search_query, 
                          status_filter=status_filter)

@insurance_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new insurance policy"""
    if request.method == 'POST':
        try:
            ins_cus_id = request.form.get('ins_cus_id')
            ins_type = request.form.get('ins_type')
            ins_num = request.form.get('ins_num')
            ins_amt = request.form.get('ins_amt')
            ins_date_str = request.form.get('ins_date')
            expiry_date_str = request.form.get('expiry_date')
            
            # Validation
            if not all([ins_cus_id, ins_type, ins_num, ins_amt, ins_date_str]):
                flash('Please fill in all required fields.', 'danger')
                return redirect(url_for('insurance.add'))
            
            # Convert dates
            ins_date = datetime.strptime(ins_date_str, '%Y-%m-%d').date()
            expiry_date = None
            if expiry_date_str:
                expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
            
            # Check for duplicate policy number
            existing_ins = Insurance.query.filter_by(ins_num=ins_num).first()
            if existing_ins:
                flash(f'Policy number {ins_num} already exists.', 'danger')
                return redirect(url_for('insurance.add'))
            
            # Create insurance
            new_insurance = Insurance(
                ins_cus_id=ins_cus_id,
                ins_type=ins_type,
                ins_num=ins_num,
                ins_date=ins_date,
                ins_amt=ins_amt,
                expiry_date=expiry_date
            )
            
            db.session.add(new_insurance)
            db.session.commit()
            
            flash('Insurance policy added successfully!', 'success')
            return redirect(url_for('insurance.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding insurance: {str(e)}', 'danger')
            return redirect(url_for('insurance.add'))
    
    customers = Customer.query.filter_by(is_active=True).order_by(Customer.cus_name).all()
    return render_template('insurance/add.html', customers=customers)

@insurance_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit insurance policy"""
    insurance = Insurance.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            insurance.ins_cus_id = request.form.get('ins_cus_id')
            insurance.ins_type = request.form.get('ins_type')
            insurance.ins_num = request.form.get('ins_num')
            insurance.ins_amt = request.form.get('ins_amt')
            insurance.ins_status = request.form.get('ins_status')
            
            ins_date_str = request.form.get('ins_date')
            if ins_date_str:
                insurance.ins_date = datetime.strptime(ins_date_str, '%Y-%m-%d').date()
                
            expiry_date_str = request.form.get('expiry_date')
            if expiry_date_str:
                insurance.expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
            else:
                insurance.expiry_date = None
                
            # Check uniqueness of policy number if changed
            existing_ins = Insurance.query.filter(Insurance.ins_num == insurance.ins_num, Insurance.ins_id != id).first()
            if existing_ins:
                flash(f'Policy number {insurance.ins_num} is already used by another policy.', 'danger')
                return redirect(url_for('insurance.edit', id=id))

            insurance.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Insurance policy updated successfully!', 'success')
            return redirect(url_for('insurance.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating insurance: {str(e)}', 'danger')
            return redirect(url_for('insurance.edit', id=id))
            
    customers = Customer.query.filter_by(is_active=True).order_by(Customer.cus_name).all()
    return render_template('insurance/edit.html', insurance=insurance, customers=customers)

@insurance_bp.route('/view/<int:id>')
@login_required
def view(id):
    """View insurance details"""
    insurance = Insurance.query.get_or_404(id)
    return render_template('insurance/view.html', insurance=insurance)

@insurance_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Delete insurance policy"""
    try:
        insurance = Insurance.query.get_or_404(id)
        db.session.delete(insurance)
        db.session.commit()
        flash('Insurance policy deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting insurance: {str(e)}', 'danger')
    
    return redirect(url_for('insurance.index'))
