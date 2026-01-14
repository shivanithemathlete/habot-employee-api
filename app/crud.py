from sqlalchemy.orm import Session
from . import models, schemas

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employee_by_email(db: Session, email: str):
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def get_employees(db: Session, skip: int = 0, limit: int = 10, department=None, role=None):
    q = db.query(models.Employee)
    if department:
        q = q.filter(models.Employee.department == department)
    if role:
        q = q.filter(models.Employee.role == role)
    return q.offset(skip).limit(limit).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_emp = models.Employee(**employee.dict())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def delete_employee(db: Session, emp):
    db.delete(emp)
    db.commit()
