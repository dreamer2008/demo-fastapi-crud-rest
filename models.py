from sqlalchemy import Table, Column, Integer, String
from database import base

class Employee(base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String)
    phone = Column(String)

    def __repr__(self):
        return f"Employee(id={self.id}, firstName='{self.firstName}', lastName='{self.lastName}', email='{self.email}', phone='{self.phone}')"