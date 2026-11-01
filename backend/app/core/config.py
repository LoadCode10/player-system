from pathlib import Path 
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

if not ENV_FILE_PATH.exists():
    print(f"\n❌ ERREUR: Fichier .env introuvable à l'emplacement : {ENV_FILE_PATH}\n")

class Settings(BaseSettings):
    DATABASE_URL : str = Field(
        ...,
        description="PostgreSQL Connection String (e.g., postgresql+asyncpg://user:pass@host:port/db)",
    )

    model_config=SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

try:
    settings = Settings()
except Exception as ex:
    print("CRITICAL: Failed to load application configuration.")
    print("Ensure backend/.env exists and contains a valid DATABASE_URL.\n")
    raise ex