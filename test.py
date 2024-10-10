import asyncio
from app.database import Database
from app.models import Product,Quotation,Site
from sqlalchemy.future import select

# Seed products with dummy data
async def seed_dummy_products(db: Database):
    """Seed dummy product data."""
    dummy_products = [
        Product(
            product_name="Canopy",
            glass_general_price=30.0,
            shipping_glass_supplier_price=6.0,
            aluminum_frame_price=15.0,
            stainless_steel_price=0.0,
            local_shipping_price=0.0,
            paint_al_frame_price=8.0,
            cut_assemble_frame_price=5.0,
            setting_block_price=6.0,
            install_glass_price=9.0,
            fix_cost_price=45.0
        ),
        Product(
            product_name="windows",
            glass_general_price=90.0,
            shipping_glass_supplier_price=10.0,
            aluminum_frame_price=45.0,
            stainless_steel_price=0.0,
            local_shipping_price=0.0,
            paint_al_frame_price=14.0,
            cut_assemble_frame_price=25.0,
            setting_block_price=6.0,
            install_glass_price=10.0,
            fix_cost_price=55.0
        ),
        Product(
            product_name="Flood-windows",
            glass_general_price=90.0,
            shipping_glass_supplier_price=9.0,
            aluminum_frame_price=40.0,
            stainless_steel_price=0.0,
            local_shipping_price=0.0,
            paint_al_frame_price=16.0,
            cut_assemble_frame_price=25.0,
            setting_block_price=4.0,
            install_glass_price=8.0,
            fix_cost_price=55.0
        ),
         Product(
            product_name="Butt-glazed",
            glass_general_price=125.0,
            shipping_glass_supplier_price=10.0,
            aluminum_frame_price=40.0,
            stainless_steel_price=0.0,
            local_shipping_price=0.0,
            paint_al_frame_price=24.0,
            cut_assemble_frame_price=25.0,
            setting_block_price=4.0,
            install_glass_price=8.0,
            fix_cost_price=55.0
        ),
        Product(
            product_name="Skylight",
            glass_general_price=90.0,
            shipping_glass_supplier_price=25.0,
            aluminum_frame_price=40.0,
            stainless_steel_price=0.0,
            local_shipping_price=0.0,
            paint_al_frame_price=25.0,
            cut_assemble_frame_price=25.0,
            setting_block_price=4.0,
            install_glass_price=8.0,
            fix_cost_price=55.0
        ),
         Product(
            product_name="Walkable_skylight",
            glass_general_price=150.0,
            shipping_glass_supplier_price=0.0,
            aluminum_frame_price=70.0,
            stainless_steel_price=0.0,
            local_shipping_price=0.0,
            paint_al_frame_price=16.0,
            cut_assemble_frame_price=25.0,
            setting_block_price=0.0,
            install_glass_price=0.0,
            fix_cost_price=55.0
        ),
        Product(
            product_name="Solarium",
            glass_general_price=120.0,
            shipping_glass_supplier_price=10.0,
            aluminum_frame_price=35.0,
            stainless_steel_price=0.0,
            local_shipping_price=0.0,
            paint_al_frame_price=16.0,
            cut_assemble_frame_price=25.0,
            setting_block_price=6.0,
            install_glass_price=12.0,
            fix_cost_price=55.0
        ),
         Product(
            product_name="Flood_wall",
            glass_general_price=0.0,
            shipping_glass_supplier_price=0.0,
            aluminum_frame_price=0.0,
            stainless_steel_price=0.0,
            local_shipping_price=0.0,
            paint_al_frame_price=0.0,
            cut_assemble_frame_price=0.0,
            setting_block_price=0.0,
            install_glass_price=0.0,
            fix_cost_price=0.0
        ),
        Product(
            product_name="Fire_window",
            glass_general_price=110.0,
            shipping_glass_supplier_price=20.0,
            aluminum_frame_price=0.0,
            stainless_steel_price=80.0,
            local_shipping_price=0.0,
            paint_al_frame_price=0.0,
            cut_assemble_frame_price=25.0,
            setting_block_price=6.0,
            install_glass_price=12.0,
            fix_cost_price=55.0
        ),
         Product(
            product_name="Bullet-proof_window",
            glass_general_price=130.0,
            shipping_glass_supplier_price=10.0,
            aluminum_frame_price=0.0,
            stainless_steel_price=50.0,
            local_shipping_price=0.0,
            paint_al_frame_price=16.0,
            cut_assemble_frame_price=25.0,
            setting_block_price=6.0,
            install_glass_price=12.0,
            fix_cost_price=55.0
        ),
    ]
    async with db.async_session() as session:
        session.add_all(dummy_products)
        await session.commit()



