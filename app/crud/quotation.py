from sqlalchemy.orm import Session
from fastapi import HTTPException
from..import models
from..schemas import quotation_schemas



def create_quotation(db: Session, quotation: quotation_schemas.QuotationCreate):
    db_quotation = models.Quotation(
        site_id=quotation.site_id,
        product_id=quotation.product_id,
        width=quotation.width,
        height=quotation.height,
        linear_foot=quotation.linear_foot,
        square_foot=quotation.square_foot
    )
    db.add(db_quotation)
    db.commit()
    db.refresh(db_quotation)
    return db_quotation

def get_quotations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Quotation).offset(skip).limit(limit).all()

def get_quotation(db: Session, quotation_id: int):
    return db.query(models.Quotation).filter(models.Quotation.id == quotation_id).first()



def update_quotation(db: Session, quotation_id: int, quotation: quotation_schemas.QuotationUpdate):
    db_quotation = db.query(models.Quotation).filter(models.Quotation.id == quotation_id).first()
    if db_quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")

    if quotation.width is not None:
        db_quotation.width = quotation.width
        db_quotation.linear_foot = ((db_quotation.width + db_quotation.height) * 2) / 12  # Update calculation logic
    if quotation.height is not None:
        db_quotation.height = quotation.height
        db_quotation.square_foot = (db_quotation.width * db_quotation.height) / 144  # Update calculation logic
    if quotation.quote_number is not None:
        db_quotation.quote_number = quotation.quote_number
    if quotation.client_name is not None:
        db_quotation.client_name = quotation.client_name
    # if quotation.total_amount is not None:
    #     db_quotation.total_amount = quotation.total_amount

    db.commit()
    db.refresh(db_quotation)
    return db_quotation

def delete_quotation(db: Session, quotation_id: int):
    quotation = db.query(models.Quotation).filter(models.Quotation.id == quotation_id).first()
    if quotation is None:
        raise HTTPException(status_code=404, detail="Quotation not found")
    db.delete(quotation)
    db.commit()
    return quotation