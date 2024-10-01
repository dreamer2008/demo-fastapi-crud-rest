from pydantic import BaseModel

class EmployeeModel(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str