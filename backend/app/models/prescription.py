"""
Prescription model - Links patients to medications.
Created by Clinicians for Patients.
"""

from app import db
from datetime import datetime, date


class Prescription(db.Model):
    __tablename__ = 'prescriptions'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    clinician_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable=False)

    # Prescription details
    dosage = db.Column(db.String(100), nullable=False)  # e.g., "1 comprimido", "5ml"
    frequency = db.Column(db.String(50), nullable=False)  # e.g., "daily", "twice_daily", "weekly"
    instructions = db.Column(db.Text, nullable=True)  # Specific instructions
    notes = db.Column(db.Text, nullable=True)  # Clinician notes

    # Duration
    start_date = db.Column(db.Date, nullable=False, default=date.today)
    end_date = db.Column(db.Date, nullable=True)  # Null = indefinite

    # Status
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = db.relationship('User', foreign_keys=[patient_id], backref='prescriptions_as_patient')
    clinician = db.relationship('User', foreign_keys=[clinician_id], backref='prescriptions_as_clinician')
    medication = db.relationship('Medication', back_populates='prescriptions')
    schedules = db.relationship('MedicationSchedule', back_populates='prescription', lazy='dynamic',
                                cascade='all, delete-orphan')
    logs = db.relationship('MedicationLog', back_populates='prescription', lazy='dynamic',
                           cascade='all, delete-orphan')

    # Frequency options
    FREQUENCIES = [
        ('once_daily', 'Uma vez ao dia'),
        ('twice_daily', 'Duas vezes ao dia'),
        ('three_times_daily', 'Três vezes ao dia'),
        ('four_times_daily', 'Quatro vezes ao dia'),
        ('every_8_hours', 'A cada 8 horas'),
        ('every_12_hours', 'A cada 12 horas'),
        ('weekly', 'Semanalmente'),
        ('as_needed', 'Quando necessário'),
        ('custom', 'Personalizado'),
    ]

    def is_current(self):
        """Check if prescription is currently active."""
        today = date.today()
        if not self.is_active:
            return False
        if self.start_date > today:
            return False
        if self.end_date and self.end_date < today:
            return False
        return True

    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'patient_id': self.patient_id,
            'clinician_id': self.clinician_id,
            'medication_id': self.medication_id,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'instructions': self.instructions,
            'notes': self.notes,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'is_current': self.is_current(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_relations:
            data['patient'] = self.patient.to_dict() if self.patient else None
            data['clinician'] = self.clinician.to_dict() if self.clinician else None
            data['medication'] = self.medication.to_dict() if self.medication else None
            data['schedules'] = [s.to_dict() for s in self.schedules.all()]

        return data

    def __repr__(self):
        return f'<Prescription {self.id} - Patient:{self.patient_id} Med:{self.medication_id}>'
