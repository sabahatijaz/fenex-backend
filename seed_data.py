import asyncio
from app.database import Database
from app.models import User, Product, Site, Quotation  # Adjust imports based on your project structure
from app.auth import get_password_hash

# Seeding users asynchronously
async def seed_users(db):
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
    async with db.async_session() as session:
        session.add_all([user1, user2])
        await session.commit()
    print("Seeded users.")

# Seeding products asynchronously
async def seed_products(db):
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
    async with db.async_session() as session:
        session.add_all([product1, product2])
        await session.commit()
    print("Seeded products.")

# Seeding sites asynchronously
async def seed_sites(db):
    """Seed initial sites."""
    site1 = Site(
        sitename="Greenfield Residential Complex",
        site_location={
            "street": "123 Main St",
            "city": "Springfield",
            "state": "IL",
            "country": "USA",
            "postal_code": "62701",
        },
        site_type="Residential",
        risks=["Fire", "Flood"],
        user_id=1  # Ensure this user_id exists
    )
    site2 = Site(
        sitename="Lakeside Commercial Plaza",
        site_location={
            "street": "456 Lakeshore Dr",
            "city": "Lakeside",
            "state": "IL",
            "country": "USA",
            "postal_code": "62702",
        },
        site_type="Commercial",
        risks=["Earthquake"],
        user_id=2  # Ensure this user_id exists
    )
    async with db.async_session() as session:
        session.add_all([site1, site2])
        await session.commit()
    print("Seeded sites.")

# Seeding quotations asynchronously
async def seed_quotations(db):
    """Seed initial quotations."""
    quotation1 = Quotation(
        site_id=1,  # Ensure this site_id exists
        product_id=1,  # Ensure this product_id exists
        width=120.0,
        height=80.0,
        shape="Flat",
        custom_shape=None,
        radius=None,
        quantity=2
    )
    quotation2 = Quotation(
        site_id=2,
        product_id=2,
        width=150.0,
        height=100.0,
        shape="Shape",
        custom_shape="Circle",
        radius=60,
        quantity=1
    )
    async with db.async_session() as session:
        session.add_all([quotation1, quotation2])
        await session.commit()
    print("Seeded quotations.")

# Run all seeding functions
async def run_seeding():
    """Run all seeding functions."""
    db = Database()
    await db.connect()  # Connect to the database
    try:
        await db.init_db()  # Ensure tables are created before seeding
        await seed_users(db)
        await seed_products(db)
        await seed_sites(db)
        await seed_quotations(db)
    finally:
        await db.disconnect()  # Disconnect from the database

if __name__ == "__main__":
    asyncio.run(run_seeding())  # Run the seeding asynchronously
