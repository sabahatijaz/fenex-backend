from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from app.database import Database
from .. import models
from ..schemas import site_schemas, common, product_schemas, quotation_schemas
from app.crud.product import get_product
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
            shape=quotation.shape,
            quantity=quotation.quantity,
            linear_foot=quotation.linear_foot,
            square_foot=quotation.square_foot
        )
        session.add(db_quotation)
        await session.commit()
        await session.refresh(db_quotation)
        product_details=await get_product(current_user,quotation.product_id)
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

        quotation=quotation_schemas.QuotationResponse(id=db_quotation.id,site_id=db_quotation.site_id,
                                                        product_id=db_quotation.product_id,
                                                        width=db_quotation.width,
                                                        height=db_quotation.height,
                                                        shape=db_quotation.shape,
                                                        quantity=db_quotation.quantity,
                                                        linear_foot=db_quotation.linear_foot,
                                                        square_foot=db_quotation.square_foot,
                                                        product=product
                                                        )
        return quotation

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

                res_quotes.append(quotation_schemas.QuotationResponse(id=quote.id,site_id=quote.site_id,
                                                            product_id=quote.product_id,
                                                            width=quote.width,
                                                            height=quote.height,
                                                            shape=quote.shape,
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

            quotation=quotation_schemas.QuotationResponse(id=quote.id,site_id=quote.site_id,
                                                            product_id=quote.product_id,
                                                            width=quote.width,
                                                            height=quote.height,
                                                            shape=quote.shape,
                                                            quantity=quote.quantity,
                                                            linear_foot=quote.linear_foot,
                                                            square_foot=quote.square_foot,
                                                            product=product
                                                            )
        print(quotation.product)
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
