import os

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "default_sql_injection_level02"
    )
    
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_DB")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LAB_NAME = "SQL Injection - Level 02"
    LAB_DIFFICULTY = "Apprentice"
    LAB_CATEGORY = "SQL Injection"