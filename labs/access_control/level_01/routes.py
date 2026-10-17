from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .database import db
from sqlalchemy import text
from .models import User

access_control_bp = Blueprint("access_control", __name__)

@access_control_bp.route('/')
@access_control_bp.route('/home')
def home():
    if not session.get('user_id'):
        flash("Please log in first.", "error")
        return redirect(url_for('access_control.login'))

    if 'id' not in request.args:
        return redirect(url_for('access_control.home', id=session.get('user_id')))

    target_id = request.args.get('id', type=int)
    target_user = User.query.get(target_id)

    return render_template("content.html", target_user=target_user, target_id=target_id)

@access_control_bp.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('access_control.home'))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for('access_control.login'))

    return render_template("form.html")

@access_control_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "warning")
    return redirect(url_for('access_control.login'))