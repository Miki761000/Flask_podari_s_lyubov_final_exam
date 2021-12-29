from functools import wraps

from flask import request
from werkzeug.exceptions import BadRequest, Forbidden
from werkzeug.routing import ValidationError

from managers.auth import auth


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            schema = schema_name()
            errors = schema.validate(request.get_json())
            if errors:
                raise BadRequest(f"Invalid fields {errors}")
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = auth.current_user()
            if not user.role == permission:
                raise Forbidden("You do not have the rights to access this resource")
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def positive_number(value):
    result = value >= 0
    if not result:
        raise ValidationError("Quantity must be positive number")
