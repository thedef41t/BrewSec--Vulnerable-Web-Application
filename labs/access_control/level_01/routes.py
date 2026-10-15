from flask import Blueprint, render_template, request
from .database import db
from sqlalchemy import text

access_control_bp = Blueprint("access_control", __name__)

@access_control_bp.route('/')
def home():
    return render_template("content.html")