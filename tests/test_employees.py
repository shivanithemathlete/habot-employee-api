import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def uniq():
    return str(uuid.uuid4())[:8]


# -------- AUTH --------

def get_token():
    res = client.post(
        "/api/employees/login",
        data={"username": "admin", "password": "admin123"}
    )
    assert res.status_code == 200
    return res.json()["access_token"]


def auth_headers():
    return {"Authorization": f"Bearer {get_token()}"}


# -------- CREATE --------

def test_create_employee_cases():
    email = f"alice_{uniq()}@test.com"

    cases = [
        {
            "name": "valid",
            "payload": {
                "name": "Alice",
                "email": email,
                "department": "HR",
                "role": "Manager"
            },
            "status": 201
        },
        {
            "name": "duplicate_email",
            "payload": {
                "name": "Bob",
                "email": email
            },
            "status": 400
        },
        {
            "name": "missing_name",
            "payload": {
                "email": f"x_{uniq()}@test.com"
            },
            "status": 422
        },
        {
            "name": "invalid_email",
            "payload": {
                "name": "X",
                "email": "not-an-email"
            },
            "status": 422
        }
    ]

    headers = auth_headers()

    for c in cases:
        res = client.post("/api/employees/", json=c["payload"], headers=headers)
        assert res.status_code == c["status"], c["name"]


# -------- LIST + FILTER + PAGINATION --------

def test_list_and_filter():
    headers = auth_headers()

    for i in range(15):
        client.post(
            "/api/employees/",
            json={
                "name": f"Emp{i}",
                "email": f"emp{i}_{uniq()}@test.com",
                "department": "Engineering" if i % 2 == 0 else "HR",
                "role": "Developer"
            },
            headers=headers
        )

    cases = [
        {"url": "/api/employees/", "status": 200},
        {"url": "/api/employees/?page=2", "status": 200},
        {"url": "/api/employees/?department=HR", "status": 200},
        {"url": "/api/employees/?department=Engineering", "status": 200},
        {"url": "/api/employees/?role=Developer", "status": 200},
    ]

    for c in cases:
        res = client.get(c["url"], headers=headers)
        assert res.status_code == c["status"]


# -------- GET BY ID --------

def test_get_employee_cases():
    headers = auth_headers()

    create = client.post(
        "/api/employees/",
        json={"name": "Jane", "email": f"jane_{uniq()}@test.com"},
        headers=headers
    )
    emp_id = create.json()["id"]

    cases = [
        {"id": emp_id, "status": 200},
        {"id": 99999, "status": 404},
    ]

    for c in cases:
        res = client.get(f"/api/employees/{c['id']}", headers=headers)
        assert res.status_code == c["status"]


# -------- PUT --------

def test_update_employee_cases():
    headers = auth_headers()

    e1 = client.post(
        "/api/employees/",
        json={"name": "Alice", "email": f"alice_{uniq()}@test.com"},
        headers=headers
    ).json()

    e2 = client.post(
        "/api/employees/",
        json={"name": "Bob", "email": f"bob_{uniq()}@test.com"},
        headers=headers
    ).json()

    cases = [
        {"name": "update_name", "id": e1["id"], "payload": {"name": "Alice Cooper"}, "status": 200},
        {"name": "update_department", "id": e1["id"], "payload": {"department": "HR"}, "status": 200},
        {"name": "duplicate_email", "id": e1["id"], "payload": {"email": e2["email"]}, "status": 400},
        {"name": "invalid_email", "id": e1["id"], "payload": {"email": "bad"}, "status": 422},
        {"name": "empty_name", "id": e1["id"], "payload": {"name": ""}, "status": 422},
        {"name": "missing_employee", "id": 99999, "payload": {"name": "Ghost"}, "status": 404},
    ]

    for c in cases:
        res = client.put(f"/api/employees/{c['id']}", json=c["payload"], headers=headers)
        assert res.status_code == c["status"], c["name"]


# -------- DELETE --------

def test_delete_cases():
    headers = auth_headers()

    create = client.post(
        "/api/employees/",
        json={"name": "Temp", "email": f"temp_{uniq()}@test.com"},
        headers=headers
    )
    emp_id = create.json()["id"]

    cases = [
        {"id": emp_id, "status": 204},
        {"id": emp_id, "status": 404},
    ]

    for c in cases:
        res = client.delete(f"/api/employees/{c['id']}", headers=headers)
        assert res.status_code == c["status"]
