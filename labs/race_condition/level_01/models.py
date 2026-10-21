from .database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, Text, ForeignKey, CheckConstraint
from datetime import datetime, timezone

class Coffee(db.Model):
    __tablename__ = "coffees"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    is_hidden: Mapped[bool] = mapped_column(default=False)
    category: Mapped[str | None] = mapped_column(String(50))
    
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    
    def __repr__(self) -> str:
        return f"<Coffee {self.name!r}>"

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str | None] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user", server_default="user", index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    basket: Mapped["Basket | None"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

class Session(db.Model):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    session_token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

class Basket(db.Model):
    __tablename__ = "baskets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True, index=True)
    coupon_code: Mapped[str | None] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship(back_populates="basket")
    items: Mapped[list["BasketItem"]] = relationship(back_populates="basket", cascade="all, delete-orphan")

    @property
    def subtotal_amount(self) -> float:
        return sum(item.subtotal for item in self.items)

    @property
    def discount(self) -> float:
        if not self.coupon_code:
            return 0.0
        coupon = db.session.execute(
            db.select(Coupon).where(Coupon.code == self.coupon_code, Coupon.active.is_(True))
        ).scalar_one_or_none()
        if coupon is None:
            return 0.0
        return round(self.subtotal_amount * (float(coupon.percent) / 100.0), 2)

    @property
    def total(self) -> float:
        return max(0.0, round(self.subtotal_amount - self.discount, 2))


class BasketItem(db.Model):
    __tablename__ = "basket_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_basket_items_quantity_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    basket_id: Mapped[int] = mapped_column(ForeignKey("baskets.id"), nullable=False, index=True)
    coffee_id: Mapped[int] = mapped_column(ForeignKey("coffees.id"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    basket: Mapped["Basket"] = relationship(back_populates="items")
    coffee: Mapped["Coffee"] = relationship()

    @property
    def subtotal(self) -> float:
        return float(self.coffee.price or 0) * self.quantity

    def __repr__(self) -> str:
        return f"<BasketItem coffee_id={self.coffee_id!r} qty={self.quantity}>"

class Coupon(db.Model):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    percent: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Coupon {self.code!r} {self.percent}%>"