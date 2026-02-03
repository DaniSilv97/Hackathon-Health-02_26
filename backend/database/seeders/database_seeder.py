"""
Database Seeder - Main seeder that calls all other seeders.
"""

from database.seeders.base_seeder import Seeder
from database.seeders.user_seeder import UserSeeder


class DatabaseSeeder(Seeder):
    """
    Main database seeder.

    This seeder calls all other seeders in the correct order.
    Similar to Laravel's DatabaseSeeder.
    """

    @classmethod
    def run(cls) -> None:
        """Run all database seeds."""
        cls.call([
            UserSeeder,
            # Add more seeders here as needed:
            # AppointmentSeeder,
            # PrescriptionSeeder,
            # etc.
        ])
