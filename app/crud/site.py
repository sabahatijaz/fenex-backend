from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Depends
from app.database import Database
from .. import models
from ..schemas import site_schemas, common, product_schemas, quotation_schemas
from app.crud.product import get_product

# Initialize the Database instance
db_instance = Database()

async def create_site(current_user, site: site_schemas.SiteCreate):
    async with db_instance.async_session() as session:
        user = await session.execute(select(models.User).filter(models.User.id == site.user_id))
        user = user.scalars().first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid user ID")

        new_site = models.Site(
            sitename=site.sitename,
            site_location=site.site_location.to_dict(),
            site_type=site.site_type,
            risks=site.risks,
            user_id=site.user_id  # Associate site with the user
        )
        print(new_site.site_location)

        session.add(new_site)
        await session.commit()
        await session.refresh(new_site)

        return new_site

async def get_sites(current_user, skip: int = 0, limit: int = 10):
    async with db_instance.async_session() as session:  # Assuming db_instance is defined elsewhere
        result = await session.execute(
            select(models.Site).filter(models.Site.user_id == current_user.id).offset(skip).limit(limit)
        )
        return result.scalars().all()


async def get_site(current_user, site_id: int):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Site).filter(models.Site.id == site_id))
        site = result.scalars().first()
        if site is None:
            raise HTTPException(status_code=404, detail="Site not found")
        return site

async def delete_site(current_user, site_id: int):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Site).filter(models.Site.id == site_id))
        site = result.scalars().first()
        if site is None:
            raise HTTPException(status_code=404, detail="Site not found")

        await session.delete(site)
        await session.commit()
        return common.BasicResponse(success=True)

async def update_site(current_user, site_id: int, site: site_schemas.SiteUpdate):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Site).filter(models.Site.id == site_id))
        db_site = result.scalars().first()
        if db_site is None:
            raise HTTPException(status_code=404, detail="Site not found")

        if site.sitename is not None:
            db_site.sitename = site.sitename
        if site.site_location is not None:
            db_site.site_location = site.site_location
        if site.site_type is not None:
            db_site.site_type = site.site_type
        if site.user_id is not None:
            user = await session.execute(select(models.User).filter(models.User.id == site.user_id))
            user = user.scalars().first()
            if not user:
                raise HTTPException(status_code=400, detail="Invalid user ID")
            db_site.user_id = site.user_id

        await session.commit()
        await session.refresh(db_site)
        return db_site

async def get_quotations_by_site_id(current_user, site_id: int):
    async with db_instance.async_session() as session:
        # Check if the site exists
        result = await session.execute(select(models.Site).filter(models.Site.id == site_id))
        site = result.scalars().first()
        
        if not site:
            raise HTTPException(status_code=404, detail="Site not found")

        # Query quotations associated with the given site_id
        result = await session.execute(select(models.Quotation).filter(models.Quotation.site_id == site_id))
        quotations = result.scalars().all()
        res_quotes=[]

        if not quotations:
            return []  # Return an empty list if no quotations are found
        else:
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