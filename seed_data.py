# seed_data.py

from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import User, Product, Site, Quotation  # Adjust imports based on your project structure
from app.auth import get_password_hash

def seed_users(db: Session):
    """Seed initial users."""
    user1 = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123")
    )
    user2 = User(
        username="user1",
        email="user1@example.com",
        hashed_password=get_password_hash("user123")
    )
    db.add_all([user1, user2])
    db.commit()
    print("Seeded users.")

def seed_products(db: Session):
    """Seed initial products."""
    product1 = Product(
        product_name="Glass Product",
        glass_general_price=50.0,
        aluminum_frame_price=20.0,
        local_shipping_price=10.0
    )
    product2 = Product(
        product_name="Frame Product",
        stainless_steel_price=30.0,
        fix_cost_price=5.0
    )
    db.add_all([product1, product2])
    db.commit()
    print("Seeded products.")

def seed_sites(db: Session):
    """Seed initial sites."""
    site1 = Site(
        sitename="Site A",
        site_location="Location A",
        site_type="residential",
        user_id=1  # Ensure this user_id exists
    )
    site2 = Site(
        sitename="Site B",
        site_location="Location B",
        site_type="commercial",
        user_id=2  # Ensure this user_id exists
    )
    db.add_all([site1, site2])
    db.commit()
    print("Seeded sites.")

def seed_quotations(db: Session):
    """Seed initial quotations."""
    quotation1 = Quotation(
        site_id=1,  # Ensure this site_id exists
        product_id=1,  # Ensure this product_id exists
        width=120.0,
        height=80.0
    )
    quotation2 = Quotation(
        site_id=2,
        product_id=2,
        width=150.0,
        height=100.0
    )
    db.add_all([quotation1, quotation2])
    db.commit()
    print("Seeded quotations.")

def run_seeding():
    """Run all seeding functions."""
    init_db()  # Ensure tables are created before seeding
    db = SessionLocal()
    try:
        seed_users(db)
        seed_products(db)
        seed_sites(db)
        seed_quotations(db)
    finally:
        db.close()

if __name__ == "__main__":
    run_seeding()
