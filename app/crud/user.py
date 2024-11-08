from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, auth
from ..schemas import user_schemas
from ..utils.auth import verify_password
from sqlalchemy.exc import NoResultFound
from app.schemas import common
from app.database import Database  # Import the Database singleton
from sqlalchemy.future import select 
from sqlalchemy.orm import joinedload

# Initialize the Database instance
db_instance = Database()

# Helper function to get user by email
async def get_user_by_email(db: Session, email: str):
    stmt=select(models.User).filter(models.User.email == email)
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    return db_user

# Create user
async def create_user(user: user_schemas.UserCreate):
    async with db_instance.async_session() as session:
        db_user = await get_user_by_email(session, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = auth.get_password_hash(user.password)
        new_user = models.User(
            username=user.username, 
            email=user.email, 
            hashed_password=hashed_password,
            role=user.role or "user"
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

# Get all users with pagination
async def get_users(current_user,skip: int = 0, limit: int = 10):
    async with db_instance.async_session() as session:
        result = await session.execute(
            select(models.User).offset(skip).limit(limit)
        )
        return result.scalars().all()

# Get a single user by ID
async def get_user(current_user,user_id: int):
    async with db_instance.async_session() as session:
        user = await session.get(models.User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

# Delete user
async def delete_user(current_user, user_id: int):
    async with db_instance.async_session() as session:
        user = await session.get(models.User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(user)
        await session.commit()
        return common.BasicResponse(success=True)

# Authenticate user function
async def authenticate_user(email: str, password: str):
    async with db_instance.async_session() as session:
        user = await get_user_by_email(session, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

# Get quotations by user ID
async def get_quotations_by_user_id(current_user, user_id: int):
    async with db_instance.async_session() as session:
        result = await session.execute(
            select(models.Quotation)
            .join(models.Site)
            .options(joinedload(models.Quotation.product))  # Eager load related data
            .filter(models.Site.user_id == user_id)
        )
        
        quotations = result.scalars().all()
        if not quotations:
            raise HTTPException(status_code=404, detail="Quotations not found")
        
        return quotations