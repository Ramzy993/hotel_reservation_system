from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity

from src.db_manager.db_driver import DBDriver
from src.web_app.standard_response import StandardResponse


def validate_permission(permission):
    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()

            user = [DBDriver().get_guests(username=current_user), DBDriver().get_employees(username=current_user)][0]

            if permission in user.user_type.permissions:
                return function(*args, **kwargs)

            return StandardResponse({"error": 'not authorized'}, 401).to_json()
        return decorated_function
    return decorator
