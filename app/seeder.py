import asyncio
from database import Database
from app.models import Product, Quotation, Site, User
from app.auth import get_password_hash
from sqlalchemy.future import select
# Seed products with dummy data


async def seed_dummy_users(db: Database):
    """Seed initial users."""
    dummy_users = [
        User(
          username="amin",
          email="amin@example.com",
          hashed_password=get_password_hash("admin123")),
        User(
          username="user1",
          email="user1@example.com",
          hashed_password=get_password_hash("user123")),
        User(
          username="user2",
          email="user2@example.com",
          hashed_password=get_password_hash("user234")),
        User(
          username="user3",
          email="user3@example.com",
          hashed_password=get_password_hash("user34")),
        User(
          username="user4",
          email="user4@example.com",
          hashed_password=get_password_hash("user4")),
    ] 
    async with db.async_session() as session:
        session.add_all(dummy_users)
        await session.commit()

async def seed_dummy_products(db: Database):
    """Seed dummy product data."""
    dummy_products = [
        Product(product_name="Canopy", glass_general_price=30.0, shipping_glass_supplier_price=6.0,
                aluminum_frame_price=15.0, stainless_steel_price=0.0, local_shipping_price=0.0,
                paint_al_frame_price=8.0, cut_assemble_frame_price=5.0, setting_block_price=6.0,
                install_glass_price=9.0, fix_cost_price=45.0),
        Product(product_name="Windows", glass_general_price=90.0, shipping_glass_supplier_price=10.0,
                aluminum_frame_price=45.0, stainless_steel_price=0.0, local_shipping_price=0.0,
                paint_al_frame_price=14.0, cut_assemble_frame_price=25.0, setting_block_price=6.0,
                install_glass_price=10.0, fix_cost_price=55.0),
        Product(product_name="Flood_windows", glass_general_price=90.0, shipping_glass_supplier_price=9.0,
                aluminum_frame_price=40.0, stainless_steel_price=0.0, local_shipping_price=0.0,
                paint_al_frame_price=16.0, cut_assemble_frame_price=25.0, setting_block_price=4.0,
                install_glass_price=8.0, fix_cost_price=55.0),
        Product(product_name="Butt_glazed", glass_general_price=125.0, shipping_glass_supplier_price=10.0,
                aluminum_frame_price=40.0, stainless_steel_price=0.0, local_shipping_price=0.0,
                paint_al_frame_price=24.0, cut_assemble_frame_price=25.0, setting_block_price=4.0,
                install_glass_price=8.0, fix_cost_price=55.0),
        Product(product_name="Skylight", glass_general_price=90.0, shipping_glass_supplier_price=25.0,
                aluminum_frame_price=40.0, stainless_steel_price=0.0, local_shipping_price=0.0,
                paint_al_frame_price=25.0, cut_assemble_frame_price=25.0, setting_block_price=4.0,
                install_glass_price=8.0, fix_cost_price=55.0),
        Product(product_name="Walkable_skylight", glass_general_price=150.0, shipping_glass_supplier_price=0.0,
                aluminum_frame_price=70.0, stainless_steel_price=0.0, local_shipping_price=0.0,
                paint_al_frame_price=16.0, cut_assemble_frame_price=25.0, setting_block_price=0.0,
                install_glass_price=0.0, fix_cost_price=55.0),
        Product(product_name="Solarium", glass_general_price=120.0, shipping_glass_supplier_price=10.0,
                aluminum_frame_price=35.0, stainless_steel_price=0.0, local_shipping_price=0.0,
                paint_al_frame_price=16.0, cut_assemble_frame_price=25.0, setting_block_price=6.0,
                install_glass_price=12.0, fix_cost_price=55.0),
        Product(product_name="Flood_wall", glass_general_price=30.0, shipping_glass_supplier_price=8.0,
                aluminum_frame_price=35.0, stainless_steel_price=0.0, local_shipping_price=0.0,
                paint_al_frame_price=12.0, cut_assemble_frame_price=20.0, setting_block_price=6.0,
                install_glass_price=12.0, fix_cost_price=55.0),
        Product(product_name="Fire_window", glass_general_price=110.0, shipping_glass_supplier_price=20.0,
                aluminum_frame_price=0.0, stainless_steel_price=80.0, local_shipping_price=0.0,
                paint_al_frame_price=0.0, cut_assemble_frame_price=25.0, setting_block_price=6.0,
                install_glass_price=12.0, fix_cost_price=55.0),
        Product(product_name="Bullet_proof_window", glass_general_price=130.0, shipping_glass_supplier_price=10.0,
                aluminum_frame_price=0.0, stainless_steel_price=50.0, local_shipping_price=0.0,
                paint_al_frame_price=16.0, cut_assemble_frame_price=25.0, setting_block_price=6.0,
                install_glass_price=12.0, fix_cost_price=55.0),
    ]
    async with db.async_session() as session:
        session.add_all(dummy_products)
        await session.commit()


