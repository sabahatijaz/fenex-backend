# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.orm import Session
from typing import List
from app.crud import user, site, quotation, product
from app.utils.auth import create_access_token, get_current_user
from app.schemas import user_schemas, site_schemas, product_schemas, quotation_schemas, common
from app.crud import user as user_crud, site as site_crud, quotation as quotation_crud, product as product_crud
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta

# Initialize FastAPI app instance
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# User Endpoints
@app.post("/users/", response_model=user_schemas.UserResponse,tags=["Users"])
async def create_user(new_user: user_schemas.UserCreate, current_user: str = Depends(get_current_user)):
    db_user = await user_crud.create_user(new_user)
    return db_user

@app.get("/users/", response_model=List[user_schemas.UserResponse],tags=["Users"])
async def read_users(skip: int = 0, limit: int = 10, current_user: str = Depends(get_current_user)):
    print(current_user.username)
    return await user.get_users(current_user, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=user_schemas.UserResponse,tags=["Users"])
async def read_user(user_id: int, current_user: str = Depends(get_current_user)):
    db_user = await user.get_user(current_user, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=common.BasicResponse,tags=["Users"])
async def delete_user(user_id: int, current_user: str = Depends(get_current_user)):
    return await user.delete_user(current_user, user_id)


# Sign-Up Endpoint
@app.post("/auth/signup", response_model=user_schemas.UserResponse, tags=["Auth"])
async def signup(new_user: user_schemas.UserCreate):
    # Create a new user
    db_user = await user_crud.create_user( new_user)
    return db_user

# Sign-In Endpoint
@app.post("/auth/signin", response_model=user_schemas.Token, tags=["Auth"])
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate the user
    user = await user_crud.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user)

    # Create access token
    access_token_expires = timedelta(minutes=30)  # Token expiration time
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# Site Endpoints
@app.post("/sites/", response_model=site_schemas.SiteResponse,tags=["Sites"])
async def create_site(site:site_schemas.SiteCreate = Depends(site_schemas.SiteCreate.as_form),current_user: str = Depends(get_current_user)
):
    db_site = await site_crud.create_site(current_user, site)
    return db_site


@app.get("/sites/", response_model=List[site_schemas.SiteResponse],tags=["Sites"])
async def read_sites(skip: int = 0, limit: int = 10, current_user: str = Depends(get_current_user)):
    return await site.get_sites(current_user, skip=skip, limit=limit)


@app.get("/sites/{site_id}", response_model=site_schemas.SiteResponse, tags=["Sites"])
async def read_site(site_id: int, current_user: str = Depends(get_current_user)):
    db_site = await site_crud.get_site(current_user, site_id)
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site


@app.put("/sites/{site_id}", response_model=site_schemas.SiteResponse,tags=["Sites"])
async def update_site(site_id: int,site:site_schemas.SiteUpdate= Depends(site_schemas.SiteUpdate.as_form),
    current_user: str = Depends(get_current_user)
):
    db_site = await site_crud.update_site(current_user,site_id, site)
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site



@app.delete("/sites/{site_id}", response_model=common.BasicResponse,tags=["Sites"])
async def delete_site(site_id: int, current_user: str = Depends(get_current_user)):
    return await site.delete_site(current_user, site_id)


@app.post("/products/", response_model=product_schemas.ProductResponse, tags=["Products"])
async def create_product(product:product_schemas.ProductCreate = Depends(product_schemas.ProductCreate.as_form),
    current_user: str = Depends(get_current_user)
):
    db_product = await product_crud.create_product(current_user, product)
    return db_product
    

@app.get("/products/", response_model=List[product_schemas.ProductResponse],tags=["Products"])
async def read_products(skip: int = 0, limit: int = 10, current_user: str = Depends(get_current_user)):
    return await product.get_products(current_user, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=product_schemas.ProductResponse,tags=["Products"])
async def read_product(product_id: int, current_user: str = Depends(get_current_user)):
    db_product = await product.get_product(current_user, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}", response_model=product_schemas.ProductResponse,tags=["Products"])
async def delete_product(product_id: int, current_user: str = Depends(get_current_user)):
    return await product.delete_product(current_user, product_id)

# Quotation Endpoints

@app.post("/quotations/", response_model=quotation_schemas.QuotationResponse, tags=["Quotations"])
async def create_quotation(quotation:quotation_schemas.QuotationCreate = Depends(quotation_schemas.QuotationCreate.as_form),current_user: str = Depends(get_current_user)):     
    db_quotation = await quotation_crud.create_quotation(current_user, quotation)
    return db_quotation


@app.get("/quotations/", response_model=List[quotation_schemas.QuotationResponse],tags=["Quotations"])
async def read_quotations(skip: int = 0, limit: int = 10, current_user: str = Depends(get_current_user)):
    return await quotation.get_quotations(current_user, skip=skip, limit=limit)


@app.get("/quotations/{quotation_id}", response_model=quotation_schemas.QuotationResponse,tags=["Quotations"])
async def read_quotation(quotation_id: int, current_user: str = Depends(get_current_user)):
    db_quotation = await quotation.get_quotation(current_user, quotation_id)
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return db_quotation


@app.put("/quotations/{quotation_id}", response_model=quotation_schemas.QuotationResponse, tags=["Quotations"])
async def update_quotation(quotation_id: int,quotation:quotation_schemas.QuotationUpdate = Depends(quotation_schemas.QuotationUpdate.as_form),current_user: str = Depends(get_current_user)):
    db_quotation = await quotation_crud.update_quotation(current_user, quotation_id, quotation)
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    
    return db_quotation


@app.delete("/quotations/{quotation_id}", response_model=quotation_schemas.QuotationResponse,tags=["Quotations"])
async def delete_quotation(quotation_id: int, current_user: str = Depends(get_current_user)):
    return await quotation.delete_quotation(current_user, quotation_id)

# get all quotations by using userid 
@app.get("/quotations/user/{user_id}", response_model=List[quotation_schemas.QuotationResponse], tags=["Quotations"])
async def get_quotations_by_user(user_id: int, current_user: str = Depends(get_current_user)):
    quotations = await user.get_quotations_by_user_id(current_user, user_id)
    if not quotations:
        raise HTTPException(status_code=404, detail="No quotations found for this user")
    return quotations