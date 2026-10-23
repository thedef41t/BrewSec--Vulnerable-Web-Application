from flask import Blueprint, render_template, request, flash, session
from .database import db
from sqlalchemy import text

sqli_bp = Blueprint("sqli", __name__)

# ---------------------------------------------------------------------
@sqli_bp.route('/', methods=["GET", "POST"])
def home():
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method == "POST":
        try:
            query = text(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
            result = db.session.execute(query).first()
            if result:
                session["user_id"] = result.id
                session["username"] = result.username
                flash("Login successful!", "success")
            else:
                flash("Invalid username or password.", "error")
        except Exception as error:
            print(f"Server error: {error}")
    return render_template("content.html")
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@sqli_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return render_template("content.html")
# ---------------------------------------------------------------------
