from sqlalchemy import ARRAY, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from database.db import Base



class Project(Base):
    __tablename__ = 'projects'

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    url: Mapped[str] = mapped_column(String(2083), nullable=False, index=True)
    company: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    problem: Mapped[str] = mapped_column(Text, nullable=True)
    solution: Mapped[str] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True, index=True)
