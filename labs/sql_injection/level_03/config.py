import os

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "default_sql_injection_level03"
    )
    
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_DB")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LAB_NAME = "SQL Injection - Level 03"
    LAB_DIFFICULTY = "Apprentice"
    LAB_CATEGORY = "SQL Injection"

    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False 