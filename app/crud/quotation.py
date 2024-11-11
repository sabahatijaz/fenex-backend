from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from app.database import Database
from .. import models
from ..schemas import site_schemas, common, product_schemas, quotation_schemas
from app.crud.product import get_product
from sqlalchemy.future import select
from typing import List
from sqlalchemy.orm import selectinload
# Initialize the Database instance
db_instance = Database()

async def create_quotation(current_user, quotation_data: quotation_schemas.QuotationCreate):
    async with db_instance.async_session() as session:

        quotation = models.Quotation(**quotation_data.model_dump())
        session.add(quotation)
        await session.commit()
        await session.refresh(quotation)
        await session.execute(
            select(models.Quotation)
            .options(selectinload(models.Quotation.product))
            .where(models.Quotation.id == quotation.id)
        )
        return quotation
    

async def update_quotation(current_user, quotation_id: int, quotation_data: quotation_schemas.QuotationUpdate):
    async with db_instance.async_session() as session:
        result = await session.execute(
            select(models.Quotation)
            .options(selectinload(models.Quotation.product))  # Eagerly load the product relation
            .where(models.Quotation.id == quotation_id)
        )
        
        quotation = result.scalar_one_or_none()

        if not quotation:
            return None

        # Create a history entry before updating the current quotation
        history_entry = models.QuotationHistory(
            quotation_id=quotation.id,
            width=quotation.width,
            height=quotation.height,
            shape=quotation.shape,
            custom_shape=quotation.custom_shape,
            radius=quotation.radius,
            quantity=quotation.quantity,
            linear_foot=quotation.linear_foot,
            square_foot=quotation.square_foot,
            version=quotation.version
        )
        session.add(history_entry)

        # Update the current quotation and increment the version
        for key, value in quotation_data.model_dump(exclude_unset=True).items():
            setattr(quotation, key, value)

            # Calculate linear_foot and square_foot if width or height is updated
            if key == 'width' and value is not None:
                quotation.linear_foot = ((quotation.width + quotation.height) * 2) / 12  # Update linear foot
            if key == 'height' and value is not None:
                quotation.square_foot = (quotation.width * quotation.height) / 144  # Update square foot

        # Increment version before committing the update
        quotation.version += 1

        # Commit the update and refresh the quotation
        await session.commit()
        await session.refresh(quotation)

        # Return the updated quotation
        return quotation

async def get_all_versions(quotation_id: int):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.QuotationHistory).filter(models.QuotationHistory.quotation_id == quotation_id))
        return result.scalars().all()
    
async def get_quotations(current_user, skip: int = 0, limit: int = 10):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Quotation).offset(skip).limit(limit))
        quotations= result.scalars().all()
        res_quotes=[]
        for i in range(len(quotations)):
                quote=quotations[i]
                p_id=quote.product_id
                product_details=await get_product(current_user,p_id)
                product=product_schemas.ProductResponse(id=product_details.id,
                                                        product_name=product_details.product_name,
                                                        glass_general_price=product_details.glass_general_price,
                                                        shipping_glass_supplier_price=product_details.shipping_glass_supplier_price,
                                                        aluminum_frame_price=product_details.aluminum_frame_price,
                                                        stainless_steel_price=product_details.stainless_steel_price,
                                                        local_shipping_price=product_details.local_shipping_price,
                                                        paint_al_frame_price=product_details.paint_al_frame_price,
                                                        cut_assemble_frame_price=product_details.cut_assemble_frame_price,
                                                        setting_block_price=product_details.setting_block_price,
                                                        install_glass_price=product_details.install_glass_price,
                                                        fix_cost_price=product_details.fix_cost_price)
                radius=quote.radius
                custom_shape=quote.custom_shape
                if not radius:
                    radius=0
                if not custom_shape:
                    custom_shape=""
                res_quotes.append(quotation_schemas.QuotationResponse(id=quote.id,site_id=quote.site_id,
                                                            product_id=quote.product_id,
                                                            width=quote.width,
                                                            height=quote.height,
                                                            shape=quote.shape,
                                                            custom_shape=custom_shape,
                                                            radius=radius,
                                                            quantity=quote.quantity,
                                                            linear_foot=quote.linear_foot,
                                                            square_foot=quote.square_foot,
                                                            product=product
                                                            ))
        return res_quotes

