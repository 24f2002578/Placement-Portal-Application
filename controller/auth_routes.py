from main import app
from flask import render_template, request, session, flash, redirect,url_for
from controller.models import *

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        if 'user_email' in session:
            #revisit this part later
            return redirect(url_for('home')) 
        return render_template('login.html') 
    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        #Data validation
        if not email or not password:
            flash('Please enter both email and password')
            return render_template('login.html')
        
        if'@' not in email:
            flash('Please enter a valid email address')
            return render_template('login.html')
        
        
        user = User.query.filter_by(user_email=email).first()
        if not user:
            flash('User does not exist')
            return render_template('login.html') 
        
        if user.password != password:
            flash('Incorrect password')
            return render_template('login.html')

        if user.is_approved==False and user.user_Role != 'student':
            flash('Approval is pending')
            return render_template('login.html')
        
        session['user_id'] = user.user_id
        session['user_email'] = user.user_email
        session['user_role'] = [role.name for role in user.roles]
        flash('You are successfully logged in')
        #redirect to home page
        return redirect(url_for('home'))
    
@app.route('/logout')
def logout():
    if 'user_email' not in session:
        flash("You are not logged in")
        return redirect(url_for('login'))

    session.pop('user_email')
    session.pop('user_role')

    flash('You are successfully logged out')
    return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        ## Check if user is login already then redirect to dashboard
        return render_template('register.html')
        

    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get("password", None)
        confirm_password = request.form.get('confirm-password', None)
        role = request.form.get('role', None)
        user_name = request.form.get('fullname', None)

            # Data validation
        if not email or not password   or not user_name or not role or not confirm_password:
                flash('Please fill in all fields')
                return render_template('register.html')

        if password != confirm_password:
                flash('Passwords do not match')
                return render_template('register.html') 

        if role == 'student':
            is_approved=True
        else:
            is_approved=False
        
        if len(password) < 8:
                flash('Password should be at least 8 characters long')
                return render_template('register.html')
        

        if '@' not in email:
                flash('Please enter a valid email address')
                return render_template('register.html')

            # Check if user already exists
        existing_user = User.query.filter_by(user_email=email).first()
        if existing_user:
                flash('User with this email already exists')
                return render_template('register.html')

        user = User.query.filter_by(user_email=email).first()
        if user:
                flash('User already exists, please log in')
                return render_template('register.html')
            
        role_obj = Role.query.filter_by(name=role).first()
        if not role_obj:
                flash('Selected role does not exist')
                return render_template('register.html')
        
        # Create new user
        new_user = User(user_email=email, password=password, user_name=user_name, user_Role=role, is_approved=is_approved)
        db.session.add(new_user)
        db.session.flush()  # Get the user_id without committing
        
        user_role = UserRole(user_id=new_user.user_id, role_id=role_obj.id)
        db.session.add(user_role)
        db.session.commit()

        flash('You are successfully registered')
        return redirect(url_for('login'))



