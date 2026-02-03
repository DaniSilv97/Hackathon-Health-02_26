"""
Base Seeder class - Laravel-like seeder pattern for Flask.
"""

from abc import ABC, abstractmethod
from typing import List, Type


class Seeder(ABC):
    """
    Base seeder class for populating database with data.

    Similar to Laravel's Seeder class, provides:
    - run(): Main method to execute seeding logic
    - call(): Call other seeders
    """

    @classmethod
    @abstractmethod
    def run(cls) -> None:
        """
        Run the database seeds.
        Override this method in child seeders.
        """
        pass

    @classmethod
    def call(cls, seeders: List[Type['Seeder']]) -> None:
        """
        Call other seeders.

        Args:
            seeders: List of Seeder classes to run
        """
        for seeder in seeders:
            print(f'  Seeding: {seeder.__name__}')
            seeder.run()
            print(f'  Seeded:  {seeder.__name__}')
