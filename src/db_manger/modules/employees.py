
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash


base = declarative_base()


class Employee(base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    employee_type_id = Column(Integer, ForeignKey('employee_types.id'))
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    staff_number = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    logged_in = Column(Boolean, nullable=False)
    user_token = Column(String)
    token_expiration = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    employee_type = relationship("EmployeeType", back_populates="employees")
    hotel = relationship("Hotel", back_populates="employees")

    def __init__(self, hotel_id, employee_type_id, staff_number, name, username, password, email):
        self.hotel_id = hotel_id
        self.employee_type_id = employee_type_id
        self.staff_number = staff_number
        self.name = name
        self.username = username
        self.password = generate_password_hash(password=password)
        self.email = email
        self.logged_in = False
        self.user_token = None
        self.token_expiration = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def set_token_expiration(self, expiration_datetime):
        self.token_expiration = expiration_datetime

    def is_token_expired(self):
        if self.token_expiration is None:
            return False
        return datetime.utcnow() > self.token_expiration

    def to_json(self):
        return {
            "id": self.id,
            "hotel_id": self.hotel_id,
            "employee_type_id": self.employee_type_id,
            "staff_number": self.staff_number,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "logged_in": self.logged_in
        }


