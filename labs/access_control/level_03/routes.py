from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .database import db
from .models import User
from .session import SessionManager

access_control_bp = Blueprint("access_control", __name__)

# ---------------------------------------------------------------------
@access_control_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('access_control.home'))
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
    users = User.query.all()
    return render_template("admin.html", users=users)
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@access_control_bp.route('/admin/update-role/<int:user_id>', methods=['POST'])
@SessionManager._admin_required
def update_role(user_id):
    referer = request.headers.get("Referer", "")
    if referer.startswith(request.host_url + "admin"):
        new_role = request.form.get("new_role")
        user = db.session.get(User, user_id)
        if user:
            user.role = new_role
            db.session.commit()
            flash(f"Updated role for {user.username} to {new_role}.", "success")
        else:
            flash("User not found.", "error")
    else:
        flash(f"Invalid request source.", "error")

    return redirect(url_for("access_control.admin"))
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@access_control_bp.route('/logout')
def logout():
    SessionManager._clear_session()
    flash("You have been logged out.", "warning")
    return redirect(url_for("access_control.login"))
# ---------------------------------------------------------------------
