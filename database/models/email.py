from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from database.db import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    analysis_id = Column(Integer, ForeignKey("email_analyses.id", ondelete="CASCADE"), nullable=True)

    content = Column(String, nullable=False)

    owner = relationship("User", back_populates='emails')
    analysis = relationship("EmailAnalysis", back_populates='email', cascade='all, delete', single_parent=True)
    group = relationship("Group", back_populates='emails')

class EmailAnalysis(Base):
    __tablename__ = "email_analyses"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, unique=True)
    sender = Column(String, nullable=True)
    recipients = Column(ARRAY(String), nullable=True)

    topic = Column(String, nullable=False)
    summary = Column(String, nullable=False)

    extra = Column(JSONB, nullable=True)

    email = relationship("Email", back_populates='analysis', uselist=False)
