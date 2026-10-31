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
    configure_secure_headers(app) 
    
    app.config.from_object(Config)
    
    database_path = instance_dir / "app.db"
    
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{database_path}"
    )
    
    db.init_app(app)
    
    from .routes import secure_bp
    app.register_blueprint(secure_bp)

    with app.app_context():
        db.create_all()
        seed_db()
        
    return app

def configure_secure_headers(app):
    @app.after_request
    def add_headers(response):
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4; "
            "style-src 'self' 'unsafe-inline'; "
        )

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers['Content-Security-Policy'] = csp_policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=()"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        return response