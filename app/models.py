
from sqlalchemy import Column, Integer, String, Float, ForeignKey, ARRAY,Numeric,DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSONB  # Import JSONB for PostgreSQL support
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
# from sqlalchemy.sql import func
import pytz
# Create a base class
Base = declarative_base()

# Create the User table model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, nullable=False, default="user")
    # Relationship with Site (back_populates matches the 'user' relationship in Site)
    sites = relationship("Site", back_populates="user")

class Site(Base):
    __tablename__ = 'sitetable'
    
    id = Column(Integer, primary_key=True, index=True)
    sitename = Column(String, index=True, nullable=False)
    site_location = Column(JSONB, nullable=False)
    site_type = Column(String, nullable=False)
    risks = Column(ARRAY(String), nullable=True)
    
    # Foreign key to link with user
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationship with Quotation
    quotations = relationship("Quotation", back_populates="site")
    
    # Relationship with User
    user = relationship("User", back_populates="sites")

    
# Create the Product table model
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    glass_general_price = Column(Float, nullable=True)
    shipping_glass_supplier_price = Column(Float, nullable=True)
    aluminum_frame_price = Column(Float, nullable=True)
    stainless_steel_price = Column(Float, nullable=True)
    local_shipping_price = Column(Float, nullable=True)
    paint_al_frame_price = Column(Float, nullable=True)
    cut_assemble_frame_price = Column(Float, nullable=True)
    setting_block_price = Column(Float, nullable=True)
    install_glass_price = Column(Float, nullable=True)
    fix_cost_price = Column(Float, nullable=True)


# Create the Quotation table model
class Quotation(Base):
    __tablename__ = 'quotation'
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey('sitetable.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    width = Column(Float)
    height = Column(Float)
    shape = Column(String, nullable=False)
    custom_shape = Column(String, nullable=True)
    radius = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False)
    linear_foot = Column(Float) 
    square_foot = Column(Float)
    version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
    # Relationships
    history = relationship("QuotationHistory", back_populates="quotation")
    site = relationship("Site", back_populates="quotations")
    product = relationship("Product")

class Dimensions(Base):
    __tablename__ = 'pivot_table'
    
    id = Column(Integer, primary_key=True, index=True)
    width = Column(Numeric, nullable=False)
    height = Column(Numeric, nullable=False)
    positive_pressure = Column(Numeric, nullable=False)
    negative_pressure = Column(Numeric, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)

    product = relationship("Product", back_populates="pivot_table")

# Adding back reference to the Product model
Product.pivot_table = relationship("Dimensions", order_by=Dimensions.id, back_populates="product")


# create a new table to store the history of created quotations
class QuotationHistory(Base):
    __tablename__ = "quotation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotation.id"))
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    shape = Column(String, nullable=False)
    custom_shape = Column(String, nullable=True)
    radius = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False)
    linear_foot = Column(Float, nullable=True)
    square_foot = Column(Float, nullable=True)
    version = Column(Integer)  # Maintain the version history
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)
    # Relationships
    quotation = relationship("Quotation", back_populates="history")
