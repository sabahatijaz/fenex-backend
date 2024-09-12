
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base

#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create a base class
Base = declarative_base()

# Create the User table model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    sites = relationship("Site", back_populates="user")

# Create the Site table model
class Site(Base):
    __tablename__ = 'sitetable'
    id = Column(Integer, primary_key=True, index=True)
    sitename = Column(String, index=True)
    site_location = Column(String)
    site_type = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))  
    quotations = relationship("Quotation", back_populates="site")
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
    linear_foot = Column(Float) 
    square_foot = Column(Float)
    # Relationships
    site = relationship("Site", back_populates="quotations")
    product = relationship("Product")

