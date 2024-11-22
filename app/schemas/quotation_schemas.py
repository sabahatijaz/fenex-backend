
from pydantic import BaseModel, ConfigDict
from app.schemas.product_schemas import ProductResponse
from typing import Optional,List
from datetime import datetime
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

    def __init__(self, **data):
        super().__init__(**data)
        self.linear_foot = ((self.width + self.height) * 2) / 12  
        self.square_foot = (self.width * self.height) / 144
class QuotationHeightWidthUpdate(BaseModel):
    width: Optional[float] = None
    height: Optional[float] = None

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
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime] = None 

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
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None


class QuotationWithHistoryResponse(BaseModel):
    current: QuotationResponse
    history: List[QuotationHistoryResponse]
