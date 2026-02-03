"""
Medication Factory - Generate Medication model instances.
"""

import random
from typing import Any, Dict
from database.factories.base_factory import Factory
from app.models.medication import Medication


class MedicationFactory(Factory):
    """Factory for creating Medication instances."""

    model = Medication
    _counter = 0

    # Sample medication data
    MEDICATIONS = [
        {'name': 'Paracetamol', 'strength': '500mg', 'form': 'tablet'},
        {'name': 'Ibuprofeno', 'strength': '400mg', 'form': 'tablet'},
        {'name': 'Amoxicilina', 'strength': '500mg', 'form': 'capsule'},
        {'name': 'Omeprazol', 'strength': '20mg', 'form': 'capsule'},
        {'name': 'Metformina', 'strength': '850mg', 'form': 'tablet'},
        {'name': 'Losartan', 'strength': '50mg', 'form': 'tablet'},
        {'name': 'Atorvastatina', 'strength': '20mg', 'form': 'tablet'},
        {'name': 'Levotiroxina', 'strength': '50mcg', 'form': 'tablet'},
        {'name': 'Insulina Glargina', 'strength': '100U/ml', 'form': 'injection'},
        {'name': 'Salbutamol', 'strength': '100mcg', 'form': 'inhaler'},
        {'name': 'Diclofenac', 'strength': '1%', 'form': 'cream'},
        {'name': 'Xarope para Tosse', 'strength': '15mg/5ml', 'form': 'liquid'},
    ]

    @classmethod
    def _get_counter(cls) -> int:
        cls._counter += 1
        return cls._counter

    @classmethod
    def definition(cls) -> Dict[str, Any]:
        """Default medication state."""
        med = random.choice(cls.MEDICATIONS)
        counter = cls._get_counter()

        return {
            'name': f"{med['name']} {counter}",
            'description': f"Medicamento para tratamento geral",
            'dosage_form': med['form'],
            'strength': med['strength'],
            'manufacturer': random.choice(['Lab A', 'Lab B', 'Lab C', 'Genérico']),
            'instructions': 'Tomar conforme indicação médica.',
            'side_effects': 'Consulte a bula para efeitos secundários.',
            'is_active': True,
        }

    @classmethod
    def paracetamol(cls) -> Dict[str, Any]:
        """State for Paracetamol."""
        return {
            'name': 'Paracetamol',
            'strength': '500mg',
            'dosage_form': 'tablet',
            'instructions': 'Tomar 1 comprimido a cada 8 horas. Não exceder 4g por dia.',
        }

    @classmethod
    def insulin(cls) -> Dict[str, Any]:
        """State for Insulin."""
        return {
            'name': 'Insulina Glargina',
            'strength': '100U/ml',
            'dosage_form': 'injection',
            'instructions': 'Administrar por via subcutânea uma vez ao dia.',
        }
