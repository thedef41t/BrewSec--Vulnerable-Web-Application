from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .database import db
from sqlalchemy import text
from .models import User

csrf_bp = Blueprint("csrf", __name__)

@csrf_bp.route('/')
def index():
    return redirect(url_for('csrf.login'))

@csrf_bp.route('/')
@csrf_bp.route('/home')
def home():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "error")
        return redirect(url_for('csrf.login'))

    target_id = request.args.get('id', type=int, default=user_id)
    if target_id != user_id:
        flash("You are not authorized to view this content.", "error")
        return redirect(url_for('csrf.home'))

    target_user = db.session.get(User, target_id)

    return render_template("content.html", target_user=target_user)

@csrf_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            flash("Logged in successfully!", "success")
            return redirect(url_for('csrf.home'))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for('csrf.login'))

    return render_template("form.html")

@csrf_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "warning")
    return redirect(url_for('csrf.login'))

@csrf_bp.route('/update_password', methods=['GET', 'POST'])
def update_password():
    username = session.get('username')
    if not username:
        flash("Unauthorized", "error"), 400

    if request.method == "POST":
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('csrf.update_password'))

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('csrf.login'))

        user.password = new_password

        db.session.commit()

        logout()

        flash("Password successfully updated!", "success")
        return redirect(url_for('csrf.home'))
    
    return render_template('update_password.html')