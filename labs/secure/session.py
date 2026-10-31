from flask import session, flash, redirect, url_for, g
from .database import db
from functools import wraps
from .models import User
from .models import Session as DBSession
from datetime import datetime, timedelta, timezone
import secrets

class SessionManager:

    @staticmethod
    def _create_session(user):
        
        token = secrets.token_urlsafe(32)

        session['session_token'] = token
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role

        expire_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=60)

        db_session = DBSession(
            user_id=user.id,
            session_token=token,
            expire_at=expire_at
        )
        db.session.add(db_session)
        db.session.commit()

    @staticmethod
    def _get_current_user():
        token = session.get('session_token')
        
        if not token:
            return None

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        db_session = DBSession.query.filter_by(session_token=token).first()

        if not db_session or db_session.expire_at < now:
            SessionManager._clear_session()
            return None

        return User.query.get(db_session.user_id)

    @staticmethod
    def _clear_session():
        token = session.get('session_token')
        if token:
            DBSession.query.filter_by(session_token=token).delete()
            db.session.commit()
        session.clear()

    @staticmethod
    def _login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = SessionManager._get_current_user()
            if not user:
                flash("Please log in to access this page.", "error")
                return redirect(url_for("secure.login"))
            g.user = user
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def _admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('role') != 'admin':
                flash("You do not have permission to access this page.", "error")
                return redirect(url_for('secure.home'))
            return f(*args, **kwargs)
        return decorated_function