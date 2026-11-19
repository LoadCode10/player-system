from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.exceptions import SkillNotFound, SkillAlreadyExists
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate


def list_skills(db: Session):
    skills_rows = (
        db.query(Skill)
        .order_by(Skill.created_at.desc())
        .all()
    )
    return skills_rows

def get_skill(
    skill_id: str,
    db : Session
):  
    founded_skill = db.query(Skill).filter_by(
        id_skill = skill_id
    ).first()

    if founded_skill is None:
        raise SkillNotFound(skill_id)
    return founded_skill


def create_skill(
    skill_in : SkillCreate,
    db: Session 
):
    existed_skill = db.query(Skill).filter(
        func.lower(Skill.name) == skill_in.name.lower()
    ).first()

    if existed_skill is not None:
        raise SkillAlreadyExists(skill_in.name)
    new_skill = Skill(
        name = skill_in.name,
        category = skill_in.category,
        description = skill_in.description
    )
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


def update_skill(
    skill_in : SkillUpdate,
    skill_id : str,
    db: Session 
):
    updated_skill = get_skill(skill_id=skill_id,db=db)
    update_data = skill_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(updated_skill, key, value)

    db.commit()
    db.refresh(updated_skill)
    return updated_skill


def delete_skill(
    skill_id : str,
    db: Session
):
    deleted_skill = get_skill(skill_id=skill_id, db=db)
    db.delete(deleted_skill)
    db.commit()