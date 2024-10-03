
from pydantic import BaseModel, ConfigDict
from app.schemas.product_schemas import ProductResponse
from typing import Optional
from fastapi import Form
class QuotationCreate(BaseModel):
    site_id: int
    product_id: int
    width: float
    height: float
    shape: str
    custom_shape: str
    radius: int
    quantity: int
    linear_foot: Optional[float] = None
    square_foot: Optional[float] = None
    @classmethod
    def as_form(
          cls,
          site_id: int = Form(...),
          product_id: int = Form(...),
          width: float = Form(...),
          height: float = Form(...),
          quantity: int = Form(...),
          shape: str = Form(...),
          custom_shape: str = Form(...),
          radius: int =Form(...),
        ) -> 'QuotationCreate':
        linear_foot = ((width + height) * 2) / 12  
        square_foot = (width * height) / 144  
        return cls(site_id=site_id,
        product_id=product_id,
        width=width,
        height=height,
        quantity=quantity,
        shape=shape,
        custom_shape=custom_shape,
        radius=radius,
        linear_foot=linear_foot,
        square_foot=square_foot)

class QuotationUpdate(BaseModel):
    width: Optional[float] = None
    height: Optional[float] = None
    shape: str
    custom_shape: str
    radius: int
    quantity: int
    calculation: Optional[float] = None   # Optional field for updates
    quote_number: Optional[str] = None
    client_name: Optional[str] = None
    linear_foot: Optional[float] = None
    square_foot: Optional[float] = None
    @classmethod
    def as_form(
          cls,
          width: Optional[float] = Form(None),
          height: Optional[float] = Form(None),
          quantity: int = Form(None),
          quote_number: Optional[str] = Form(None),
          client_name: Optional[str] = Form(None),
          shape: str = Form(None),
          custom_shape: str = Form(None),
          radius: int =Form(None),
        ) -> 'QuotationUpdate': 
        return cls(width=width,
        height=height,
        shape=shape,
        custom_shape=custom_shape,
        radius=radius,
        quantity=quantity,
        quote_number=quote_number,
        client_name=client_name)


class QuotationResponse(BaseModel):
    id: int
    site_id: int
    product_id: int
    width: float
    height: float
    shape: str
    custom_shape: str
    radius: int
    quantity: int
    linear_foot: Optional[float] = None
    square_foot: Optional[float] = None
    product: ProductResponse

    class Config(ConfigDict):
        from_attributes = True

