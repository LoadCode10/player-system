from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

ALLOWED_CATEGORIES: tuple[str, ...] = (
    "fundamentals",
    "backend",
    "frontend",
    "database",
    "ai_engineering",
    "devops",
    "cybersecurity",
    "networking",
    "machine_learning",
)

class SkillCreate(BaseModel):
  name : str = Field(..., min_length=2)
  category : str = Field(..., min_length=2)
  description : str | None = None

  @field_validator("name", "category", mode="before")
  @classmethod
  def strip_white_spaces(cls, value: str) -> str:
    if isinstance(value, str):
      return value.strip()
    return value

  @field_validator("category")
  @classmethod
  def validate_and_normalize_category(cls, value: str) -> str:
    normalized = value.lower()
    if normalized not in ALLOWED_CATEGORIES:
      allowed = ", ".join(ALLOWED_CATEGORIES)
      raise ValueError(f"Invalid category '{value}'. Must be one of: {allowed}")
    return normalized


class SkillUpdate(BaseModel):
  name: str | None = Field(default=None, min_length=2)
  category: str | None = Field(default=None, min_length=2)
  description: str | None = None 

  @field_validator("name", "category", mode="before")
  @classmethod
  def strip_whitespace(cls, value: str | None) -> str | None:
    if isinstance(value, str):
      return value.strip()
    return value

  @field_validator("category")
  @classmethod
  def validate_and_normalize_category(cls, value: str | None) -> str | None:
    if value is None:
        return value
    normalized = value.lower()
    if normalized not in ALLOWED_CATEGORIES:
      allowed = ", ".join(ALLOWED_CATEGORIES)
      raise ValueError(f"Invalid category '{value}'. Must be one of: {allowed}")
    return normalized

class SkillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_skill: str
    name: str
    category: str
    description: str | None
    created_at: datetime


    
