"""
MedicationSchedule model - Specific times to take medication.
Part of a Prescription, set by Clinicians.
"""

from app import db
from datetime import datetime, time


class MedicationSchedule(db.Model):
    __tablename__ = 'medication_schedules'

    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.id'), nullable=False)

    # Schedule details
    time = db.Column(db.Time, nullable=False)  # Time of day to take medication
    dosage = db.Column(db.String(100), nullable=True)  # Override prescription dosage if needed
    label = db.Column(db.String(50), nullable=True)  # e.g., "Manhã", "Almoço", "Noite"

    # Days of week (for weekly/custom schedules)
    monday = db.Column(db.Boolean, default=True)
    tuesday = db.Column(db.Boolean, default=True)
    wednesday = db.Column(db.Boolean, default=True)
    thursday = db.Column(db.Boolean, default=True)
    friday = db.Column(db.Boolean, default=True)
    saturday = db.Column(db.Boolean, default=True)
    sunday = db.Column(db.Boolean, default=True)

    # Reminder settings
    reminder_enabled = db.Column(db.Boolean, default=True)
    reminder_minutes_before = db.Column(db.Integer, default=15)  # Minutes before scheduled time

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    prescription = db.relationship('Prescription', back_populates='schedules')

    # Time labels
    TIME_LABELS = [
        ('morning', 'Manhã'),
        ('lunch', 'Almoço'),
        ('afternoon', 'Tarde'),
        ('dinner', 'Jantar'),
        ('night', 'Noite'),
        ('bedtime', 'Ao deitar'),
        ('custom', 'Personalizado'),
    ]

    def is_scheduled_for_day(self, weekday):
        """Check if scheduled for a specific weekday (0=Monday, 6=Sunday)."""
        days = [
            self.monday, self.tuesday, self.wednesday, self.thursday,
            self.friday, self.saturday, self.sunday
        ]
        return days[weekday]

    def get_scheduled_days(self):
        """Get list of scheduled days."""
        days = []
        if self.monday:
            days.append('monday')
        if self.tuesday:
            days.append('tuesday')
        if self.wednesday:
            days.append('wednesday')
        if self.thursday:
            days.append('thursday')
        if self.friday:
            days.append('friday')
        if self.saturday:
            days.append('saturday')
        if self.sunday:
            days.append('sunday')
        return days

    def to_dict(self):
        return {
            'id': self.id,
            'prescription_id': self.prescription_id,
            'time': self.time.strftime('%H:%M') if self.time else None,
            'dosage': self.dosage,
            'label': self.label,
            'days': {
                'monday': self.monday,
                'tuesday': self.tuesday,
                'wednesday': self.wednesday,
                'thursday': self.thursday,
                'friday': self.friday,
                'saturday': self.saturday,
                'sunday': self.sunday,
            },
            'scheduled_days': self.get_scheduled_days(),
            'reminder_enabled': self.reminder_enabled,
            'reminder_minutes_before': self.reminder_minutes_before,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<MedicationSchedule {self.id} - {self.time}>'
