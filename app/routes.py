from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db
from .auth import authenticate, create_access_token, get_current_user

router = APIRouter(prefix="/api/employees", tags=["employees"])

# IMPORTANT: tokenUrl is RELATIVE to the router prefix
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ---------- AUTH ----------

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


def require_user(token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return user


# ---------- EMPLOYEES ----------

@router.post("/", response_model=schemas.EmployeeOut, status_code=201)
def create(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    user: str = Depends(require_user),
):
    if crud.get_employee_by_email(db, employee.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_employee(db, employee)


@router.get("/", response_model=list[schemas.EmployeeOut])
def list_employees(
    page: int = Query(1, ge=1),
    department: str | None = None,
    role: str | None = None,
    db: Session = Depends(get_db),
    user: str = Depends(require_user),
):
    skip = (page - 1) * 10
    return crud.get_employees(db, skip=skip, limit=10, department=department, role=role)


@router.get("/{employee_id}", response_model=schemas.EmployeeOut)
def get(
    employee_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(require_user),
):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.delete("/{employee_id}", status_code=204)
def delete(
    employee_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(require_user),
):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    crud.delete_employee(db, emp)
