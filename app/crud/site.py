from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Depends
from app.database import Database
from .. import models
from ..schemas import site_schemas

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
            site_location=site.site_location,
            site_type=site.site_type,
            user_id=site.user_id  # Associate site with the user
        )

        session.add(new_site)
        await session.commit()
        await session.refresh(new_site)

        return new_site

async def get_sites(current_user, skip: int = 0, limit: int = 10):
    async with db_instance.async_session() as session:
        result = await session.execute(select(models.Site).offset(skip).limit(limit))
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
