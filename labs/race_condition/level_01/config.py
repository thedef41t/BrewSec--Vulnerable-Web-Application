import os

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "race_condition_level01_secret_key"
    )
    
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_DB")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LAB_NAME = "Race Condition - Level 01"
    LAB_DIFFICULTY = "Apprentice"
    LAB_CATEGORY = "Race Condition"

    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False 