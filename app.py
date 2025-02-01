from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate  # Import Migrate
from models import db, User, Password  # Ensure these are correct imports

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize SQLAlchemy with app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Route to Home page, only accessible if logged in
@app.route('/')
@login_required
def home():
    return render_template('home.html')


# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists!", "danger")
            return redirect(url_for('register'))

        # Hash password
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user and add to DB
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # **New: Add the password entry into the Password table**
        new_password_entry = Password(
            website=website,
            username=username,  # Use the same username
            password=hashed_password,  # Store hashed password
            user_id=new_user.id  # Link to the user
        )
        db.session.add(new_password_entry)
        db.session.commit()  # Save the record in the database

        flash("Account Created! Password saved.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login Successful!", "success")
            next_page = request.args.get('next')  # Redirect to next page after login if available
            return redirect(next_page or url_for('home'))
        else:
            flash("Login Failed. Check your credentials", "danger")

    return render_template('login.html')


# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))


# Dashboard Route - Shows passwords related to the current user
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', passwords=current_user.passwords)


# Ensure database tables are created when app starts
with app.app_context():
    db.create_all()  # Creates all tables based on the models defined

if __name__ == '__main__':
    app.run(debug=True)
