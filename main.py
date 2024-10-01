from fastapi import FastAPI, HTTPException, Depends

from typing import List, Annotated
import models
from api_models import EmployeeModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/employees/", response_model=EmployeeModel)
def create_employee(employee: EmployeeModel, db: db_dependency):
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.get("/employees/", response_model=List[EmployeeModel])
def read_employees(db: db_dependency):
    employees = db.query(models.Employee).all()
    return employees


@app.get("/employees/{employee_id}", response_model=EmployeeModel)
def read_employee(employee_id: int, db: db_dependency):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail=f"Employee[id={employee_id}] not found ")
    return employee


@app.put("/employees/{employee_id}", response_model=EmployeeModel)
def update_employee(employee_id: int, employee: EmployeeModel, db: db_dependency):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail=f"Employee[id={employee_id}] not found")
    db_employee.firstName = employee.firstName
    db_employee.lastName = employee.lastName
    db_employee.email = employee.email
    db_employee.phone = employee.phone
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.delete("/employees/{employee_id}", response_model=EmployeeModel)
def delete_employee(employee_id: int, db: db_dependency):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail=f"Employee[id={employee_id}] not found")
    db.delete(db_employee)
    db.commit()
    return db_employee

