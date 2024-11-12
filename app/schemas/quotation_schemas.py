
from pydantic import BaseModel, ConfigDict
from app.schemas.product_schemas import ProductResponse
from typing import Optional,List
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

class QuotationHeightWidthUpdate(BaseModel):
    width: Optional[float] = None
    height: Optional[float] = None

    @classmethod
    def as_form(
        cls,
        width: Optional[float] = Form(None),
        height: Optional[float] = Form(None),
    ) -> 'QuotationHeightWidthUpdate':
        return cls(width=width, height=height)

class QuotationResponse(BaseModel):
    id: int
    site_id: int
    product_id: int
    width: float
    height: float
    shape: str
    custom_shape: Optional[str] = None  # Make it optional
    radius: Optional[int] = None  # Make it optional
    quantity: int
    linear_foot: Optional[float] = None
    square_foot: Optional[float] = None
    product: ProductResponse

    class Config(ConfigDict):
        from_attributes = True

class QuotationHistoryResponse(BaseModel):
    id: int
    quotation_id: int
    width: Optional[float] = None
    height: Optional[float] = None
    shape: Optional[str] = None
    custom_shape: Optional[str] = None
    radius: Optional[int] = None
    quantity: Optional[int] = None
    linear_foot: Optional[float] = None
    square_foot: Optional[float] = None
    version: int

class QuotationWithHistoryResponse(BaseModel):
    current: QuotationResponse
    history: List[QuotationHistoryResponse]
