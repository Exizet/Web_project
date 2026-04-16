from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.Backend.db.db import Base


class Snt(Base):
    __tablename__ = 'snt'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String)
    is_active = Column(Boolean, default=True)
    sites_quantity = Column(Integer)
    free_sites = Column(Integer, default=0)

    gardeners = relationship("Gardener", back_populates="nsnt")
    announce = relationship("Announcement", back_populates="nsnt")
    contacts = relationship("Contacts", back_populates="nsnt")
