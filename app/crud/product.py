from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from app.database import Database
from .. import models
from sqlalchemy import func
from ..schemas import product_schemas
from sqlalchemy.future import select
from typing import List
# Initialize the Database instance
db_instance = Database()

async def create_product(current_user,product: product_schemas.ProductCreate):
    async with db_instance.async_session() as session:
        new_product = models.Product(
            product_name=product.product_name,
            glass_general_price=product.glass_general_price,
            shipping_glass_supplier_price=product.shipping_glass_supplier_price,
            aluminum_frame_price=product.aluminum_frame_price,
            stainless_steel_price=product.stainless_steel_price,
            local_shipping_price=product.local_shipping_price,
            paint_al_frame_price=product.paint_al_frame_price,
            cut_assemble_frame_price=product.cut_assemble_frame_price,
            setting_block_price=product.setting_block_price,
            install_glass_price=product.install_glass_price,
            fix_cost_price=product.fix_cost_price
        )
        
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        return new_product

async def get_products(current_user,skip: int = 0, limit: int = 10):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Product).offset(skip).limit(limit))
        return result.scalars().all()

async def get_product(current_user,product_id: int):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Product).filter(models.Product.id == product_id))
        product = result.scalars().first()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

async def delete_product(current_user,product_id: int):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Product).filter(models.Product.id == product_id))
        product = result.scalars().first()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        await session.delete(product)
        await session.commit()
        return product


async def get_products_by_names(product_names: List[str]) -> List[product_schemas.ProductResponse1]:
    normalized_names = {name.strip().lower() for name in product_names}

    async with db_instance.async_session() as session:
        # Execute a case-insensitive query to get products with names matching any in normalized_names
        result = await session.execute(
            select(models.Product).where(func.lower(models.Product.product_name).in_(normalized_names))
        )
        
        # Retrieve products from the query
        products = result.scalars().all()

        # Create a set of product names fetched from the database for easy lookup
        fetched_product_names = {product.product_name.lower() for product in products}

        # Check if any of the requested product names were not found
        not_found = normalized_names - fetched_product_names
        if not_found:
            raise HTTPException(status_code=404, detail=f"Products not found: {', '.join(not_found)}")

        # Filter the products to include only those exactly matching the requested names
        filtered_products = [
            product_schemas.ProductResponse1(id=product.id, product_name=product.product_name)
            for product in products if product.product_name.lower() in normalized_names
        ]

        return filtered_products