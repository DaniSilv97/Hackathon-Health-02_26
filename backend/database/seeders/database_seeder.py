"""
Database Seeder - Main seeder that calls all other seeders.
"""

from database.seeders.base_seeder import Seeder
from database.seeders.user_seeder import UserSeeder
from database.seeders.medication_seeder import MedicationSeeder


class DatabaseSeeder(Seeder):
    """
    Main database seeder.
    Calls all other seeders in the correct order.
    """

    @classmethod
    def run(cls) -> None:
        """Run all database seeds."""
        cls.call([
            UserSeeder,
            MedicationSeeder,
        ])
