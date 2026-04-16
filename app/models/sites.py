from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.Backend.db.db import Base

class Site(Base):
    __tablename__ = 'sites'

    site_number = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    site_owner = Column(String(100))
    owner_id = Column(Integer, ForeignKey('gardener.id'))

    gardener = relationship('Gardener', back_populates='sites')