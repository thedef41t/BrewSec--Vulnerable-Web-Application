from flask import Blueprint, render_template, request, redirect, url_for
from .database import db
from .models import Review
import  re

xss_bp = Blueprint("xss", __name__)

BLOCKED_TAGS = [
                    "script", "iframe", "object",
                    "embed", "link", "style",
                    "meta", "img", "svg",
                    "video", "audio", "source",
                    "track", "canvas", "map",
                    "area", "base", "form",
                    "input", "button"
                ]

TAG_PATTERN = re.compile(
    r"<\s*/?\s*(" + "|".join(re.escape(t) for t in BLOCKED_TAGS) + r")\b[^>]*>",
    re.IGNORECASE,
)

def sanatizer(value: str) -> str:
    if not value:
        return ""
    cleaned = TAG_PATTERN.sub("", value)
    return cleaned[:1000]

@xss_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        author = sanatizer(request.form.get('author'))[:50]
        comment = sanatizer(request.form.get('comment'))
        
        new_review = Review(author=author, comment=comment)
        db.session.add(new_review)
        db.session.commit()
        
        return redirect(url_for('xss.home'))
        
    reviews = Review.query.order_by(Review.id.desc()).all()
    return render_template('content.html', reviews=reviews)