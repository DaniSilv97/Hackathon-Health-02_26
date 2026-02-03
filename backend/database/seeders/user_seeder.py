"""
User Seeder - Populate database with initial users.
"""

from database.seeders.base_seeder import Seeder
from database.factories import UserFactory
from app.models.user import User
from app import db


class UserSeeder(Seeder):
    """
    Seeder for creating initial users.

    Creates:
    - 1 Admin user
    - 3 Clinician users
    - 10 Patient users
    """

    @classmethod
    def run(cls) -> None:
        """Run the user seeds."""

        # Create default admin (fixed credentials for development)
        if not User.query.filter_by(email='admin@health.com').first():
            admin = User(
                name='Administrator',
                email='admin@health.com',
                password='admin123',
                role='admin',
                is_active=True
            )
            db.session.add(admin)
            print('    Created: admin@health.com (password: admin123)')

        # Create default clinician
        if not User.query.filter_by(email='clinician@health.com').first():
            clinician = User(
                name='Dr. Default Clinician',
                email='clinician@health.com',
                password='clinician123',
                role='clinician',
                is_active=True
            )
            db.session.add(clinician)
            print('    Created: clinician@health.com (password: clinician123)')

        # Create default patient
        if not User.query.filter_by(email='patient@health.com').first():
            patient = User(
                name='Default Patient',
                email='patient@health.com',
                password='patient123',
                role='patient',
                is_active=True
            )
            db.session.add(patient)
            print('    Created: patient@health.com (password: patient123)')

        db.session.commit()

        # Create additional random users using factories
        print('    Creating additional users with factories...')

        # Additional clinicians
        UserFactory.state('clinician').create_many(2)
        print('    Created: 2 additional clinicians')

        # Additional patients
        UserFactory.state('patient').create_many(5)
        print('    Created: 5 additional patients')
