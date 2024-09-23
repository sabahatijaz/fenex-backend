from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from app.database import Database
from .. import models
from ..schemas import quotation_schemas
from sqlalchemy.future import select

# Initialize the Database instance
db_instance = Database()

async def create_quotation(current_user, quotation: quotation_schemas.QuotationCreate):
    async with db_instance.async_session() as session:
        db_quotation = models.Quotation(
            site_id=quotation.site_id,
            product_id=quotation.product_id,
            width=quotation.width,
            height=quotation.height,
            linear_foot=quotation.linear_foot,
            square_foot=quotation.square_foot
        )
        session.add(db_quotation)
        await session.commit()
        await session.refresh(db_quotation)
        return db_quotation

async def get_quotations(current_user, skip: int = 0, limit: int = 10):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Quotation).offset(skip).limit(limit))
        return result.scalars().all()

async def get_quotation(current_user, quotation_id: int):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Quotation).filter(models.Quotation.id == quotation_id))
        quotation = result.scalars().first()
        if quotation is None:
            raise HTTPException(status_code=404, detail="Quotation not found")
        return quotation

async def update_quotation(current_user, quotation_id: int, quotation: quotation_schemas.QuotationUpdate):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Quotation).filter(models.Quotation.id == quotation_id))
        db_quotation = result.scalars().first()
        if db_quotation is None:
            raise HTTPException(status_code=404, detail="Quotation not found")

        if quotation.width is not None:
            db_quotation.width = quotation.width
            db_quotation.linear_foot = ((db_quotation.width + db_quotation.height) * 2) / 12  # Update calculation logic
        if quotation.height is not None:
            db_quotation.height = quotation.height
            db_quotation.square_foot = (db_quotation.width * db_quotation.height) / 144  # Update calculation logic
        if quotation.quote_number is not None:
            db_quotation.quote_number = quotation.quote_number
        if quotation.client_name is not None:
            db_quotation.client_name = quotation.client_name

        await session.commit()
        await session.refresh(db_quotation)
        return db_quotation

async def delete_quotation(current_user, quotation_id: int):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Quotation).filter(models.Quotation.id == quotation_id))
        quotation = result.scalars().first()
        if quotation is None:
            raise HTTPException(status_code=404, detail="Quotation not found")
        await session.delete(quotation)
        await session.commit()
        return quotation
