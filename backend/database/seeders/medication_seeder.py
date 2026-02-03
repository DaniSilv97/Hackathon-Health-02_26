"""
Medication Seeder - Populate database with common medications.
"""

from database.seeders.base_seeder import Seeder
from app.models.medication import Medication
from app import db


class MedicationSeeder(Seeder):
    """Seeder for creating common medications catalog."""

    MEDICATIONS = [
        {
            'name': 'Paracetamol',
            'description': 'Analgésico e antipirético para dor e febre',
            'dosage_form': 'tablet',
            'strength': '500mg',
            'manufacturer': 'Genérico',
            'instructions': 'Tomar 1 comprimido a cada 6-8 horas. Máximo 4g/dia.',
            'side_effects': 'Raramente causa efeitos. Em doses elevadas pode afetar o fígado.',
        },
        {
            'name': 'Ibuprofeno',
            'description': 'Anti-inflamatório não esteroide (AINE)',
            'dosage_form': 'tablet',
            'strength': '400mg',
            'manufacturer': 'Genérico',
            'instructions': 'Tomar 1 comprimido a cada 8 horas, com alimentos.',
            'side_effects': 'Pode causar irritação gástrica, náuseas.',
        },
        {
            'name': 'Amoxicilina',
            'description': 'Antibiótico de largo espectro',
            'dosage_form': 'capsule',
            'strength': '500mg',
            'manufacturer': 'Genérico',
            'instructions': 'Tomar 1 cápsula a cada 8 horas durante 7-10 dias.',
            'side_effects': 'Pode causar diarreia, náuseas, reações alérgicas.',
        },
        {
            'name': 'Omeprazol',
            'description': 'Inibidor da bomba de protões para problemas gástricos',
            'dosage_form': 'capsule',
            'strength': '20mg',
            'manufacturer': 'Genérico',
            'instructions': 'Tomar 1 cápsula em jejum, 30 min antes do pequeno-almoço.',
            'side_effects': 'Pode causar dor de cabeça, náuseas.',
        },
        {
            'name': 'Metformina',
            'description': 'Antidiabético oral para diabetes tipo 2',
            'dosage_form': 'tablet',
            'strength': '850mg',
            'manufacturer': 'Genérico',
            'instructions': 'Tomar com as refeições para reduzir efeitos gastrointestinais.',
            'side_effects': 'Pode causar náuseas, diarreia no início do tratamento.',
        },
        {
            'name': 'Losartan',
            'description': 'Anti-hipertensor (antagonista dos recetores da angiotensina)',
            'dosage_form': 'tablet',
            'strength': '50mg',
            'manufacturer': 'Genérico',
            'instructions': 'Tomar 1 comprimido por dia, de preferência à mesma hora.',
            'side_effects': 'Pode causar tonturas, especialmente no início.',
        },
        {
            'name': 'Atorvastatina',
            'description': 'Estatina para controlo do colesterol',
            'dosage_form': 'tablet',
            'strength': '20mg',
            'manufacturer': 'Genérico',
            'instructions': 'Tomar 1 comprimido ao deitar.',
            'side_effects': 'Pode causar dores musculares.',
        },
        {
            'name': 'Levotiroxina',
            'description': 'Hormona tiroideia sintética',
            'dosage_form': 'tablet',
            'strength': '50mcg',
            'manufacturer': 'Genérico',
            'instructions': 'Tomar em jejum, 30-60 min antes do pequeno-almoço.',
            'side_effects': 'Em doses corretas raramente causa efeitos.',
        },
        {
            'name': 'Salbutamol Inalador',
            'description': 'Broncodilatador para asma e DPOC',
            'dosage_form': 'inhaler',
            'strength': '100mcg/dose',
            'manufacturer': 'Genérico',
            'instructions': 'Inalar 1-2 puffs quando necessário. Máximo 8 puffs/dia.',
            'side_effects': 'Pode causar tremores, palpitações.',
        },
        {
            'name': 'Diclofenac Gel',
            'description': 'Anti-inflamatório tópico',
            'dosage_form': 'cream',
            'strength': '1%',
            'manufacturer': 'Genérico',
            'instructions': 'Aplicar na zona afetada 3-4 vezes ao dia.',
            'side_effects': 'Pode causar irritação local.',
        },
    ]

    @classmethod
    def run(cls) -> None:
        """Run the medication seeds."""
        for med_data in cls.MEDICATIONS:
            # Check if medication already exists
            existing = Medication.query.filter_by(name=med_data['name']).first()
            if not existing:
                medication = Medication(**med_data, is_active=True)
                db.session.add(medication)
                print(f"    Created: {med_data['name']}")

        db.session.commit()
        print(f'    Total medications: {Medication.query.count()}')
