"""
Factories module - Laravel-like model factories for Flask.

Usage:
    from database.factories import UserFactory

    # Create a single user
    user = UserFactory.create()

    # Create multiple users
    users = UserFactory.create_many(10)

    # Create without saving to database
    user = UserFactory.make()

    # Create with custom attributes
    user = UserFactory.create(name='John Doe', role='admin')
"""

from database.factories.user_factory import UserFactory

__all__ = ['UserFactory']