async def seed_dummy_quotations(db: Database):
    """Seed dummy quotation data."""
    dummy_quotations = [
        Quotation(
          width=96.0,
          height=24.0,
          shape="Flat",
          custom_shape=None,
          radius=None,
          quantity=2
        ),
        Quotation(  
          width=118.0,
          height=118.0,
          shape="circle",
          custom_shape="circle",
          radius=59,
          quantity=2
        ),
        Quotation(
          width=72.0,
          height=68.0,
          shape="Flat",
          custom_shape=None,
          radius=None,
          quantity=2
        ),
        Quotation(
 
          width=56.0,
          height=126.0,
          shape="Flat",
          custom_shape=None,
          radius=None,
          quantity=2
        ),
        Quotation(
          width=210.0,
          height=32.4,
          shape="Flat",
          custom_shape=None,
          radius=None,
          quantity=2
        ),
        Quotation(
          width=90.0,
          height=36.0,
          shape="Flat",
          custom_shape=None,
          radius=None,
          quantity=2
        ),
        Quotation( 
          width=40.0,
          height=170.0,
          shape="Flat",
          custom_shape=None,
          radius=None,
          quantity=2
        ),
        Quotation(  
          width=54.0,
          height=36.0,
          shape="Flat",
          custom_shape=None,
          radius=None,
          quantity=2
        ),

        Quotation( 
          width=78.0,
          height=104.0,
          shape="Flat",
          custom_shape=None,
          radius=None,
          quantity=2
        ),
        Quotation(
          width=60.0,
          height=60.0,
          shape="circle",
          custom_shape="circle",
          radius=30,
          quantity=2
        ),
    ]
    async with db.async_session() as session:
        session.add_all(dummy_quotations)
        await session.commit()

async def seed_dummy_sites(db: Database):
    """Seed initial sites."""
    dummy_sites = [
       Site(
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
        ),
       Site(
          sitename="Oakwood Commercial Building",
          site_location={
              "street": "456 Oakwood Ave",
              "city": "Chicago",
              "state": "IL",
              "country": "USA",
              "postal_code": "60611",
           },
           site_type="Commercial",
           risks=["Fire", "Flood"],
          
        ),
       Site(
          sitename="Riverview Industrial Park",
          site_location={
             "street": "789 Riverview Dr",
             "city": "Peoria",
             "state": "IL",
             "country": "USA",
             "postal_code": "61614",
            },
            site_type="Industrial",
            risks=["Fire", "Environmental"],
            
       ),
       Site(
          sitename="Lakeside Condominiums",
          site_location={
              "street": "901 Lakeside Dr",
              "city": "Naperville",
              "state": "IL",
              "country": "USA",
              "postal_code": "60563",
            },
            site_type="Residential",
            risks=["Fire", "Flood"],
             
        ),
        Site(
          sitename="Downtown Office Building",
          site_location={
             "street": "1111 Main St",
             "city": "Rockford",
             "state": "IL",
             "country": "USA",
             "postal_code": "61101",
            },
            site_type="Commercial",
            risks=["Fire", "Earthquake"],
        ),
    ]
    async with db.async_session() as session:
        session.add_all(dummy_sites)
        await session.commit()


# Fetch all products from the database
async def fetch_all_products(db: Database):
    """Fetch all products and return their details."""
    async with db.async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        return products

# Fetch all quotations from the database
async def fetch_all_quotations(db: Database):
    """Fetch all products and return their details."""
    async with db.async_session() as session:
        result = await session.execute(select(Quotation))
        quotations = result.scalars().all()
        return quotations
    
# Fetch all sites from the database
async def fetch_all_sites(db: Database):
    """Fetch all products and return their details."""
    async with db.async_session() as session:
        result = await session.execute(select(Site))
        sites = result.scalars().all()
        return sites
    


async def main():
    db = Database()
    await db.connect()

    # Call the seeding functions
    await seed_dummy_products(db)
    await seed_dummy_quotations(db)
    await seed_dummy_sites(db)
    
    # fetch and print data to verify seeding
    products = await fetch_all_products(db)
    quotations = await fetch_all_quotations(db)
    sites = await fetch_all_sites(db)
    
    print("Seeded Products:", products)
    print("Seeded Quotations:", quotations)
    print("Seeded Sites:", sites)
    await db.disconnect() 

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())























