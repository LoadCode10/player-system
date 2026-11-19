from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.skill import SkillRead, SkillCreate, SkillUpdate

from app.services.skill_service import list_skills, get_skill, create_skill, update_skill, delete_skill

router = APIRouter(tags=["Skills"])

@router.get("/skills", response_model=list[SkillRead])
def get_skills_list_endpoint(
  db: Session = Depends(get_db)
):
  return list_skills(db=db)

@router.get("/skills/{skill_id}",response_model=SkillRead)
def get_skill_byID_endpoint(
  skill_id: str,
  db: Session = Depends(get_db)
):
  return get_skill(skill_id=skill_id, db=db)

@router.post("/skills",response_model=SkillRead, status_code=status.HTTP_201_CREATED)
def create_skill_endpoint(
  skill_in: SkillCreate,
  db: Session = Depends(get_db)
):
  return create_skill(skill_in=skill_in, db=db)

@router.patch("/skills/{skill_id}",response_model=SkillRead)
def update_skill_endpoint(
  skill_in: SkillUpdate,
  skill_id: str,
  db: Session = Depends(get_db)
):
  return update_skill(
    skill_in=skill_in,
    skill_id=skill_id,
    db=db
  )

@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill_endpoint(
  skill_id: str,
  db: Session =Depends(get_db)
):
  delete_skill(skill_id=skill_id, db=db)
  return {
    "message": "skill deleted successfully!"
  }