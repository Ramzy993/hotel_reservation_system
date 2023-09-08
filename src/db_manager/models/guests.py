
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


from werkzeug.security import generate_password_hash, check_password_hash


base = declarative_base()


class Guest(base):
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True)
    guest_type_id = Column(Integer, ForeignKey('user_types.id'))
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    logged_in = Column(Boolean, nullable=False)
    user_token = Column(String)
    token_expiration = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user_type = relationship("UserType", back_populates="guests")

    def __init__(self, name, username, password, email, guest_type_id):
        self.guest_type_id = guest_type_id
        self.name = name
        self.username = username
        self.password = generate_password_hash(password=password)
        self.email = email
        self.logged_in = False
        self.user_token = None
        self.token_expiration = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

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


