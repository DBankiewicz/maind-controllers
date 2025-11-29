from database.db import Base
from sqlalchemy import String, DateTime, JSON, Column


# sessions
# sid non null primary
# sess json not null
# expire timestamp not null


class Session(Base):
    __tablename__ = "sessions"

    sid = Column(String, primary_key=True)

    sess = Column(JSON, nullable=False)

    expire = Column(DateTime(timezone=True), nullable=False)

