from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Recipe(Base):
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(256), nullable=False)
    url = Column(String(255), nullable=True, index=True)
    source = Column(String(255), nullable=True)
    submitter_id = Column(String(10), ForeignKey("user.id"), nullable=True)
    submitter = relationship("User", back_populates="recipes")