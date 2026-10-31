import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
    )
    
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_DB")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LAB_NAME = "Secure"

    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False 