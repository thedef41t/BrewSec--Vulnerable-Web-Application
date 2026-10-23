from flask import Blueprint, render_template, request, redirect, url_for
from .database import db
from .models import Review

xss_bp = Blueprint("xss", __name__)

# ---------------------------------------------------------------------
@xss_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        author = request.form.get('author')
        comment = request.form.get('comment')
        
        new_review = Review(author=author, comment=comment)
        db.session.add(new_review)
        db.session.commit()
        
        return redirect(url_for('xss.home'))
        
    reviews = Review.query.order_by(Review.id.desc()).all()
    return render_template('content.html', reviews=reviews)
# ---------------------------------------------------------------------
