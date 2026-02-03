"""
Base Factory class - Laravel-like factory pattern for Flask.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from app import db


class Factory(ABC):
    """
    Base factory class for generating model instances.

    Similar to Laravel's Factory class, provides methods for:
    - make(): Create instance without persisting
    - create(): Create and persist instance
    - create_many(): Create multiple instances
    """

    model: Type[db.Model] = None

    @classmethod
    @abstractmethod
    def definition(cls) -> Dict[str, Any]:
        """
        Define the model's default state.
        Override this method in child factories.

        Returns:
            Dict with default attribute values
        """
        pass

    @classmethod
    def make(cls, **attributes) -> db.Model:
        """
        Create a model instance without persisting to database.

        Args:
            **attributes: Override default attributes

        Returns:
            Model instance (not saved)
        """
        data = cls.definition()
        data.update(attributes)
        return cls.model(**data)

    @classmethod
    def create(cls, **attributes) -> db.Model:
        """
        Create a model instance and persist to database.

        Args:
            **attributes: Override default attributes

        Returns:
            Model instance (saved)
        """
        instance = cls.make(**attributes)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def create_many(cls, count: int, **attributes) -> List[db.Model]:
        """
        Create multiple model instances and persist to database.

        Args:
            count: Number of instances to create
            **attributes: Override default attributes for all instances

        Returns:
            List of model instances (saved)
        """
        instances = []
        for _ in range(count):
            instance = cls.make(**attributes)
            db.session.add(instance)
            instances.append(instance)
        db.session.commit()
        return instances

    @classmethod
    def make_many(cls, count: int, **attributes) -> List[db.Model]:
        """
        Create multiple model instances without persisting.

        Args:
            count: Number of instances to create
            **attributes: Override default attributes for all instances

        Returns:
            List of model instances (not saved)
        """
        return [cls.make(**attributes) for _ in range(count)]

    @classmethod
    def state(cls, state_name: str) -> 'FactoryBuilder':
        """
        Apply a state transformation to the factory.

        Args:
            state_name: Name of the state method to apply

        Returns:
            FactoryBuilder for chaining
        """
        return FactoryBuilder(cls).state(state_name)


class FactoryBuilder:
    """
    Builder class for chaining factory states.
    Similar to Laravel's Factory builder pattern.
    """

    def __init__(self, factory_class: Type[Factory]):
        self.factory_class = factory_class
        self.states: List[str] = []
        self.attributes: Dict[str, Any] = {}

    def state(self, state_name: str) -> 'FactoryBuilder':
        """Apply a state to the builder."""
        self.states.append(state_name)
        return self

    def with_attributes(self, **attributes) -> 'FactoryBuilder':
        """Add custom attributes."""
        self.attributes.update(attributes)
        return self

    def _apply_states(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply all registered states to the data."""
        for state_name in self.states:
            state_method = getattr(self.factory_class, state_name, None)
            if state_method and callable(state_method):
                state_data = state_method()
                data.update(state_data)
        return data

    def make(self, **attributes) -> db.Model:
        """Create instance without persisting."""
        data = self.factory_class.definition()
        data = self._apply_states(data)
        data.update(self.attributes)
        data.update(attributes)
        return self.factory_class.model(**data)

    def create(self, **attributes) -> db.Model:
        """Create and persist instance."""
        instance = self.make(**attributes)
        db.session.add(instance)
        db.session.commit()
        return instance

    def create_many(self, count: int, **attributes) -> List[db.Model]:
        """Create multiple instances."""
        instances = []
        for _ in range(count):
            instance = self.make(**attributes)
            db.session.add(instance)
            instances.append(instance)
        db.session.commit()
        return instances
