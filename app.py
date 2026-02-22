from flask import Flask, render_template, redirect, url_for, flash
from extensions import db, login_manager, bcrypt, session
import os

# Extensions are initialized in extensions.py

def create_app(config_name='development'):
    """Application factory pattern"""
    
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    session.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Create upload folder if it doesn't exist
    upload_folder = app.config.get('UPLOAD_FOLDER', 'static/uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    # Register blueprints (routes)
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.customer import customer_bp
    from routes.insurance import insurance_bp
    from routes.bill import bill_bp
    from routes.payment import payment_bp
    from routes.user import user_bp
    from routes.report import report_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(insurance_bp)
    app.register_blueprint(bill_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Context processors (make variables available in all templates)
    @app.context_processor
    def utility_processor():
        from datetime import datetime
        return {
            'app_name': app.config.get('APP_NAME'),
            'app_version': app.config.get('APP_VERSION'),
            'current_year': datetime.now().year
        }
    
    # Shell context for flask shell
    @app.shell_context_processor
    def make_shell_context():
        from models.login import Login
        from models.user import User
        from models.role import Role
        from models.customer import Customer
        from models.insurance import Insurance
        from models.bill import Bill
        from models.payment import Payment
        
        return {
            'db': db,
            'Login': Login,
            'User': User,
            'Role': Role,
            'Customer': Customer,
            'Insurance': Insurance,
            'Bill': Bill,
            'Payment': Payment
        }
    
    return app


# Create app instance
app = create_app(os.getenv('FLASK_ENV', 'development'))


if __name__ == '__main__':
    # Run the application
    print("=" * 50)
    print(f"  {app.config.get('APP_NAME')}")
    print(f"  Version: {app.config.get('APP_VERSION')}")
    print(f"  Environment: {os.getenv('FLASK_ENV', 'development')}")
    print("=" * 50)
    
    app.run(
        host='127.0.0.1',
        port=int(os.environ.get('PORT', 5501)),
        debug=app.config.get('DEBUG', True)
    )
