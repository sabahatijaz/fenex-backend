# app/schemas/site.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from fastapi import Form

class SiteCreate(BaseModel):
    sitename: str 
    site_location: str
    site_type: Literal['residential', 'commercial']
    user_id: int 
    @classmethod
    def as_form(
          cls,
          sitename: str = Form(...),
          site_location: str = Form(...),
          site_type: Literal['residential', 'commercial'] = Form(...),
          user_id: int = Form(...)
        ) -> 'SiteCreate':
        return cls(sitename=sitename, site_location=site_location, site_type=site_type, user_id=user_id)

class SiteResponse(BaseModel):
    id: int
    sitename: str
    site_location: str
    site_type: Literal['residential', 'commercial']
    user_id: Optional[int] = None

    class Config(ConfigDict):
        from_attributes = True
        
class SiteUpdate(BaseModel):
    sitename: Optional[str] = None
    site_location: Optional[str] = None
    site_type: Optional[Literal['residential', 'commercial']] = None
    user_id: Optional[int] = None
    @classmethod
    def as_form(
          cls,
          sitename: str = Form(...),
          site_location: str = Form(...),
          site_type: Literal['residential', 'commercial'] = Form(...),
          user_id: int = Form(...)
        ) -> 'SiteUpdate':
        return cls(sitename=sitename, site_location=site_location, site_type=site_type, user_id=user_id)