import uuid
from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, Table, Column, UniqueConstraint, func, Date,Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id_skill : Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default= lambda : str(uuid.uuid4())
    )

    name : Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    category : Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    description : Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable= False
    )

