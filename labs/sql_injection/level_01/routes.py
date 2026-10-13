from flask import Blueprint, render_template, request
from .database import db
from sqlalchemy import text

sqli_bp = Blueprint("sqli", __name__)

@sqli_bp.route('/')
def home():
    q = request.args.get("q", "")
    
    query = f"""
        SELECT name, description, price
        FROM coffees
        WHERE name LIKE '%{q}%'
        AND is_hidden = 0
    """
    
    result = db.session.execute(text(query))
    rows = [dict(row) for row in result.mappings().all()]
    
    return render_template("content.html", rows=rows, q=q)