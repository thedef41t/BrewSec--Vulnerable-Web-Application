from .models import Coffee, User
from .database import db
from cli.menu import Colors

def seed_db():
    if Coffee.query.first() is not None:
        return
    
    if User.query.first() is not None:
        return
    
    coffees = [
        {
            "name": "Cappuccino",
            "description": "Classic Italian coffee.",
            "price": 7.99,
            "is_hidden": False,
            "category": "classic"
        },
        {
            "name": "Espresso",
            "description": "Strong and concentrated coffee.",
            "price": 4.99,
            "is_hidden": False,
            "category": "classic"
        },
        {
            "name": "Hidden Coffee",
            "description": "This product should not normally be visible.",
            "price": 103.99,
            "is_hidden": True,
            "category": "special"
        },
    ]
    
    users = [
        {
            "username": "administrator",
            "email": "admin@brewsec.local",
            "password": "SecurePass123",
            "role": "admin",
        },
        {
            "username": "carlos",
            "email": "carlos@brewsec.local",
            "password": "CarlosS3c123",
            "role": "user",
        },
        {
            "username": "wiener",
            "email": "wiener@brewsec.local",
            "password": "SecWiener123",
            "role": "user",
        },
    ]
    
    for coffee in coffees:
        db.session.add(
            Coffee(
                name=coffee["name"],
                description=coffee["description"],
                price=coffee["price"],
                is_hidden=coffee["is_hidden"],
                category=coffee["category"]
            )
        )
    
    db.session.commit()
    
    for user in users:
        db.session.add(
            User(
                username=user["username"],
                email=user["email"],
                role=user["role"],
                password=user["password"]
            )
        )
    
    db.session.commit()
    
    print(f"{Colors.CYAN}[+]{Colors.RESET} Level 01 database seeded.")