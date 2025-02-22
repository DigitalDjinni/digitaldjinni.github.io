from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_user, logout_user, login_required
from app.models import User  
from app.forms import LoginForm, RegisterForm
from app import db, bcrypt  

# Blueprint for authentication routes
auth_blueprint = Blueprint('auth_blueprint', __name__)

# Login Route
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    # Flask-WTF validation checks before processing
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Checks if user exists and password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            remember = form.remember.data  # Remember Me checkbox info
            login_user(user, remember=remember)  # Flask-Login authentication

            # Sets a cookie if Remember Me is checked
            response = make_response(redirect(url_for('trip_blueprint.list_trips')))
            if remember:
                response.set_cookie('remember_token', 'true', max_age=30*24*60*60) # allowing the cookie to expire in 30 days
            else:
                response.set_cookie('remember_token', '', expires=0) 

            flash('Login successful!', 'success')
            return response 

        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)

# Logout Route
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()  
    flash('You have successfully logged out.', 'info')  

    # Delete remember me cookie when user logs out
    response = make_response(redirect(url_for('auth_blueprint.login')))
    response.set_cookie('remember_token', '', expires=0)  
    return response

# Registration Route
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  

    # Validating with Flask-WTF
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Checks if the email already exists. If so tells the user to login
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('auth_blueprint.login'))

        # Hashes the users password before storing in the database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')  
            return redirect(url_for('auth_blueprint.login'))

        except Exception as e:
            db.session.rollback()  
            flash('An error occurred during registration. Please try again.', 'danger')

    return render_template('register.html', form=form)
