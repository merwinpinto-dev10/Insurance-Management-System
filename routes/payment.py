from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from models.payment import Payment
from models.customer import Customer
from models.bill import Bill
from datetime import datetime

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/')
@login_required
def index():
    """List all payments with search"""
    search_query = request.args.get('search', '')
    
    query = Payment.query
    
    if search_query:
        query = query.join(Customer).filter(
            db.or_(
                Customer.cus_name.like(f'%{search_query}%'),
                Payment.transaction_ref.like(f'%{search_query}%'),
                Payment.pay_type.like(f'%{search_query}%')
            )
        )
        
    payments = query.order_by(Payment.pay_date.desc()).all()
    return render_template('payment/list.html', 
                          payments=payments, 
                          search_query=search_query)

@payment_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Add new payment"""
    if request.method == 'POST':
        try:
            pay_cus_id = request.form.get('pay_cus_id')
            pay_bill_id = request.form.get('pay_bill_id')
            pay_type = request.form.get('pay_type')
            pay_amount = request.form.get('pay_amount')
            pay_date_str = request.form.get('pay_date')
            payment_method = request.form.get('payment_method')
            transaction_ref = request.form.get('transaction_ref')
            pay_desc = request.form.get('pay_desc')

            # Validation
            if not all([pay_cus_id, pay_type, pay_amount, pay_date_str]):
                flash('Please fill in all required fields.', 'danger')
                return redirect(url_for('payment.add'))

            # Convert dates
            pay_date = datetime.strptime(pay_date_str, '%Y-%m-%d').date()
            
            # Handle Bill ID (empty string check)
            if pay_bill_id and pay_bill_id.strip():
                pay_bill_id = int(pay_bill_id)
            else:
                pay_bill_id = None

            # Create payment
            new_payment = Payment(
                pay_cus_id=pay_cus_id,
                pay_bill_id=pay_bill_id,
                pay_type=pay_type,
                pay_date=pay_date,
                pay_amount=pay_amount,
                pay_desc=pay_desc,
                payment_method=payment_method,
                transaction_ref=transaction_ref
            )
            
            db.session.add(new_payment)
            
            # Update Bill Status if linked
            if pay_bill_id:
                bill = Bill.query.get(pay_bill_id)
                if bill:
                    # Commit payload first to include this payment in calculations
                    db.session.commit() 
                    
                    # Calculate total paid including this new payment
                    total_paid = bill.get_paid_amount()
                    
                    if total_paid >= float(bill.bill_amount):
                        bill.bill_status = 'Paid'
                    # Optional: Add 'Partial' status if needed, but keeping it simple for now
                    
                    db.session.add(bill) # Add back to session to update status
                    db.session.commit()
                else:
                    db.session.commit() # Commit payment even if bill check fails (shouldn't happen)
            else:
                db.session.commit()
            
            flash('Payment recorded successfully!', 'success')
            return redirect(url_for('payment.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error recording payment: {str(e)}', 'danger')
            return redirect(url_for('payment.add'))
    
    customers = Customer.query.filter_by(is_active=True).order_by(Customer.cus_name).all()
    # Only show pending/overdue bills for linking
    bills = Bill.query.filter(Bill.bill_status.in_(['Pending', 'Overdue'])).order_by(Bill.bill_date.desc()).all()
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('payment/add.html', customers=customers, bills=bills, today=today)

@payment_bp.route('/view/<int:id>')
@login_required
def view(id):
    """View payment receipt"""
    payment = Payment.query.get_or_404(id)
    return render_template('payment/view.html', payment=payment)

@payment_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Delete payment"""
    try:
        payment = Payment.query.get_or_404(id)
        
        # If linked to a bill, we might need to revert bill status
        # This is complex, for now just delete and let user manually fix bill if needed
        # Or simpler: re-check balance after delete
        
        bill_id = payment.pay_bill_id
        
        db.session.delete(payment)
        db.session.commit()
        
        # Re-check bill status if linked
        if bill_id:
            bill = Bill.query.get(bill_id)
            if bill:
                total_paid = bill.get_paid_amount()
                if total_paid < float(bill.bill_amount):
                    bill.bill_status = 'Pending' # Revert to Pending if not fully paid
                    # Or 'Overdue' if date passed? logic can be complex. simpler is 'Pending'
                db.session.commit()
        
        flash('Payment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting payment: {str(e)}', 'danger')
        
    return redirect(url_for('payment.index'))
