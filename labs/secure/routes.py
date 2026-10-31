from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .database import db
from .models import User, Coffee
from .session import SessionManager
from werkzeug.security import check_password_hash

secure_bp = Blueprint("secure", __name__)

# ---------------------------------------------------------------------
@secure_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('secure.home'))
    return redirect(url_for('secure.login'))
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@secure_bp.route('/home')
@SessionManager._login_required
def home():
    user_id = session.get('user_id')

    target_id = request.args.get('id', type=int, default=user_id)
    if target_id != user_id:
        flash("You are not authorized to view this content.", "error")
        return redirect(url_for('secure.home'))

    target_user = db.session.get(User, target_id)

    return render_template("content.html", target_user=target_user)
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@secure_bp.route('/products')
def products():
    coffees = Coffee.query.all()
    return render_template("coffee.html", coffees=coffees)
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@secure_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            SessionManager._create_session(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('secure.home'))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for('secure.login'))

    return render_template("form.html")
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@secure_bp.route('/profile')
@SessionManager._login_required
def profile():
    user = SessionManager._get_current_user()
    return render_template("user-profile.html", user=user)
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@secure_bp.route('/admin', methods=['GET', 'POST'])
@SessionManager._admin_required
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@secure_bp.route('/admin/update-role/<int:user_id>', methods=['POST'])
@SessionManager._admin_required
def update_role(user_id):
    current_user = session.get("user_id")
    if not current_user:
        flash("Please log in to continue.", "error")
        return redirect(url_for("secure.login"))

    current_user = db.session.get(User, current_user)
    if not current_user or current_user.role != "admin":
        flash("Unauthorized: Admin privileges required.", "error")
        return redirect(url_for("secure.home"))

    new_role = request.form.get("new_role")
    target_user = db.session.get(User, user_id)

    if target_user is None:
        flash("User not found", "error")
        return redirect(url_for("secure.admin"))

    if current_user.id == target_user.id:
        flash("Security restriction: You cannot modify your own privilege level.", "error")
        return redirect(url_for("secure.admin"))

    if target_user.id == 1 and target_user.role == "admin":
        flash("Primary admin role cannot be changed!", "error")
        return redirect(url_for("secure.admin"))

    target_user.role = new_role
    db.session.commit()

    return redirect(url_for("secure.admin"))
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@secure_bp.route('/logout')
def logout():
    SessionManager._clear_session()
    flash("You have been logged out.", "warning")
    return redirect(url_for("secure.login"))
# ---------------------------------------------------------------------
