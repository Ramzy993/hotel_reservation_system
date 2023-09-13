
from sqlalchemy import Column, Integer, ARRAY, Enum


from src.db_manager import Base
from src.db_manager.utils import UserRole, RolePermissions


class UserType(Base):
    __tablename__ = 'users_types'

    id = Column(Integer, primary_key=True)
    role = Column(Enum(*UserRole.list_values(), name="UserRole"), nullable=False, unique=True)
    permissions = Column(ARRAY(Enum(*RolePermissions.list_values(), name="RolePermissions")))

    def __init__(self, role, permissions):
        self.role = role
        self.permissions = permissions

    def to_json(self):
        return {
            "id": self.id,
            "role": self.role,
            "permissions": self.permissions,
        }
