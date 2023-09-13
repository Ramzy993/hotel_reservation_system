
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from src.db_manager import Base


class Guest(Base):
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True)
    guest_type_id = Column(Integer, ForeignKey('users_types.id'))
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    logged_in = Column(Boolean, nullable=False, default=False)
    user_token = Column(String)
    token_expiration = Column(DateTime, default=datetime.utcnow())
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    user_type = relationship("UserType")
    reservations = relationship("Reservation", back_populates="guest")

    def __init__(self, name, username, password, email, guest_type_id):
        self.guest_type_id = guest_type_id
        self.name = name
        self.username = username
        self.password = generate_password_hash(password=password)
        self.email = email

    @staticmethod
    def is_admin():
        return False

    def is_token_expired(self):
        if self.token_expiration is None:
            return False
        return datetime.utcnow() > self.token_expiration

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "logged_in": self.logged_in
        }


