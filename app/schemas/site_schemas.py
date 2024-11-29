from pydantic import BaseModel, Field , model_validator
from typing import Optional, List, Literal
from datetime import datetime
class Address(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: str

    def to_dict(self):
        return {
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "postal_code": self.postal_code,
        }

class SiteCreate(BaseModel):
    sitename: str 
    site_location: Address
    site_type: Literal['Residential', 'Commercial']  # Adjusted to match case sensitivity
    risks: List[str] = []  # List of risks associated with the site
    user_id: int  # Associated user ID


class SiteResponse(BaseModel):
    id: int
    sitename: str
    site_location: Address
    site_type: Literal['Residential', 'Commercial']
    risks: List[str]
    user_id: Optional[int] = None
    site_id: str  # This will store the formatted site_id
    last_updated:Optional[datetime] =None

    @model_validator(mode='before')
    def format_site_id(cls, values):
        site_id = values.id  
        if site_id:
            values.site_id = f"FX-{site_id}"  
        return values

    class Config:
        from_attributes = True 
        
class SiteUpdate(BaseModel):
    site_id: Optional[str] = None
    sitename: Optional[str] = None
    site_location: Optional[Address] = None
    site_type: Optional[Literal['Residential', 'Commercial']] = None
    risks: Optional[List[str]] = Field(default_factory=list)
    user_id: Optional[int] = None
    last_updated: Optional[datetime] =None

