import enum
import uuid
from sqlalchemy import String, DateTime, Integer, Boolean,ForeignKey, Table, Column, UniqueConstraint,Index, func, Date,Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base

class QuestRank(str, enum.Enum):
    RANK_E = "E"
    RANK_D = "D"
    RANK_C = "C"
    RANK_B = "B"
    RANK_A = "A"
    RANK_S = "S"



class Quest(Base):

  __tablename__ = "quests"

  id_quest : Mapped[str] = mapped_column(
    String,
    primary_key=True,
    default=lambda: str(uuid.uuid4())
  )

  title: Mapped[str] = mapped_column(
    String,
    nullable=False
  )

  topic: Mapped[str] = mapped_column(
    String,
    nullable=False
  )

  rank: Mapped[QuestRank] = mapped_column(
    SQLEnum(
      QuestRank,
      name = "quest_rank",
      values_collable=lambda obj:[e.value for e in obj]
    ),
    nullable=False,
    default=QuestRank.RANK_E,
  )

  status : Mapped[str] = mapped_column(
     String,
     nullable=False,
     default="available"
  )

  problem: Mapped[str] = mapped_column(Text, nullable=False)
  technique_notes: Mapped[str] = mapped_column(Text, nullable=True)
  code_snippet: Mapped[str] = mapped_column(Text, nullable=True)
  solution_url: Mapped[str] = mapped_column(String, nullable=True)
  xp_reward: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
  is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

  started_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), nullable=True
  )
  cleared_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), nullable=True
  )
  created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True),
      nullable=False,
      server_default=func.now(),
  )

  steps: Mapped[list["QuestStep"]] = relationship(
    back_populates= "quest",
    cascade="all, delete-orphan",
    order_by="QuestStep.position"
  )


class QuestStep(Base):
   __tablename__ = "quest_step"

   id_step: Mapped[str] = mapped_column(
      String,
      primary_key=True,
      default=lambda: str(uuid.uuid4())    
   )

   id_quest: Mapped[str] = mapped_column(
      ForeignKey("quests.id_quest", ondelete="CASCADE"),
      nullable=False
   )

   position: Mapped[int] = mapped_column(
      Integer,
      nullable=False
   )

   is_done : Mapped[bool] = mapped_column(
      Boolean,
      default=False
   )

   quest: Mapped["Quest"] = relationship(
      back_populates="steps"
   )