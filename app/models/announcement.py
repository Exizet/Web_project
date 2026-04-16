from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.Backend.db.db import Base

class Announcement(Base):
    __tablename__ = "announce"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description= Column(String)
    snt_id = Column(Integer, ForeignKey('snt.id'))
    is_active = Column(Boolean, default=True)

    nsnt = relationship('Snt', back_populates='announce')