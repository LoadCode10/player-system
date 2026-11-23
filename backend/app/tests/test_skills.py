BASE_URL = "/skills"


def test_create_skill_success(client):
    payload = {
        "name": "FastAPI",
        "category": "backend",
        "description": "Async Python web framework",
    }
    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "FastAPI"
    assert data["category"] == "backend"
    assert data["description"] == "Async Python web framework"
    assert "id_skill" in data


def test_create_skill_normalizes_category(client):
    payload = {
        "name": "Docker",
        "category": " Backend ",
    }
    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 201
    assert response.json()["category"] == "backend"


def test_create_duplicate_skill_case_insensitive_returns_409(client):
    client.post(BASE_URL, json={"name": "PostgreSQL", "category": "database"})
    response = client.post(BASE_URL, json={"name": "postgresql", "category": "database"})

    assert response.status_code == 409


def test_create_skill_unknown_category_returns_422(client):
    payload = {
        "name": "Rust",
        "category": "embedded_systems",
    }
    response = client.post(BASE_URL, json=payload)

    assert response.status_code == 422


def test_get_unknown_skill_id_returns_404(client):
    response = client.get(f"{BASE_URL}/99999")

    assert response.status_code == 404


def test_patch_skill_updates_only_sent_fields(client):
    create_resp = client.post(
        BASE_URL,
        json={
            "name": "React",
            "category": "frontend",
            "description": "Original description",
        },
    )
    skill_id = create_resp.json()["id_skill"]

    patch_resp = client.patch(
        f"{BASE_URL}/{skill_id}",
        json={"description": "Updated description"},
    )

    assert patch_resp.status_code == 200
    updated = patch_resp.json()
    assert updated["name"] == "React"
    assert updated["category"] == "frontend"
    assert updated["description"] == "Updated description"


def test_delete_skill_returns_204_then_get_returns_404(client):
    create_resp = client.post(
        BASE_URL,
        json={"name": "Redis", "category": "database"},
    )
    skill_id = create_resp.json()["id_skill*"]

    delete_resp = client.delete(f"{BASE_URL}/{skill_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"{BASE_URL}/{skill_id}")
    assert get_resp.status_code == 404