from .database import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, Text
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