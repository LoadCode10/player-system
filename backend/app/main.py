from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.exceptions import SkillNotFound, SkillAlreadyExists
from app.db.session import get_db
from app.models.skill import Skill
from app.schemas.skill import SkillRead, SkillCreate, SkillUpdate

app = FastAPI(title="The System API")


@app.exception_handler(SkillNotFound)
async def skill_not_found_handler(
    request: Request,
    exc: SkillNotFound
):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message}
    )

@app.exception_handler(SkillAlreadyExists)
async def skill_already_exist_handler(
    request: Request,
    exc: SkillAlreadyExists
):
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message}
    )


@app.get("/skills/list_skills", response_model=list[SkillRead])
def list_skills(db: Session = Depends(get_db)):
    skills_rows = (
        db.query(Skill)
        .order_by(Skill.created_at.desc())
        .all()
    )
    return skills_rows


@app.get("/skills/get_skill/{skill_id}",response_model=SkillRead)
def get_skill(
    skill_id: str,
    db : Session = Depends(get_db)
):  
    
    founded_skill = db.query(Skill).filter_by(
        id_skill = skill_id
    ).first()

    if founded_skill is None:
        raise SkillNotFound(skill_id)

    return founded_skill


@app.post("/skills/create_skill", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
def create_skill(
    request: Request,
    skill_in : SkillCreate,
    db: Session = Depends(get_db)
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

@app.patch("/skills/update_skill/{skill_id}",
           response_model=SkillRead)
def update_skill(
    skill_in : SkillUpdate,
    skill_id : str,
    db: Session = Depends(get_db)
):
    updated_skill = get_skill(skill_id=skill_id,db=db)
    update_data = skill_in.model_dump(exclude_unset=True)

    for key, value in update_data.items:
        setattr(updated_skill, key, value)

    db.commit()
    db.refresh(updated_skill)
    return updated_skill





    
@app.get("/")
def root():
    return {"message": "The System API is online"}


# @app.get("/health")
# def health():
#     return {
#         "status": "online",
#         "message": "The System is awake."
#     }

# @app.get("/db-check")
# def db_check(db: Session = Depends(get_db)):
#     result = db.execute(text("SELECT 1")).scalar()
#     return {
#         "status" : "online",
#         "result" : result
#     }