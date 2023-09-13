
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash

from src.db_manager import Base
from src.db_manager.utils import UserRole


class Employee(Base):
    __tablename__ = 'employees'

    # TODO: use consecutive uuid instead of regular incremental id in all table
    id = Column(Integer, primary_key=True)
    employee_type_id = Column(Integer, ForeignKey('users_types.id'))
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    staff_number = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    logged_in = Column(Boolean, nullable=False, default=False)
    user_token = Column(String, default=None)
    token_expiration = Column(DateTime, default=datetime.utcnow())
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    user_type = relationship("UserType")
    hotel = relationship("Hotel", back_populates="employees")
    reservations = relationship("Reservation", back_populates="employee")

    def __init__(self, hotel_id, employee_type_id, staff_number, name, username, password, email):
        self.hotel_id = hotel_id
        self.employee_type_id = employee_type_id
        self.staff_number = staff_number
        self.name = name
        self.username = username
        self.password = generate_password_hash(password=password)
        self.email = email

    def is_admin(self):
        return self.user_type.role == UserRole.ADMIN.value

    def is_token_expired(self):
        if self.token_expiration is None:
            return False
        return datetime.utcnow() > self.token_expiration

    def check_password(self, password):
        return check_password_hash(self.password, password)

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


