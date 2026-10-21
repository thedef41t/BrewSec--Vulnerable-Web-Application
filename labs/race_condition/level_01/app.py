from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
from .config import Config
from .database import db
from .seed import seed_db

def create_app():
    lab_dir = Path(__file__).resolve().parent
    instance_dir = lab_dir / "instance"
    
    instance_dir.mkdir(parents=True, exist_ok=True)
    
    load_dotenv(lab_dir / ".env")
    
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    database_path = instance_dir / "app.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{database_path}"
    )
    
    db.init_app(app)
    
    from .routes import race_condition_bp
    app.register_blueprint(race_condition_bp)

    with app.app_context():
        db.create_all()
        seed_db()
        
    return app