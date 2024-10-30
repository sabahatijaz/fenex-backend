
from pydantic import BaseModel, ConfigDict
from typing import Optional
from fastapi import Form


# Product Schemas
class ProductCreate(BaseModel):
    product_name: str
    glass_general_price: Optional[float] = None
    shipping_glass_supplier_price: Optional[float] = None
    aluminum_frame_price: Optional[float] = None
    stainless_steel_price: Optional[float] = None
    local_shipping_price: Optional[float] = None
    paint_al_frame_price: Optional[float] = None
    cut_assemble_frame_price: Optional[float] = None
    setting_block_price: Optional[float] = None
    install_glass_price: Optional[float] = None
    fix_cost_price: Optional[float] = None
    @classmethod
    def as_form(
          cls,
          product_name: str = Form(...),
          glass_general_price: Optional[float] = Form(None),
          shipping_glass_supplier_price: Optional[float] = Form(None),
          aluminum_frame_price: Optional[float] = Form(None),
          stainless_steel_price: Optional[float] = Form(None),
          local_shipping_price: Optional[float] = Form(None),
          paint_al_frame_price: Optional[float] = Form(None),
          cut_assemble_frame_price: Optional[float] = Form(None),
          setting_block_price: Optional[float] = Form(None),
          install_glass_price: Optional[float] = Form(None),
          fix_cost_price: Optional[float] = Form(None),
        ) -> 'ProductCreate':
        return cls(product_name=product_name,
        glass_general_price=glass_general_price,
        shipping_glass_supplier_price=shipping_glass_supplier_price,
        aluminum_frame_price=aluminum_frame_price,
        stainless_steel_price=stainless_steel_price,
        local_shipping_price=local_shipping_price,
        paint_al_frame_price=paint_al_frame_price,
        cut_assemble_frame_price=cut_assemble_frame_price,
        setting_block_price=setting_block_price,
        install_glass_price=install_glass_price,
        fix_cost_price=fix_cost_price)


class ProductResponse(BaseModel):
    id: int
    product_name: str
    glass_general_price: Optional[float] = None
    shipping_glass_supplier_price: Optional[float] = None
    aluminum_frame_price: Optional[float] = None
    stainless_steel_price: Optional[float] = None
    local_shipping_price: Optional[float] = None
    paint_al_frame_price: Optional[float] = None
    cut_assemble_frame_price: Optional[float] = None
    setting_block_price: Optional[float] = None
    install_glass_price: Optional[float] = None
    fix_cost_price: Optional[float] = None

    class Config(ConfigDict):
        from_attributes = True

class ProductResponse1(BaseModel):
    id: int
    product_name: str