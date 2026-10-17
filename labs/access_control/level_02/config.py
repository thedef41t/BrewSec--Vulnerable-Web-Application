import os

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "JY7d4ZQ5p4aQ5LotwJVRorBDEiK2m6MptM1Ffb"
    )
    
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_DB")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LAB_NAME = "Access Control - Level 02"
    LAB_DIFFICULTY = "Practitioner"
    LAB_CATEGORY = "Access Control"

    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False 