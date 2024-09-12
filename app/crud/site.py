# app/crud/site.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from..import models
from..schemas import site_schemas


def create_site(db: Session, site: site_schemas.SiteCreate):
    user = db.query(models.User).filter(models.User.id == site.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    new_site = models.Site(
        sitename=site.sitename,
        site_location=site.site_location,
        site_type=site.site_type,
        user_id=site.user_id
    )
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    return new_site

def get_sites(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Site).offset(skip).limit(limit).all()


def get_site(db: Session, site_id: int):
    return db.query(models.Site).filter(models.Site.id == site_id).first()


def delete_site(db: Session, site_id: int):
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    db.delete(site)
    db.commit()
    return site


def update_site(db: Session, site_id: int, site: site_schemas.SiteUpdate):
    db_site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")

    if site.sitename is not None:
        db_site.sitename = site.sitename
    if site.site_location is not None:
        db_site.site_location = site.site_location
    if site.site_type is not None:
        db_site.site_type = site.site_type
    if site.user_id is not None:
        user = db.query(models.User).filter(models.User.id == site.user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        db_site.user_id = site.user_id

    db.commit()
    db.refresh(db_site)
    return db_site