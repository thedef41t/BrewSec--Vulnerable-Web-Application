from flask import Blueprint, render_template, request
from .database import db
from sqlalchemy import text

sqli_bp = Blueprint("sqli", __name__)

@sqli_bp.route('/', methods=["GET", "POST"])
def home():
    return render_template("content.html")