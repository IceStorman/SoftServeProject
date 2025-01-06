from .base import Base, Column, Integer, String

class Category(Base):
    __tablename__ = 'Category'
    category_id = Column(Integer, primary_key=True)
    name = Column(String)