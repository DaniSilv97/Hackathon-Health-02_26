from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.models.user import UserRole


def role_required(*roles):
    """
    Decorator to require specific roles for a route.

    Usage:
        @role_required(UserRole.ADMIN)
        def admin_only():
            ...

        @role_required(UserRole.ADMIN, UserRole.CLINICIAN)
        def admin_or_clinician():
            ...
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')

            if user_role not in roles:
                return jsonify({
                    'error': 'Insufficient permissions',
                    'required_roles': list(roles),
                    'your_role': user_role
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper


def admin_required(fn):
    """Decorator to require admin role."""
    return role_required(UserRole.ADMIN)(fn)


def clinician_required(fn):
    """Decorator to require clinician role."""
    return role_required(UserRole.CLINICIAN)(fn)


def patient_required(fn):
    """Decorator to require patient role."""
    return role_required(UserRole.PATIENT)(fn)


def admin_or_clinician_required(fn):
    """Decorator to require admin or clinician role."""
    return role_required(UserRole.ADMIN, UserRole.CLINICIAN)(fn)
