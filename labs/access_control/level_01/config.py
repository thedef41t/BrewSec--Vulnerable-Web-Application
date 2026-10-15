import os

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "default_access_control_level01"
    )
    
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_DB")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LAB_NAME = "Access Control - Level 01"
    LAB_DIFFICULTY = "Apprentice"
    LAB_CATEGORY = "Access Control"

    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False 