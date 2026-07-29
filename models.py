try:
    from .database import Base, engine
except ImportError:
    from database import Base, engine
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
