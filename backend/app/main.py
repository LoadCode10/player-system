from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

from app.core.exceptions import SkillNotFound, SkillAlreadyExists

from app.routers import skills


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

app.include_router(skills.router)

    
