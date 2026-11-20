from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import SkillNotFound, SkillAlreadyExists
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate


UNIQUE_NAME_INDEX = "uq_skills_name_lower"

def is_name_conflict(exc: IntegrityError) -> bool:
    diag = getattr(exc.orig, "diag", None)
    return getattr(diag,"constraint_name",None) == UNIQUE_NAME_INDEX

def commit_or_conflict(db: Session, name:str):
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        if is_name_conflict(exc):
            raise SkillAlreadyExists(name)  from exc
        raise


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
    commit_or_conflict(db, skill_in.name)
    db.refresh(new_skill)
    return new_skill


def update_skill(
    skill_in : SkillUpdate,
    skill_id : str,
    db: Session 
):
    update_skill = get_skill(skill_id=skill_id,db=db)
    update_data = skill_in.model_dump(exclude_unset=True)

    new_name = update_data.get("name")
    if new_name and new_name.lower() != update_skill.name.lower():
        isExist_skill = db.query(Skill).filter(
            func.lower(Skill.name) == new_name.lower(),
            Skill.id_skill != update_skill.id_skill
        ).first()
        if isExist_skill:
            raise SkillAlreadyExists(new_name)

    for key, value in update_data.items():
        setattr(update_skill, key, value)

    commit_or_conflict(db, new_name or update_skill.name)
    db.refresh(update_skill)
    return update_skill


def delete_skill(
    skill_id : str,
    db: Session
):
    deleted_skill = get_skill(skill_id=skill_id, db=db)
    db.delete(deleted_skill)
    db.commit()
    