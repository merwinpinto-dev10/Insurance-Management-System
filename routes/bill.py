from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models.bill import Bill
from models.customer import Customer
from datetime import datetime

bill_bp = Blueprint('bill', __name__, url_prefix='/bill')

@bill_bp.route('/')
@login_required
def index():
    """List all bills"""
    bills = Bill.query.order_by(Bill.created_at.desc()).all()
    return render_template('bill/list.html', bills=bills)

@bill_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new bill"""
    if request.method == 'POST':
        try:
            bill_cus_id = request.form.get('bill_cus_id')
            bill_num = request.form.get('bill_num')
            bill_amount = request.form.get('bill_amount')
            bill_date_str = request.form.get('bill_date')
            due_date_str = request.form.get('due_date')
            bill_desc = request.form.get('bill_desc') # Note: Description not in model, might need to ignore or add to model if needed. 
            # Checked model: no description field. Ignoring bill_desc.

            # Validation
            if not all([bill_cus_id, bill_num, bill_amount, bill_date_str]):
                flash('Please fill in all required fields.', 'danger')
                return redirect(url_for('bill.add'))

            # Convert dates
            bill_date = datetime.strptime(bill_date_str, '%Y-%m-%d').date()
            due_date = None
            if due_date_str:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

            # Check duplication
            existing_bill = Bill.query.filter_by(bill_num=bill_num).first()
            if existing_bill:
                flash(f'Bill number {bill_num} already exists.', 'danger')
                return redirect(url_for('bill.add'))

            # Create bill
            new_bill = Bill(
                bill_cus_id=bill_cus_id,
                bill_num=bill_num,
                bill_amount=bill_amount,
                bill_date=bill_date,
                due_date=due_date
            )
            
            db.session.add(new_bill)
            db.session.commit()
            
            flash('Bill created successfully!', 'success')
            return redirect(url_for('bill.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating bill: {str(e)}', 'danger')
            return redirect(url_for('bill.add'))
    
    customers = Customer.query.filter_by(is_active=True).order_by(Customer.cus_name).all()
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('bill/add.html', customers=customers, today=today)

@bill_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit bill"""
    bill = Bill.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            bill.bill_cus_id = request.form.get('bill_cus_id')
            bill.bill_num = request.form.get('bill_num')
            bill.bill_amount = request.form.get('bill_amount')
            bill.bill_status = request.form.get('bill_status')
            
            bill_date_str = request.form.get('bill_date')
            if bill_date_str:
                bill.bill_date = datetime.strptime(bill_date_str, '%Y-%m-%d').date()
                
            due_date_str = request.form.get('due_date')
            if due_date_str:
                bill.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            else:
                bill.due_date = None

            # Check duplication
            existing_bill = Bill.query.filter(Bill.bill_num == bill.bill_num, Bill.bill_id != id).first()
            if existing_bill:
                flash(f'Bill number {bill.bill_num} is already used.', 'danger')
                return redirect(url_for('bill.edit', id=id))
            
            bill.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Bill updated successfully!', 'success')
            return redirect(url_for('bill.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating bill: {str(e)}', 'danger')
            return redirect(url_for('bill.edit', id=id))

    customers = Customer.query.filter_by(is_active=True).order_by(Customer.cus_name).all()
    return render_template('bill/edit.html', bill=bill, customers=customers)

@bill_bp.route('/view/<int:id>')
@login_required
def view(id):
    """View bill details"""
    bill = Bill.query.get_or_404(id)
    return render_template('bill/view.html', bill=bill)

@bill_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Delete bill"""
    try:
        bill = Bill.query.get_or_404(id)
        db.session.delete(bill)
        db.session.commit()
        flash('Bill deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting bill: {str(e)}', 'danger')
        
    return redirect(url_for('bill.index'))
