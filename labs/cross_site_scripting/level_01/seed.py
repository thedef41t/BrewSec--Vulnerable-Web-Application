from .models import Coffee
from .database import db
from cli.menu import Colors

def seed_db():
    if Coffee.query.first() is not None:
        return
    
    coffees = [
        {
            "name": "Cappuccino",
            "description": "Classic Italian coffee.",
            "price": 7.99,
            "is_hidden": False
        },
        {
            "name": "Espresso",
            "description": "Strong and concentrated coffee.",
            "price": 4.99,
            "is_hidden": False
        },
        {
            "name": "Hidden Coffee",
            "description": "This product should not normally be visible.",
            "price": 103.99,
            "is_hidden": True
        },
    ]
    
    for coffee in coffees:
        db.session.add(
            Coffee(
                name=coffee["name"],
                description=coffee["description"],
                price=coffee["price"],
                is_hidden=coffee["is_hidden"],
            )
        )
    
    db.session.commit()
    
    print(f"{Colors.CYAN}[+]{Colors.RESET} Level 01 database seeded.")