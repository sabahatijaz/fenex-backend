# app/main.py
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.orm import Session
from typing import List,Union,Dict
from app.utils.auth import create_access_token, get_current_user
from app.schemas import user_schemas, site_schemas, product_schemas, quotation_schemas, common
from app.crud import user as user_crud, site as site_crud, quotation as quotation_crud, product as product_crud
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
import pandas as pd
# Initialize FastAPI app instance
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv('pivot_table.csv')

@app.get("/possible-widths/", response_model=List[int])
async def get_possible_widths() -> List[int]:
    return df["WIDTH"].unique().tolist()

@app.get("/possible-lengths/", response_model=List[int])
async def get_possible_lengths() -> List[int]:
    return df["LENGTH"].unique().tolist()

@app.get("/width-by-length/{length}", response_model=Union[List[int], str])
async def get_width_by_length(length: int) -> Union[List[int], str]:
    widths = df[df["LENGTH"] == length]["WIDTH"].tolist()
    if not widths:
        raise HTTPException(status_code=404, detail="No widths found for the given length.")
    return widths

@app.get("/length-by-width/{width}", response_model=Union[List[int], str])
async def get_length_by_width(width: int) -> Union[List[int], str]:
    lengths = df[df["WIDTH"] == width]["LENGTH"].tolist()
    if not lengths:
        raise HTTPException(status_code=404, detail="No lengths found for the given width.")
    return lengths

@app.get("/pressures-by-length-and-width/{length}/{width}", response_model=Union[Dict[str, List[int]], str])
async def get_pressures_by_length_and_width(length: int, width: int) -> Union[Dict[str, List[int]], str]:
    positive_pressures = df[(df["LENGTH"] == length) & (df["WIDTH"] == width)]["POSITIVE_PRESSURE"].tolist()
    negative_pressures = df[(df["LENGTH"] == length) & (df["WIDTH"] == width)]["NEGATIVE_PRESSURE"].tolist()
    
    if not positive_pressures and not negative_pressures:
        raise HTTPException(status_code=404, detail="No pressures found for the given length and width.")
    
    return {
        "positive_pressures": positive_pressures,
        "negative_pressures": negative_pressures
    }


# User Endpoints
@app.post("/users/", response_model=user_schemas.UserResponse,tags=["Users"])
async def create_user(new_user: user_schemas.UserCreate, current_user: str = Depends(get_current_user)):
    db_user = await user_crud.create_user(new_user)
    return db_user

@app.get("/users/", response_model=List[user_schemas.UserResponse],tags=["Users"])
async def read_users(skip: int = 0, limit: int = 10, current_user: str = Depends(get_current_user)):
    print(current_user.username)
    return await user_crud.get_users(current_user, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=user_schemas.UserResponse,tags=["Users"])
async def read_user(user_id: int, current_user: str = Depends(get_current_user)):
    db_user = await user_crud.get_user(current_user, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=common.BasicResponse,tags=["Users"])
async def delete_user(user_id: int, current_user: str = Depends(get_current_user)):
    return await user_crud.delete_user(current_user, user_id)


# Sign-Up Endpoint
@app.post("/auth/signup", response_model=user_schemas.UserResponse, tags=["Auth"])
async def signup(new_user: user_schemas.UserCreate):
    # Create a new user
    db_user = await user_crud.create_user( new_user)
    return db_user

# Sign-In Endpoint
@app.post("/auth/signin", response_model=user_schemas.Token, tags=["Auth"])
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    print("form_data: ",form_data)
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
async def create_site(site:site_schemas.SiteCreate,current_user: str = Depends(get_current_user)
):
    db_site = await site_crud.create_site(current_user, site)
    return db_site


@app.get("/sites/", response_model=List[site_schemas.SiteResponse],tags=["Sites"])
async def read_sites(skip: int = 0, limit: int = 10, current_user: str = Depends(get_current_user)):
    return await site_crud.get_sites(current_user, skip=skip, limit=limit)


@app.get("/sites/{site_id}", response_model=site_schemas.SiteResponse, tags=["Sites"])
async def read_site(site_id: int, current_user: str = Depends(get_current_user)):
    db_site = await site_crud.get_site(current_user, site_id)
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site


