import os

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "access_control_level03_secret_key"
    )
    
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_DB")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LAB_NAME = "Access Control - Level 03"
    LAB_DIFFICULTY = "Practitioner"
    LAB_CATEGORY = "Access Control"

    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False 