# app/crud/product.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from..import models
from..schemas import product_schemas


def create_product(db: Session, product: product_schemas.ProductCreate):
    new_product = models.Product(
        product_name=product.product_name,
        glass_general_price=product.glass_general_price,
        shipping_glass_supplier_price=product.shipping_glass_supplier_price,
        aluminum_frame_price=product.aluminum_frame_price,
        stainless_steel_price=product.stainless_steel_price,
        local_shipping_price=product.local_shipping_price,
        paint_al_frame_price=product.paint_al_frame_price,
        cut_assemble_frame_price=product.cut_assemble_frame_price,
        setting_block_price=product.setting_block_price,
        install_glass_price=product.install_glass_price,
        fix_cost_price=product.fix_cost_price
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return product