# Seed quotations with dummy data
async def seed_dummy_quotations(db: Database, site_ids, product_ids):
    """Seed dummy quotation data."""
    dummy_quotations = [
        Quotation(width=96.0, height=24.0, shape="Flat", custom_shape=None, radius=None, quantity=2,
                  site_id=site_ids[0], product_id=product_ids[0]),
        Quotation(width=118.0, height=118.0, shape="circle", custom_shape="circle", radius=59, quantity=2,
                  site_id=site_ids[1], product_id=product_ids[1]),
        Quotation(width=72.0, height=68.0, shape="Flat", custom_shape=None, radius=None, quantity=2,
                  site_id=site_ids[2], product_id=product_ids[2]),
        Quotation(width=56.0, height=126.0, shape="Flat", custom_shape=None, radius=None, quantity=2,
                  site_id=site_ids[3], product_id=product_ids[3]),
        Quotation(width=210.0, height=32.4, shape="Flat", custom_shape=None, radius=None, quantity=2,
                  site_id=site_ids[4], product_id=product_ids[4]),
        Quotation(width=90.0, height=36.0, shape="Flat", custom_shape=None, radius=None, quantity=2,
                  site_id=site_ids[0], product_id=product_ids[5]),
        Quotation(width=40.0, height=170.0, shape="Flat", custom_shape=None, radius=None, quantity=2,
                  site_id=site_ids[1], product_id=product_ids[6]),
        Quotation(width=54.0, height=36.0, shape="Flat", custom_shape=None, radius=None, quantity=2,
                  site_id=site_ids[2], product_id=product_ids[7]),
        Quotation(width=78.0, height=104.0, shape="Flat", custom_shape=None, radius=None, quantity=2,
                  site_id=site_ids[3], product_id=product_ids[8]),
        Quotation(width=60.0, height=60.0, shape="circle", custom_shape="circle", radius=30, quantity=2,
                  site_id=site_ids[4], product_id=product_ids[9]),
    ]
    async with db.async_session() as session:
        session.add_all(dummy_quotations)
        await session.commit()


# Seed sites with dummy data
async def seed_dummy_sites(db: Database):
    """Seed initial sites with user_id."""
    dummy_sites = [
        Site(sitename="Greenfield Residential Complex",
             site_location={"street": "123 Main St", "city": "Springfield", "state": "IL",
                            "country": "USA", "postal_code": "62701"},
             site_type="Residential", risks=["Fire", "Flood"], user_id=1),
        Site(sitename="Oakwood Commercial Building",
             site_location={"street": "456 Oakwood Ave", "city": "Chicago", "state": "IL",
                            "country": "USA", "postal_code": "60611"},
             site_type="Commercial", risks=["Fire", "Flood"], user_id=2),
        Site(sitename="Riverview Industrial Park",
             site_location={"street": "789 Riverview Dr", "city": "Peoria", "state": "IL",
                            "country": "USA", "postal_code": "61614"},
             site_type="Residential", risks=["Fire", "Environmental"], user_id=3),
        Site(sitename="Lakeside Condominiums",
             site_location={"street": "901 Lakeside Dr", "city": "Naperville", "state": "IL",
                            "country": "USA", "postal_code": "60563"},
             site_type="Residential", risks=["Fire", "Flood"], user_id=4),
        Site(sitename="Downtown Office Building",
             site_location={"street": "1111 Main St", "city": "Rockford", "state": "IL",
                            "country": "USA", "postal_code": "61101"},
             site_type="Commercial", risks=["Fire", "Earthquake"], user_id=5),
    ]
    async with db.async_session() as session:
        session.add_all(dummy_sites)
        await session.commit()


# Fetch all seeded products to verify seeding
async def fetch_all_products(db: Database):
    async with db.async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        for product in products:
            print(product)


# Fetch all seeded quotations to verify seeding
async def fetch_all_quotations(db: Database):
    async with db.async_session() as session:
        result = await session.execute(select(Quotation))
        quotations = result.scalars().all()
        for quotation in quotations:
            print(quotation)


# Fetch all seeded sites to verify seeding
async def fetch_all_sites(db: Database):
    async with db.async_session() as session:
        result = await session.execute(select(Site))
        sites = result.scalars().all()
        for site in sites:
            print(site)

async def fetch_all_users(db: Database):
    async with db.async_session() as session:
        result = await session.execute(select(Site))
        users = result.scalars().all()
        for user in users:
            print(user)

# Main function to run seeders
async def main():
    db = Database()
    await seed_dummy_users(db)
    await seed_dummy_products(db)
    await seed_dummy_sites(db)

    # Fetch IDs of seeded products and sites for quotations
    async with db.async_session() as session:
        products_result = await session.execute(select(Product))
        product_ids = [product.id for product in products_result.scalars().all()]

        sites_result = await session.execute(select(Site))
        site_ids = [site.id for site in sites_result.scalars().all()]

    # Seed quotations with the fetched IDs
    await seed_dummy_quotations(db, site_ids, product_ids)

    # Verify seeding
    await fetch_all_users(db)
    await fetch_all_products(db)
    await fetch_all_quotations(db)
    await fetch_all_sites(db)


if __name__ == "__main__":
    asyncio.run(main())
