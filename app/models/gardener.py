from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.Backend.db.db import Base

class Gardener(Base):
    __tablename__ = 'gardener'

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(250))
    phone = Column(String(12))
    hashed_password = Column(String, unique=True)
    email = Column(String(100))
    snt_id = Column(Integer, ForeignKey('snt.id'))
    site_number = Column(Integer)
    is_admin = Column(Boolean, default=False)
    is_moderator = Column(Boolean, default=False)
    is_user = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    sites = relationship("Site", uselist=False, single_parent=True,back_populates="gardener")
    nsnt = relationship('Snt', back_populates='gardeners')

