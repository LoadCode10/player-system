from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.skill import Skill
from app.schemas.skill import SkillRead, SkillCreate, SkillUpdate

app = FastAPI(title="The System API")


@app.get("/list_skills", response_model=list[SkillRead])
def list_skills(db: Session = Depends(get_db)):
    skills_rows = (
        db.query(Skill)
        .order_by(Skill.created_at.desc())
        .all()
    )

    return skills_rows

@app.get("/get_skill/{skill_id}",response_model=SkillRead)
def get_skill(
    skill_id: str,
    db : Session = Depends(get_db)
):  
    
    founded_skill = db.query(Skill).filter_by(
        skill_id = Skill.id_skill
    ).first()

    if founded_skill is None:
        raise HTTPException(status_code= 404, detail="skill not found")

    return {
        "skill": founded_skill,
        "message" : "Skill Already Exists"
    }
    
    

# @app.post("create_skill", response_model=SkillCreate)
# def create_skill(
#     skill_inputs : SkillCreate,
#     db: Session = Depends(get_db)
# ):
    



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