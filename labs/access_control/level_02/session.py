from flask import session, flash, redirect, url_for
from .database import db
from functools import wraps
import json
import base64
from .models import Session as DBSession
from datetime import datetime, timedelta

class SessionManager:

    @staticmethod
    def _create_session(user):
        payload = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "exp": (datetime.utcnow() + timedelta(minutes=5)).isoformat()
        }

        token = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()

        session['session_token'] = token
        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email
        session['role'] = user.role

        db_session = DBSession(user_id=user.id, session_token=token)
        db.session.add(db_session)
        db.session.commit()

    @staticmethod
    def _get_current_user(self):
        user_id = session.get('user_id')
        if user_id:
            current_user = json.dumps({
                "user_id": session.get('user_id'),
                "username": session.get('username'),
                "email": session.get('email'),
                "role": session.get('role')
            })
        return current_user

    @staticmethod
    def _clear_session():
        token = session.get('session_token')
        if token:
            DBSession.query.filter_by(session_token=token).delete()
            db.session.commit()
        session.clear()

    @staticmethod
    def _admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('role') != 'admin':
                flash("You do not have permission to access this page.", "error")
                return redirect(url_for('access_control.home'))
            return f(*args, **kwargs)
        return decorated_function