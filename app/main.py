# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import user, site, quotation, product
from app.schemas import user_schemas, site_schemas, product_schemas, quotation_schemas
from app.crud import user as user_crud, site as site_crud, quotation as quotation_crud, product as product_crud
from app.database import init_db, get_db

# Initialize FastAPI app instance
app = FastAPI()
init_db()

# User Endpoints
@app.post("/users/", response_model=user_schemas.UserResponse,tags=["Users"])
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db, user)
    return db_user

@app.get("/users/", response_model=List[user_schemas.UserResponse],tags=["Users"])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=user_schemas.UserResponse,tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=user_schemas.UserResponse,tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user.delete_user(db, user_id)


# Site Endpoints
@app.post("/sites/", response_model=site_schemas.SiteResponse,tags=["Sites"])
def create_site(site:site_schemas.SiteCreate = Depends(site_schemas.SiteCreate.as_form),db: Session = Depends(get_db)
):
    db_site = site_crud.create_site(db, site)
    return db_site


@app.get("/sites/", response_model=List[site_schemas.SiteResponse],tags=["Sites"])
def read_sites(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return site.get_sites(db, skip=skip, limit=limit)


@app.get("/sites/{site_id}", response_model=site_schemas.SiteResponse, tags=["Sites"])
def read_site(site_id: int, db: Session = Depends(get_db)):
    db_site = site_crud.get_site(db, site_id)
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site


@app.put("/sites/{site_id}", response_model=site_schemas.SiteResponse,tags=["Sites"])
def update_site(site_id: int,site:site_schemas.SiteUpdate= Depends(site_schemas.SiteUpdate.as_form),
    db: Session = Depends(get_db)
):
    db_site = site_crud.update_site(db,site_id, site)
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site



@app.delete("/sites/{site_id}", response_model=site_schemas.SiteResponse,tags=["Sites"])
def delete_site(site_id: int, db: Session = Depends(get_db)):
    return site.delete_site(db, site_id)


@app.post("/products/", response_model=product_schemas.ProductResponse, tags=["Products"])
def create_product(product:product_schemas.ProductCreate = Depends(product_schemas.ProductCreate.as_form),
    db: Session = Depends(get_db)
):
    db_product = product_crud.create_product(db, product)
    return db_product
    

@app.get("/products/", response_model=List[product_schemas.ProductResponse],tags=["Products"])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return product.get_products(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=product_schemas.ProductResponse,tags=["Products"])
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = product.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}", response_model=product_schemas.ProductResponse,tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return product.delete_product(db, product_id)

# Quotation Endpoints

@app.post("/quotations/", response_model=quotation_schemas.QuotationResponse, tags=["Quotations"])
def create_quotation(quotation:quotation_schemas.QuotationCreate = Depends(quotation_schemas.QuotationCreate.as_form),db: Session = Depends(get_db)):     
    db_quotation = quotation_crud.create_quotation(db, quotation)
    return db_quotation


@app.get("/quotations/", response_model=List[quotation_schemas.QuotationResponse],tags=["Quotations"])
def read_quotations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return quotation.get_quotations(db, skip=skip, limit=limit)


@app.get("/quotations/{quotation_id}", response_model=quotation_schemas.QuotationResponse,tags=["Quotations"])
def read_quotation(quotation_id: int, db: Session = Depends(get_db)):
    db_quotation = quotation.get_quotation(db, quotation_id)
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return db_quotation


@app.put("/quotations/{quotation_id}", response_model=quotation_schemas.QuotationResponse, tags=["Quotations"])
def update_quotation(quotation_id: int,quotation:quotation_schemas.QuotationUpdate = Depends(quotation_schemas.QuotationUpdate.as_form),db: Session = Depends(get_db)):
    db_quotation = quotation_crud.update_quotation(db, quotation_id, quotation)
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    
    return db_quotation


@app.delete("/quotations/{quotation_id}", response_model=quotation_schemas.QuotationResponse,tags=["Quotations"])
def delete_quotation(quotation_id: int, db: Session = Depends(get_db)):
    return quotation.delete_quotation(db, quotation_id)

# get all quotations by using userid 
@app.get("/quotations/user/{user_id}", response_model=List[quotation_schemas.QuotationResponse], tags=["Quotations"])
def get_quotations_by_user(user_id: int, db: Session = Depends(get_db)):
    quotations = user.get_quotations_by_user_id(db, user_id)
    if not quotations:
        raise HTTPException(status_code=404, detail="No quotations found for this user")
    return quotations