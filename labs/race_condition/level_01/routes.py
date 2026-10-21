from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .database import db
from .models import User, Basket, BasketItem, Coffee, Coupon
from .session import SessionManager
from sqlalchemy import text
from sqlalchemy.sql import func

race_condition_bp = Blueprint("race_condition", __name__)

@race_condition_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('race_condition.home'))
    return redirect(url_for('race_condition.login'))

@race_condition_bp.route('/basket/add/<int:coffee_id>', methods=['POST'])
def add_to_basket(coffee_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "error")
        return redirect(url_for('race_condition.login'))

    coffee = db.session.get(Coffee, coffee_id)
    if not coffee or coffee.is_hidden:
        flash("That brew isn't available.", "error")
        return redirect(url_for('race_condition.home'))

    basket = db.session.execute(
        db.select(Basket).where(Basket.user_id == user_id)
    ).scalar_one_or_none()
    if basket is None:
        basket = Basket(user_id=user_id)
        db.session.add(basket)
        db.session.flush()

    item = db.session.execute(
        db.select(BasketItem).where(
            BasketItem.basket_id == basket.id,
            BasketItem.coffee_id == coffee.id,
        )
    ).scalar_one_or_none()
    if item:
        item.quantity += 1
    else:
        db.session.add(BasketItem(basket_id=basket.id, coffee_id=coffee.id, quantity=1))

    db.session.commit()
    flash(f"Added {coffee.name} to your basket.", "success")
    return redirect(url_for('race_condition.home'))

@race_condition_bp.route('/basket')
def basket():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "error")
        return redirect(url_for('race_condition.login'))

    user_basket = db.session.execute(
        db.select(Basket).where(Basket.user_id == user_id)
    ).scalar_one_or_none()

    return render_template(
        "basket.html",
        basket=user_basket,
        target_user=db.session.get(User, user_id),
    )

@race_condition_bp.route('/home')
def home():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "error")
        return redirect(url_for('race_condition.login'))

    target_id = request.args.get('id', type=int, default=user_id)
    if target_id != user_id:
        flash("You are not authorized to view this content.", "error")
        return redirect(url_for('race_condition.home'))

    target_user = db.session.get(User, target_id)

    category = request.args.get("category", "all")
    coffees = []
    try:
        if category == "all":
            query = text("SELECT * FROM coffees")
            coffees = db.session.execute(query).fetchall()
        else:
            query = text(f"SELECT * FROM coffees WHERE category = '{category}'")
            coffees = db.session.execute(query).fetchall()
    except Exception as error:
        print(f"Server error: {error}")

    basket = None
    if target_user:
        basket = db.session.execute(
            db.select(Basket).where(Basket.user_id == target_user.id)
        ).scalar_one_or_none()

    return render_template(
        "content.html",
        coffees=coffees,
        selected_category=category,
        target_user=target_user,
        basket=basket,
    )

@race_condition_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            SessionManager._create_session(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('race_condition.home'))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for('race_condition.login'))

    return render_template("form.html")

@race_condition_bp.route('/logout')
def logout():
    SessionManager._clear_session()
    flash("You have been logged out.", "warning")
    return redirect(url_for("race_condition.login"))

@race_condition_bp.route('/basket/coupon', methods=['POST'])
def apply_coupon():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "error")
        return redirect(url_for('race_condition.login'))

    code = (request.form.get('code') or '').strip().upper()
    if not code:
        flash("Enter a coupon code.", "error")
        return redirect(url_for('race_condition.home'))

    user_basket = db.session.execute(
        db.select(Basket).where(Basket.user_id == user_id)
    ).scalar_one_or_none()
    if not user_basket or not user_basket.items:
        flash("Add something to your basket first.", "error")
        return redirect(url_for('race_condition.home'))

    coupon = db.session.execute(
        db.select(Coupon).where(
            func.upper(Coupon.code) == code.upper(),
            Coupon.active.is_(True),
        )
    ).scalar_one_or_none()

    if coupon is None:
        flash("Invalid or expired coupon.", "error")
        return redirect(url_for('race_condition.home'))

    user_basket.coupon_code = coupon.code
    db.session.commit()
    flash(f"Coupon {coupon.code} applied ({coupon.percent}% off).", "success")
    return redirect(url_for('race_condition.home'))

@race_condition_bp.route('/basket/coupon/remove', methods=['POST'])
def remove_coupon():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "error")
        return redirect(url_for('race_condition.login'))

    user_basket = db.session.execute(
        db.select(Basket).where(Basket.user_id == user_id)
    ).scalar_one_or_none()

    if user_basket and user_basket.coupon_code:
        user_basket.coupon_code = None
        db.session.commit()
        flash("Coupon removed.", "warning")
    else:
        flash(f"No coupon to remove (basket={'yes' if user_basket else 'no'}).", "error")

    return redirect(url_for('race_condition.home'))