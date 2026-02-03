"""
User Factory - Generate User model instances for testing and seeding.
"""

import random
import string
from typing import Any, Dict
from database.factories.base_factory import Factory
from app.models.user import User


class UserFactory(Factory):
    """
    Factory for creating User instances.

    Usage:
        # Create a random user
        user = UserFactory.create()

        # Create an admin
        admin = UserFactory.state('admin').create()

        # Create a clinician
        clinician = UserFactory.state('clinician').create()

        # Create a patient
        patient = UserFactory.state('patient').create()

        # Create with custom attributes
        user = UserFactory.create(name='John Doe', email='john@example.com')
    """

    model = User

    # Counter for unique emails
    _counter = 0

    @classmethod
    def _get_counter(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def _random_string(cls, length: int = 8) -> str:
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    @classmethod
    def definition(cls) -> Dict[str, Any]:
        """Default user state - creates a patient."""
        counter = cls._get_counter()
        return {
            'name': f'User {counter}',
            'email': f'user{counter}_{cls._random_string(4)}@example.com',
            'password': 'password123',  # Will be hashed by model
            'role': 'patient',
            'is_active': True,
        }

    # ==================== States ====================

    @classmethod
    def admin(cls) -> Dict[str, Any]:
        """State for admin users."""
        counter = cls._get_counter()
        return {
            'name': f'Admin {counter}',
            'email': f'admin{counter}_{cls._random_string(4)}@example.com',
            'role': 'admin',
        }

    @classmethod
    def clinician(cls) -> Dict[str, Any]:
        """State for clinician users."""
        counter = cls._get_counter()
        return {
            'name': f'Dr. Clinician {counter}',
            'email': f'clinician{counter}_{cls._random_string(4)}@example.com',
            'role': 'clinician',
        }

    @classmethod
    def patient(cls) -> Dict[str, Any]:
        """State for patient users."""
        counter = cls._get_counter()
        return {
            'name': f'Patient {counter}',
            'email': f'patient{counter}_{cls._random_string(4)}@example.com',
            'role': 'patient',
        }

    @classmethod
    def inactive(cls) -> Dict[str, Any]:
        """State for inactive users."""
        return {
            'is_active': False,
        }

    @classmethod
    def unverified(cls) -> Dict[str, Any]:
        """State for unverified users."""
        return {
            'email_verified_at': None,
        }

    # ==================== Helpers ====================

    @classmethod
    def create_admin(cls, **attributes) -> User:
        """Shortcut to create an admin user."""
        return cls.state('admin').create(**attributes)

    @classmethod
    def create_clinician(cls, **attributes) -> User:
        """Shortcut to create a clinician user."""
        return cls.state('clinician').create(**attributes)

    @classmethod
    def create_patient(cls, **attributes) -> User:
        """Shortcut to create a patient user."""
        return cls.state('patient').create(**attributes)
