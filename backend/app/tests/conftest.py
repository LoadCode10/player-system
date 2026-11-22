import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app as fastapi_app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings
from app.models import Skill

# Swap the database name at the end of your existing DATABASE_URL
TEST_DATABASE_URL = settings.DATABASE_URL.rsplit("/", 1)[0] + "/player_system_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create all tables before the test suite runs and drop them afterward."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    """Provide a clean database session for each test, wiping rows after each run."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Clean all tables between tests so tests never leak state into one another
        with engine.begin() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                conn.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;'))


@pytest.fixture()
def client(db_session):
    """Provide a FastAPI TestClient with get_db overridden to use the test session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    fastapi_app.dependency_overrides[get_db] = override_get_db
    with TestClient(fastapi_app) as test_client:
        yield test_client
    fastapi_app.dependency_overrides.clear()

    