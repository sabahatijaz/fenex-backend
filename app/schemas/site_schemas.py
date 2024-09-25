from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Literal
from fastapi import Form

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

    @classmethod
    def as_form(
        cls,
        sitename: str = Form(...),
        street: str = Form(...),
        city: str = Form(...),
        state: str = Form(...),
        country: str = Form(...),
        postal_code: str = Form(...),
        site_type: Literal['Residential', 'Commercial'] = Form(...),
        risks: List[str] = Form(...),
        user_id: int = Form(...)
    ) -> 'SiteCreate':
        address = Address(street=street, city=city, state=state, country=country, postal_code=postal_code)
        return cls(
            sitename=sitename,
            site_location=address,
            site_type=site_type,
            risks=risks,
            user_id=user_id
        )

class SiteResponse(BaseModel):
    id: int
    sitename: str
    site_location: Address
    site_type: Literal['Residential', 'Commercial']
    risks: List[str]
    user_id: Optional[int] = None

    class Config(ConfigDict):
        from_attributes = True
        
class SiteUpdate(BaseModel):
    site_id: Optional[str] = None
    sitename: Optional[str] = None
    site_location: Optional[Address] = None
    site_type: Optional[Literal['Residential', 'Commercial']] = None
    risks: Optional[List[str]] = Field(default_factory=list)
    user_id: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        site_id: str = Form(...),
        name: str = Form(...),
        street: str = Form(...),
        city: str = Form(...),
        state: str = Form(...),
        country: str = Form(...),
        postal_code: str = Form(...),
        site_type: Literal['Residential', 'Commercial'] = Form(...),
        risks: List[str] = Form(...),
        user_id: int = Form(...)
    ) -> 'SiteUpdate':
        address = Address(street=street, city=city, state=state, country=country, postal_code=postal_code)
        return cls(
            site_id=site_id,
            sitename=sitename,
            site_location=address,
            site_type=site_type,
            risks=risks,
            user_id=user_id
        )