async def get_quotation(current_user, quotation_id: int):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Quotation).filter(models.Quotation.id == quotation_id))
        quote = result.scalars().first()
        print(quote.id)
        if quote is None:
            raise HTTPException(status_code=404, detail="Quotation not found")
        else:
            product_details=await get_product(current_user,quote.product_id)
            product=product_schemas.ProductResponse(id=product_details.id,
                                                        product_name=product_details.product_name,
                                                        glass_general_price=product_details.glass_general_price,
                                                        shipping_glass_supplier_price=product_details.shipping_glass_supplier_price,
                                                        aluminum_frame_price=product_details.aluminum_frame_price,
                                                        stainless_steel_price=product_details.stainless_steel_price,
                                                        local_shipping_price=product_details.local_shipping_price,
                                                        paint_al_frame_price=product_details.paint_al_frame_price,
                                                        cut_assemble_frame_price=product_details.cut_assemble_frame_price,
                                                        setting_block_price=product_details.setting_block_price,
                                                        install_glass_price=product_details.install_glass_price,
                                                        fix_cost_price=product_details.fix_cost_price)

            radius=quote.radius
            custom_shape=quote.custom_shape
            if not radius:
                radius=0
            if not custom_shape:
                custom_shape=""

            quotation=quotation_schemas.QuotationResponse(id=quote.id,site_id=quote.site_id,
                                                            product_id=quote.product_id,
                                                            width=quote.width,
                                                            height=quote.height,
                                                            shape=quote.shape,
                                                            custom_shape=custom_shape,
                                                            radius=radius,
                                                            quantity=quote.quantity,
                                                            linear_foot=quote.linear_foot,
                                                            square_foot=quote.square_foot,
                                                            product=product
                                                            )
        print(quotation.product)
        return quotation

async def delete_quotation(current_user, quotation_id: int):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Quotation).filter(models.Quotation.id == quotation_id))
        quotation = result.scalars().first()
        if quotation is None:
            raise HTTPException(status_code=404, detail="Quotation not found")
        await session.delete(quotation)
        await session.commit()
        return quotation


async def add_quotations_for_site(
    site_id: int, quotations: List[quotation_schemas.QuotationCreate]) -> List[models.Quotation]:
    async with db_instance.async_session() as session:  
        site_result = await session.execute(select(models.Site).filter(models.Site.id == site_id))
        site = site_result.scalar_one_or_none()
        if site is None:
            raise HTTPException(status_code=404, detail="Site not found")
        
        added_quotations = []
        for quotation in quotations:
            db_quotation = models.Quotation(
                site_id=site_id,
                product_id=quotation.product_id,
                width=quotation.width,
                height=quotation.height,
                shape=quotation.shape,
                custom_shape=quotation.custom_shape,
                radius=quotation.radius,
                quantity=quotation.quantity,
                linear_foot=quotation.linear_foot,
                square_foot=quotation.square_foot,
            )
            session.add(db_quotation)
            added_quotations.append(db_quotation)

        await session.commit()

        for quotation in added_quotations:
            await session.refresh(quotation)
            await session.execute(select(models.Quotation).options(selectinload(models.Quotation.product)))

        return added_quotations
    
# get all the quotations by show its version
async def get_current_and_history(quotation_id: int):
    async with db_instance.async_session() as session:
        # Fetch the current version of the quotation with the product relationship eagerly loaded
        current_result = await session.execute(
            select(models.Quotation)
            .options(selectinload(models.Quotation.product))  # Eagerly load the product relationship
            .where(models.Quotation.id == quotation_id)
        )
        current_quotation = current_result.scalar_one_or_none()

        if not current_quotation:
            return None, []

        # Fetch the history of the quotation with all fields loaded
        history_result = await session.execute(
            select(models.QuotationHistory)
            .where(models.QuotationHistory.quotation_id == quotation_id)
        )
        quotation_history = history_result.scalars().all()

        return current_quotation, quotation_history