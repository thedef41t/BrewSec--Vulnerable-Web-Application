import os

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "default_cross_site_scripting_level03"
    )
    
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_DB")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LAB_NAME = "Cross Site Scripting - Level 03"
    LAB_DIFFICULTY = "Practitioner"
    LAB_CATEGORY = "Cross Site Scripting"

    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False 