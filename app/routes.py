from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import get_db

router = APIRouter(prefix="/api/employees", tags=["employees"])

@router.post("/", response_model=schemas.EmployeeOut, status_code=201)
def create(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    if crud.get_employee_by_email(db, employee.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_employee(db, employee)

@router.get("/", response_model=list[schemas.EmployeeOut])
def list_employees(
    page: int = Query(1, ge=1),
    department: str | None = None,
    role: str | None = None,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * 10
    return crud.get_employees(db, skip=skip, limit=10, department=department, role=role)

@router.get("/{employee_id}", response_model=schemas.EmployeeOut)
def get(employee_id: int, db: Session = Depends(get_db)):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.delete("/{employee_id}", status_code=204)
def delete(employee_id: int, db: Session = Depends(get_db)):
    emp = crud.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    crud.delete_employee(db, emp)
