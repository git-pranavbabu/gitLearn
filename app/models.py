from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, text, TIMESTAMP
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text('true'), nullable=False)
    rating = Column(Integer, nullable=True, server_default=text('0'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="posts")
    votes = relationship("Vote", back_populates="post", passive_deletes=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    posts = relationship("Post", back_populates="user", passive_deletes=True)
    votes = relationship("Vote", back_populates="user", passive_deletes=True)

class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)

    user = relationship("User", back_populates="votes")
    post = relationship("Post", back_populates="votes")


    