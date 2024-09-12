# app/crud/user.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, auth
from ..schemas import user_schemas

def create_user(db: Session, user: user_schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user


# for get quotaions by user id 
def get_quotations_by_user_id(db: Session, user_id: int):
    return (
        db.query(models.Quotation)
        .join(models.Site)
        .filter(models.Site.user_id == user_id)
        .all()
    )