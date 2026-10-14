from flask import Blueprint, render_template, request, flash, session
from .database import db
from sqlalchemy import text

sqli_bp = Blueprint("sqli", __name__)

@sqli_bp.route('/', methods=["GET", "POST"])
def home():
    category = request.args.get("category", "all")
    coffees = []
    try:
        if category == "all":
            query = text("SELECT * FROM coffees")
            coffees = db.session.execute(query).fetchall()
        else:
            query = text(f"SELECT * FROM coffees WHERE category = '{category}'")
            coffees = db.session.execute(query).fetchall()
    except Exception as error:
        print(f"Server error: {error}")
    return render_template("content.html", coffees=coffees, selected_category=category)