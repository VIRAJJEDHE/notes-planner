from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,current_user,logout_user,login_required

auth = Blueprint('auth',__name__)

@auth.route("/login",methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        email=request.form.get('email')
        password=request.form.get('password')
        
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in Successfully',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again',category='error')
        else:
            flash('Email does not exit',category='error')
    return render_template('login.html', user=current_user)

@auth.route("/signup",methods=['GET','POST'])
def signup():
    if(request.method=='POST'):
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        lastName=request.form.get('lastName')
        password=request.form.get('password')
        confirmPassword=request.form.get('confirmPassword')

        user=User.query.filter_by(email=email).first()
        if user:
            flash('This email already exists',category='error')
        elif len(email)<4:
            flash('Invalid Email Address',category='error')
        elif len(firstName)<2:
            flash('first name should have more than 1 characters',category='error')
        elif len(lastName)<2:
            flash('last name should have more than 1 characters',category='error')
        elif len(password)<7:
            flash('password should have more than 7 characters',category='error')
        elif password!=confirmPassword:
            flash('Passwords do not match',category='error')
        else:
            new_user=User(firstName=firstName,lastName=lastName,email=email,password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created Successfully',category='success')
            login_user(new_user,remember=True)
            return redirect(url_for('views.home'))

    return render_template('signup.html',user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))