import uuid
from datetime import datetime
from sqlalchemy import (String, DateTime, Integer, Boolean, ForeignKey, Table, Column, UniqueConstraint, Text, func, false, Enum as SQLEnum)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.enums import Rank, QuestStatus

quest_skill = Table(
    "quest_skill",
    Base.metadata,
    Column("id_quest", ForeignKey("quests.id_quest", ondelete="CASCADE"), primary_key=True),
    Column("id_skill", ForeignKey("skills.id_skill", ondelete="RESTRICT"), primary_key=True),
)

def _values(enum_cls):
    return [e.value for e in enum_cls]

class Quest(Base):
    __tablename__ = "quests"

    id_quest: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String, nullable=False)
    topic: Mapped[str] = mapped_column(String, nullable=False)
    rank: Mapped[Rank] = mapped_column(
        SQLEnum(Rank, name="rank", values_callable=_values), nullable=False
    )
    status: Mapped[QuestStatus] = mapped_column(
        SQLEnum(QuestStatus, name="quest_status", values_callable=_values),
        nullable=False,
        server_default=QuestStatus.AVAILABLE.value,
    )
    problem: Mapped[str] = mapped_column(Text, nullable=False)
    technique_notes: Mapped[str | None] = mapped_column(Text)
    code_snippet: Mapped[str | None] = mapped_column(Text)
    solution_url: Mapped[str | None] = mapped_column(String)
    xp_reward: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cleared_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    steps: Mapped[list["QuestStep"]] = relationship(
        back_populates="quest", cascade="all, delete-orphan",
        order_by="QuestStep.position", passive_deletes=True,
    )
    skills: Mapped[list["Skill"]] = relationship(secondary=quest_skill)


class QuestStep(Base):
    __tablename__ = "quest_steps"
    __table_args__ = (
        UniqueConstraint("id_quest", "position", name="uq_quest_steps_quest_position"),
    )

    id_step: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_quest: Mapped[str] = mapped_column(
        ForeignKey("quests.id_quest", ondelete="CASCADE"), nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())

    quest: Mapped["Quest"] = relationship(back_populates="steps")