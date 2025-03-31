import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

# Set up in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database and override get_db dependency
@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_item():
    # Test creating an item
    response = client.post(
        "/api/items/",
        json={"title": "Test Item", "description": "Test Description", "is_active": True}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "Test Description"
    assert data["is_active"] == True
    assert "id" in data
    
    # Test getting the created item
    item_id = data["id"]
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id

def test_read_items():
    # Create a test item
    client.post(
        "/api/items/",
        json={"title": "Test Item", "description": "Test Description"}
    )
    
    # Get all items
    response = client.get("/api/items/")
    assert response.status_code == 200
    assert len(response.json()) > 0