from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from database.db import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    sender = Column(String, nullable=True)
    receiver = Column(String, nullable=True)

    topic = Column(String, nullable=True)

    summary = Column(String, nullable=False)
    content = Column(String, nullable=False)

    tags = Column(String, nullable=False)

    analysis = Column(JSONB)


    owner = relationship("User", back_populates='emails')

