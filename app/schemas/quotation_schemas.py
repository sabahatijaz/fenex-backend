
from pydantic import BaseModel, ConfigDict
from typing import Optional
from fastapi import Form
class QuotationCreate(BaseModel):
    site_id: int
    product_id: int
    width: float
    height: float
    linear_foot: Optional[float] = None
    square_foot: Optional[float] = None
    @classmethod
    def as_form(
          cls,
          site_id: int = Form(...),
          product_id: int = Form(...),
          width: float = Form(...),
          height: float = Form(...),
        ) -> 'QuotationCreate':
        linear_foot = ((width + height) * 2) / 12  
        square_foot = (width * height) / 144  
        return cls(site_id=site_id,
        product_id=product_id,
        width=width,
        height=height,
        linear_foot=linear_foot,
        square_foot=square_foot)

class QuotationUpdate(BaseModel):
    width: Optional[float] = None
    height: Optional[float] = None
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
          quote_number: Optional[str] = Form(None),
          client_name: Optional[str] = Form(None),
        ) -> 'QuotationUpdate': 
        return cls(width=width,
        height=height,
        quote_number=quote_number,
        client_name=client_name)


class QuotationResponse(BaseModel):
    id: int
    site_id: int
    product_id: int
    width: float
    height: float
    linear_foot: Optional[float] = None
    square_foot: Optional[float] = None

    class Config(ConfigDict):
        from_attributes = True

