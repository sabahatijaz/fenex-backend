from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from app.database import Database
from .. import models
from ..schemas import product_schemas
from sqlalchemy.future import select

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
