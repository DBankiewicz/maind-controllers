from database.db import Base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    public_id = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False)
    name = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    emails = relationship("Email", back_populates='group', cascade='all, delete', passive_deletes=True)