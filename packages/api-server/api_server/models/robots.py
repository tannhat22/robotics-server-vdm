from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api_server.database import Base

class Robot(Base):
    __tablename__ = "robots"

    id = Column(Integer, primary_key=True, index=True)
    serial_no = Column(String(255))
    name = Column(String(255))
    ip_address = Column(String(255))