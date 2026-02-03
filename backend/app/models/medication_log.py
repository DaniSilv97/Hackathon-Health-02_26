"""
MedicationLog model - Records when patients take their medication.
The checkbox tracking for the calendar.
"""

from app import db
from datetime import datetime, date, time


class MedicationLog(db.Model):
    __tablename__ = 'medication_logs'

    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('medication_schedules.id'), nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Log details
    scheduled_date = db.Column(db.Date, nullable=False)  # The date the medication was scheduled
    scheduled_time = db.Column(db.Time, nullable=True)  # The time it was scheduled
    taken_at = db.Column(db.DateTime, nullable=True)  # When actually taken (null = not taken yet)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, taken, skipped, missed

    # Additional info
    notes = db.Column(db.Text, nullable=True)  # Patient notes
    skipped_reason = db.Column(db.String(200), nullable=True)  # If skipped, why

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    prescription = db.relationship('Prescription', back_populates='logs')
    schedule = db.relationship('MedicationSchedule', backref='logs')
    patient = db.relationship('User', backref='medication_logs')

    # Status options
    STATUSES = [
        ('pending', 'Pendente'),
        ('taken', 'Tomado'),
        ('skipped', 'Ignorado'),
        ('missed', 'Perdido'),
    ]

    def mark_as_taken(self, taken_at=None, notes=None):
        """Mark medication as taken."""
        self.status = 'taken'
        self.taken_at = taken_at or datetime.utcnow()
        if notes:
            self.notes = notes
        db.session.commit()

    def mark_as_skipped(self, reason=None):
        """Mark medication as skipped."""
        self.status = 'skipped'
        self.skipped_reason = reason
        db.session.commit()

    def mark_as_missed(self):
        """Mark medication as missed (auto-marked when time passes)."""
        self.status = 'missed'
        db.session.commit()

    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'prescription_id': self.prescription_id,
            'schedule_id': self.schedule_id,
            'patient_id': self.patient_id,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'scheduled_time': self.scheduled_time.strftime('%H:%M') if self.scheduled_time else None,
            'taken_at': self.taken_at.isoformat() if self.taken_at else None,
            'status': self.status,
            'notes': self.notes,
            'skipped_reason': self.skipped_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        if include_relations:
            data['prescription'] = self.prescription.to_dict(include_relations=True) if self.prescription else None

        return data

    @classmethod
    def get_or_create_for_schedule(cls, prescription_id, schedule_id, patient_id, scheduled_date, scheduled_time):
        """Get existing log or create new one for a specific schedule."""
        log = cls.query.filter_by(
            prescription_id=prescription_id,
            schedule_id=schedule_id,
            scheduled_date=scheduled_date
        ).first()

        if not log:
            log = cls(
                prescription_id=prescription_id,
                schedule_id=schedule_id,
                patient_id=patient_id,
                scheduled_date=scheduled_date,
                scheduled_time=scheduled_time,
                status='pending'
            )
            db.session.add(log)
            db.session.commit()

        return log

    def __repr__(self):
        return f'<MedicationLog {self.id} - {self.scheduled_date} {self.status}>'
