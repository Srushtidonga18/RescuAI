import uuid
from sqlalchemy import Column, String, Integer, Float
from RescuAI.backend.app.core.database import Base

class ResourceItem(Base):
    __tablename__ = "resource_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)

class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
