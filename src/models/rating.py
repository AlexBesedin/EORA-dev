from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime

from database.db import Base

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    similarity = Column(Float, nullable=False)
    response_time = Column(Float, nullable=False)


    project = relationship("Project", back_populates="ratings")