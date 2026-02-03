"""
Medication model - Catalog of available medications.
Managed by Admin users.
"""

from app import db
from datetime import datetime


class Medication(db.Model):
    __tablename__ = 'medications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    dosage_form = db.Column(db.String(50), nullable=False)  # tablet, capsule, liquid, injection
    strength = db.Column(db.String(50), nullable=True)  # e.g., "500mg", "10ml"
    manufacturer = db.Column(db.String(200), nullable=True)
    instructions = db.Column(db.Text, nullable=True)  # General instructions
    side_effects = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    prescriptions = db.relationship('Prescription', back_populates='medication', lazy='dynamic')

    # Dosage form options
    DOSAGE_FORMS = [
        ('tablet', 'Comprimido'),
        ('capsule', 'Cápsula'),
        ('liquid', 'Líquido'),
        ('injection', 'Injeção'),
        ('cream', 'Creme'),
        ('drops', 'Gotas'),
        ('inhaler', 'Inalador'),
        ('patch', 'Adesivo'),
        ('suppository', 'Supositório'),
        ('other', 'Outro'),
    ]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'dosage_form': self.dosage_form,
            'strength': self.strength,
            'manufacturer': self.manufacturer,
            'instructions': self.instructions,
            'side_effects': self.side_effects,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<Medication {self.name}>'
