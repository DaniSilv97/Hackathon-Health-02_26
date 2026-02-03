"""
PrescriptionController - Clinician management of patient prescriptions.
"""

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.medication import Medication
from app.models.prescription import Prescription
from app.models.medication_schedule import MedicationSchedule
from datetime import datetime, date, time


class PrescriptionController:
    @staticmethod
    @jwt_required()
    def index():
        """List prescriptions (filtered by role)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        patient_id = request.args.get('patient_id', type=int)
        active_only = request.args.get('active_only', 'true', type=str).lower() == 'true'

        query = Prescription.query

        # Role-based filtering
        if user.is_patient():
            query = query.filter_by(patient_id=user.id)
        elif user.is_clinician():
            if patient_id:
                query = query.filter_by(patient_id=patient_id, clinician_id=user.id)
            else:
                query = query.filter_by(clinician_id=user.id)
        # Admin can see all

        if active_only:
            query = query.filter_by(is_active=True)

        query = query.order_by(Prescription.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'prescriptions': [p.to_dict(include_relations=True) for p in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
        }), 200

    @staticmethod
    @jwt_required()
    def show(prescription_id):
        """Get single prescription."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        prescription = Prescription.query.get(prescription_id)
        if not prescription:
            return jsonify({'error': 'Prescription not found'}), 404

        # Check access
        if user.is_patient() and prescription.patient_id != user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        if user.is_clinician() and prescription.clinician_id != user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify({'prescription': prescription.to_dict(include_relations=True)}), 200

    @staticmethod
    @jwt_required()
    def store():
        """Create new prescription (Clinician only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_clinician():
            return jsonify({'error': 'Unauthorized - Clinician only'}), 403

        data = request.get_json()

        # Validation
        required_fields = ['patient_id', 'medication_id', 'dosage', 'frequency']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Verify patient exists and is a patient
        patient = User.query.get(data['patient_id'])
        if not patient or not patient.is_patient():
            return jsonify({'error': 'Invalid patient'}), 400

        # Verify medication exists
        medication = Medication.query.get(data['medication_id'])
        if not medication or not medication.is_active:
            return jsonify({'error': 'Invalid medication'}), 400

        # Parse dates
        start_date = date.today()
        if data.get('start_date'):
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()

        end_date = None
        if data.get('end_date'):
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()

        prescription = Prescription(
            patient_id=data['patient_id'],
            clinician_id=user.id,
            medication_id=data['medication_id'],
            dosage=data['dosage'],
            frequency=data['frequency'],
            instructions=data.get('instructions'),
            notes=data.get('notes'),
            start_date=start_date,
            end_date=end_date,
            is_active=True,
        )

        db.session.add(prescription)
        db.session.flush()  # Get prescription ID

        # Add schedules if provided
        schedules_data = data.get('schedules', [])
        for schedule_data in schedules_data:
            schedule_time = datetime.strptime(schedule_data['time'], '%H:%M').time()
            schedule = MedicationSchedule(
                prescription_id=prescription.id,
                time=schedule_time,
                dosage=schedule_data.get('dosage'),
                label=schedule_data.get('label'),
                monday=schedule_data.get('monday', True),
                tuesday=schedule_data.get('tuesday', True),
                wednesday=schedule_data.get('wednesday', True),
                thursday=schedule_data.get('thursday', True),
                friday=schedule_data.get('friday', True),
                saturday=schedule_data.get('saturday', True),
                sunday=schedule_data.get('sunday', True),
                reminder_enabled=schedule_data.get('reminder_enabled', True),
                reminder_minutes_before=schedule_data.get('reminder_minutes_before', 15),
            )
            db.session.add(schedule)

        db.session.commit()

        return jsonify({
            'message': 'Prescription created successfully',
            'prescription': prescription.to_dict(include_relations=True)
        }), 201

    @staticmethod
    @jwt_required()
    def update(prescription_id):
        """Update prescription (Clinician only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_clinician():
            return jsonify({'error': 'Unauthorized - Clinician only'}), 403

        prescription = Prescription.query.get(prescription_id)
        if not prescription:
            return jsonify({'error': 'Prescription not found'}), 404

        if prescription.clinician_id != user.id and not user.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()

        # Update fields
        if 'dosage' in data:
            prescription.dosage = data['dosage']
        if 'frequency' in data:
            prescription.frequency = data['frequency']
        if 'instructions' in data:
            prescription.instructions = data['instructions']
        if 'notes' in data:
            prescription.notes = data['notes']
        if 'start_date' in data:
            prescription.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data:
            prescription.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data['end_date'] else None
        if 'is_active' in data:
            prescription.is_active = data['is_active']

        db.session.commit()

        return jsonify({
            'message': 'Prescription updated successfully',
            'prescription': prescription.to_dict(include_relations=True)
        }), 200

    @staticmethod
    @jwt_required()
    def destroy(prescription_id):
        """Deactivate prescription (Clinician only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_clinician():
            return jsonify({'error': 'Unauthorized - Clinician only'}), 403

        prescription = Prescription.query.get(prescription_id)
        if not prescription:
            return jsonify({'error': 'Prescription not found'}), 404

        if prescription.clinician_id != user.id and not user.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403

        # Soft delete
        prescription.is_active = False
        db.session.commit()

        return jsonify({'message': 'Prescription deactivated successfully'}), 200

    @staticmethod
    @jwt_required()
    def add_schedule(prescription_id):
        """Add schedule to prescription (Clinician only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_clinician():
            return jsonify({'error': 'Unauthorized - Clinician only'}), 403

        prescription = Prescription.query.get(prescription_id)
        if not prescription:
            return jsonify({'error': 'Prescription not found'}), 404

        if prescription.clinician_id != user.id and not user.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()

        if not data.get('time'):
            return jsonify({'error': 'time is required'}), 400

        schedule_time = datetime.strptime(data['time'], '%H:%M').time()

        schedule = MedicationSchedule(
            prescription_id=prescription.id,
            time=schedule_time,
            dosage=data.get('dosage'),
            label=data.get('label'),
            monday=data.get('monday', True),
            tuesday=data.get('tuesday', True),
            wednesday=data.get('wednesday', True),
            thursday=data.get('thursday', True),
            friday=data.get('friday', True),
            saturday=data.get('saturday', True),
            sunday=data.get('sunday', True),
            reminder_enabled=data.get('reminder_enabled', True),
            reminder_minutes_before=data.get('reminder_minutes_before', 15),
        )

        db.session.add(schedule)
        db.session.commit()

        return jsonify({
            'message': 'Schedule added successfully',
            'schedule': schedule.to_dict()
        }), 201

    @staticmethod
    @jwt_required()
    def get_patients():
        """Get list of patients (for Clinicians)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not (user.is_clinician() or user.is_admin()):
            return jsonify({'error': 'Unauthorized'}), 403

        patients = User.query.filter_by(role='patient', is_active=True).all()

        return jsonify({
            'patients': [p.to_dict() for p in patients]
        }), 200

    @staticmethod
    @jwt_required()
    def get_frequencies():
        """Get list of available frequencies."""
        return jsonify({'frequencies': Prescription.FREQUENCIES}), 200
