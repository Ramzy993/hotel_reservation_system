
from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from src.db_manager.utils import UserRole, RolePermissions

base = declarative_base()


class UserType(base):
    __tablename__ = 'users_types'

    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True)
    permissions = Column(ARRAY(String))

    employees = relationship("Employee", back_populates="employee_type")

    def __init__(self, role: UserRole, permissions: list[RolePermissions]):
        self.role = role
        self.permissions = [permission.value for permission in permissions]

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type_,
            "roles": self.roles,
        }
