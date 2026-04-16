from sqlalchemy import Column, Integer, String, Boolean

from app.Backend.db.db import Base

class Photo(Base):
    __tablename__ = 'Photos'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    image_path = Column(String)
    album_id = Column(Integer)
    is_active = Column(Boolean, default=True)