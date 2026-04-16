from sqlalchemy import Column, Integer, String, Boolean

from app.Backend.db.db import Base

class Album(Base):
    __tablename__ = "album"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    description = Column(String)
    snt_id = Column(Integer)
    path = Column(String)
    photos_count = Column(Integer)
    is_active = Column(Boolean, default=True)