from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.Backend.db.db import Base


class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    phone = Column(String)
    email = Column(String)
    time_contact = Column(String, default=None)
    responsible = Column(String, default=None)
    title = Column(String)
    snt_id = Column(Integer, ForeignKey('snt.id'))
    is_active = Column(Boolean, default=True)

    nsnt = relationship('Snt', back_populates='contacts')