@app.put("/sites/{site_id}", response_model=site_schemas.SiteResponse,tags=["Sites"])
async def update_site(site_id: int,site: site_schemas.SiteUpdate,
    current_user: str = Depends(get_current_user)
):
    db_site = await site_crud.update_site(current_user,site_id, site)
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site



@app.delete("/sites/{site_id}", response_model=common.BasicResponse,tags=["Sites"])
async def delete_site(site_id: int, current_user: str = Depends(get_current_user)):
    return await site_crud.delete_site(current_user, site_id)


@app.post("/products/", response_model=product_schemas.ProductResponse, tags=["Products"])
async def create_product(product:product_schemas.ProductCreate = Depends(product_schemas.ProductCreate.as_form),
    current_user: str = Depends(get_current_user)
):
    db_product = await product_crud.create_product(current_user, product)
    return db_product
    

@app.get("/products/", response_model=List[product_schemas.ProductResponse],tags=["Products"])
async def read_products(skip: int = 0, limit: int = 10, current_user: str = Depends(get_current_user)):
    return await product_crud.get_products(current_user, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=product_schemas.ProductResponse,tags=["Products"])
async def read_product(product_id: int, current_user: str = Depends(get_current_user)):
    db_product = await product_crud.get_product(current_user, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}", response_model=product_schemas.ProductResponse,tags=["Products"])
async def delete_product(product_id: int, current_user: str = Depends(get_current_user)):
    return await product_crud.delete_product(current_user, product_id)

# Quotation Endpoints

@app.post("/quotations/", response_model=quotation_schemas.QuotationResponse, tags=["Quotations"])
async def create_quotation(quotation:quotation_schemas.QuotationCreate ,current_user: str = Depends(get_current_user)):     
    print(quotation)
    db_quotation = await quotation_crud.create_quotation(current_user, quotation)
    return db_quotation


@app.get("/quotations/", response_model=List[quotation_schemas.QuotationResponse],tags=["Quotations"])
async def read_quotations(skip: int = 0, limit: int = 10, current_user: str = Depends(get_current_user)):
    return await quotation_crud.get_quotations(current_user, skip=skip, limit=limit)


@app.get("/quotations/{quotation_id}", response_model=quotation_schemas.QuotationResponse,tags=["Quotations"])
async def read_quotation(quotation_id: int, current_user: str = Depends(get_current_user)):
    db_quotation = await quotation_crud.get_quotation(current_user, quotation_id)
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
    return await quotation_crud.delete_quotation(current_user, quotation_id)

# get all quotations by using userid 
@app.get("/quotations/user/{user_id}", response_model=List[quotation_schemas.QuotationResponse], tags=["Quotations"])
async def get_quotations_by_user(user_id: int, current_user: str = Depends(get_current_user)):
    quotations = await user_crud.get_quotations_by_user_id(current_user, user_id)
    if not quotations:
        raise HTTPException(status_code=404, detail="No quotations found for this user")
    return quotations

# get all quotations by using siteid 
@app.get("/quotations/site/{site_id}", response_model=List[quotation_schemas.QuotationResponse], tags=["Quotations"])
async def get_quotations_by_site(site_id: int, current_user: str = Depends(get_current_user)):
    quotations = await site_crud.get_quotations_by_site_id(current_user, site_id)
    if not quotations:
        raise HTTPException(status_code=404, detail="No quotations found for this site")
    return quotations


@app.get("/shapes", response_model=List[str], tags=["Shapes"])
async def get_shapes(current_user: str = Depends(get_current_user)):
    shapes = [
                "UE SIDED TRAPEZOID",
                "TRIANGLE",
                "HALF-CIRCLE",
                "EYEBROW",
                "HALF EYEBROW",
                "HALF ELLIPTICAL",
                "TRAPEZOID",
                "PENTAGON",
                "OVAL",
                "ELIPTICAL",
                "ARCH",
                "GOTHIC",
                "QUARTER SEGMENT",
                "QUARTER CIRCLE",
                "FULL CIRCLE",
                "OCTAGON",
                "HALF ARCH",
                "WAVE SHAPE",
                "EXTENDED FULL ELLIPSE",
                "EQUAL LEG TRIANGLE",
                "FAN",
                "HEXAGON",
                "HOTDOG",
                "HALF FAN"
            ]
    return shapes
