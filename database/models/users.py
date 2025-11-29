from database.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
#users
# id
# username
# pass_hash
# created_at
# updated at


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    pass_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    emails = relationship("Email", back_populates="owner", cascade="all, delete", passive_deletes=True)
