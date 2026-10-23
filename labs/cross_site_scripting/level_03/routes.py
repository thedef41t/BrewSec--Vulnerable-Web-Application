from flask import Blueprint, render_template, request, redirect, url_for, flash
from .database import db
from .models import Feedback

xss_bp = Blueprint("xss", __name__)

# ---------------------------------------------------------------------
@xss_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        try:
            new_feedback = Feedback(name=name, email=email, subject=subject, message=message)
            db.session.add(new_feedback)
            db.session.commit()
            flash("Your feedback has been submitted successfully!", "success")
            return redirect(url_for('xss.home'))
        except Exception as e:
            print(f"Error saving feedback: {e}")
            db.session.rollback()
            flash("An error occurred while saving your feedback.", "error")
            return redirect(url_for('xss.home'))
        
    feedback = Feedback.query.order_by(Feedback.id.desc()).all()
    return render_template('content.html', feedback=feedback)
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
@xss_bp.route('/feedback')
def feedback():
    feedback = Feedback.query.all()
    return render_template('feedback.html', feedback=feedback)
# ---------------------------------------------------------------------
