from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .database import db
from sqlalchemy import text
from .models import User
from .session import SessionManager

access_control_bp = Blueprint("access_control", __name__)

# ---------------------------------------------------------------------
@access_control_bp.route('/')
def index():
    return redirect(url_for('access_control.login'))
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@access_control_bp.route('/home')
def home():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "error")
        return redirect(url_for('access_control.login'))

    target_id = request.args.get('id', type=int, default=user_id)
    if target_id != user_id:
        flash("You are not authorized to view this content.", "error")
        return redirect(url_for('access_control.home'))

    target_user = db.session.get(User, target_id)

    return render_template("content.html", target_user=target_user)
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@access_control_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            SessionManager._create_session(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('access_control.home'))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for('access_control.login'))

    return render_template("form.html")
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@access_control_bp.route('/admin', methods=['GET', 'POST'])
@SessionManager._admin_required
def admin():
    return render_template("admin.html")
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@access_control_bp.route('/logout')
def logout():
    SessionManager._clear_session()
    flash("You have been logged out.", "warning")
    return redirect(url_for('access_control.login'))
# ---------------------------------------------------------------------
