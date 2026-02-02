from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(255), nullable=False, index=True, unique=True)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    published_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    is_published = Column(Boolean, default=False)
