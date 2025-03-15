from .base import Base, Column, Integer, String

class InteractionTypes(Base):
    __tablename__ = 'InteractionTypes'
    interaction_type_id = Column(Integer, primary_key=True)
    name = Column(String)