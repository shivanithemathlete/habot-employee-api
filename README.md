# Habot — Employee Management API

A secure REST API for managing employees within an organization.

Built as part of the **HabotConnect — Python Backend Developer** hiring assignment. This project demonstrates clean API design, JWT authentication, strict validation, filtering, pagination, correct HTTP semantics, and full automated test coverage.

---

## ✨ Features

- **JWT Bearer-token authentication** — Secure access control
- **Full CRUD operations** — Create, Read, Update, List, and Delete employees
- **Strong validation**:
  - Required name field
  - Valid and unique email addresses
- **Advanced filtering** — Filter by department and role
- **Pagination** — 10 records per page
- **Consistent HTTP status codes** — Proper REST semantics
- **Table-driven automated tests** — Comprehensive pytest coverage
- **Postman & curl friendly** — Easy to test and integrate

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | FastAPI |
| **ORM** | SQLAlchemy |
| **Database** | SQLite (file-based) |
| **Authentication** | JWT (python-jose + cryptography) |
| **Testing** | pytest |

---

## 🚀 Setup

### Quick Start (Using Makefile)

The easiest way to get started is using the provided Makefile:

```bash
# Clone repository
git clone <repository-url>
cd habot-employee-api

# Setup virtual environment and install dependencies
make setup

# Run the server
make run
```

### Manual Setup

Alternatively, you can set up manually:

#### 1. Clone Repository

```bash
git clone <repository-url>
cd habot-employee-api
```

#### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

### Available Makefile Commands

| Command | Description |
|---------|-------------|
| `make setup` | Create virtual environment and install dependencies |
| `make run` | Start the development server with auto-reload |
| `make test` | Run the full test suite |
| `make clean` | Remove virtual environment, database, and cache files |

---

## 🌐 Access URLs

| Service | URL |
|---------|-----|
| **API Base** | `http://127.0.0.1:8000` |
| **Swagger UI** | `http://127.0.0.1:8000/docs` |

---

## 🔐 Authentication

This API is protected by JWT Bearer tokens.

### Default Credentials

```
Username: admin
Password: admin123
```

### Obtain Token

**Endpoint:** `POST /api/employees/login`

**Content-Type:** `application/x-www-form-urlencoded`

**Request:**
```
username=admin
password=admin123
```

**Response:**
```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

### Use Token

All protected endpoints require the following header:

```
Authorization: Bearer <JWT_TOKEN>
```

---

## 📡 API Endpoints

> **Note:** All endpoints require authentication.

### Create Employee

**Endpoint:** `POST /api/employees/`

**Request Body:**
```json
{
  "name": "Alice",
  "email": "alice@test.com",
  "department": "HR",
  "role": "Manager"
}
```

**Response:** `201 Created`

---

### List Employees

**Endpoint:** `GET /api/employees/`

**Query Parameters:**
- `?page=2` — Pagination (10 records per page)
- `?department=HR` — Filter by department
- `?role=Manager` — Filter by role
- `?department=HR&role=Manager` — Combined filters

**Example:**
```
GET /api/employees/?page=1&department=HR&role=Manager
```

---

### Get Employee by ID

**Endpoint:** `GET /api/employees/{id}`

**Response:**
- `200 OK` — Employee found
- `404 Not Found` — Employee does not exist

---

### Update Employee

**Endpoint:** `PUT /api/employees/{id}`

**Request Body:** (any subset of fields allowed)
```json
{
  "name": "Alice Cooper",
  "email": "alice.new@test.com",
  "department": "Engineering",
  "role": "Developer"
}
```

---

### Delete Employee

**Endpoint:** `DELETE /api/employees/{id}`

**Response:** `204 No Content`

---

## ✅ Validation Rules

| Rule | Behavior |
|------|----------|
| Name is empty | `400 Bad Request` |
| Email is invalid | `422 Validation Error` |
| Email already exists | `400 Bad Request` |
| Invalid request body | `422 Validation Error` |
| Non-existent employee ID | `404 Not Found` |

---

## 🧪 Running Tests

Run the full automated test suite:

**Using Makefile (recommended):**
```bash
make test
```

**Or manually:**
```bash
pytest
```

### Test Coverage

The test suite includes:

- ✅ All CRUD operations
- ✅ Validation and error cases
- ✅ Pagination & filtering
- ✅ Authentication
- ✅ Update edge cases

Tests run against a real SQLite database and validate the full system end-to-end.

---

## 📝 Notes

- SQLite database file `employees.db` is created locally
- JWT secret is hardcoded for demo purposes only
- Auto-increment integer IDs are intentionally used (correct for internal HR systems)
- The API is designed for testing via Postman or curl as required in the assignment

---

## 📚 Additional Resources

- **Postman Collection:** Available in `postman/habot-employee-api.postman_collection.json`
- **Postman Environment:** Available in `postman/token_env.postman_environment.json`

---

*Built with ❤️ for HabotConnect*
