"""
CalendarController - Patient medication calendar and logging.
"""

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.prescription import Prescription
from app.models.medication_schedule import MedicationSchedule
from app.models.medication_log import MedicationLog
from datetime import datetime, date, timedelta


class CalendarController:
    @staticmethod
    @jwt_required()
    def get_calendar():
        """Get medication calendar for a date range."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        # Get date range from query params
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = date.today()

        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = start_date + timedelta(days=7)

        # Get patient_id (for clinicians viewing patient calendar)
        patient_id = request.args.get('patient_id', type=int)

        if user.is_patient():
            patient_id = user.id
        elif not patient_id and (user.is_clinician() or user.is_admin()):
            return jsonify({'error': 'patient_id required'}), 400

        # Get active prescriptions for the patient
        prescriptions = Prescription.query.filter(
            Prescription.patient_id == patient_id,
            Prescription.is_active == True,
            Prescription.start_date <= end_date,
            db.or_(
                Prescription.end_date.is_(None),
                Prescription.end_date >= start_date
            )
        ).all()

        # Build calendar data
        calendar = {}
        current_date = start_date

        while current_date <= end_date:
            day_key = current_date.isoformat()
            calendar[day_key] = {
                'date': day_key,
                'weekday': current_date.weekday(),
                'medications': []
            }

            for prescription in prescriptions:
                # Check if prescription is active for this date
                if prescription.start_date > current_date:
                    continue
                if prescription.end_date and prescription.end_date < current_date:
                    continue

                for schedule in prescription.schedules.filter_by(is_active=True).all():
                    # Check if scheduled for this day of week
                    if not schedule.is_scheduled_for_day(current_date.weekday()):
                        continue

                    # Get or create log entry
                    log = MedicationLog.query.filter_by(
                        prescription_id=prescription.id,
                        schedule_id=schedule.id,
                        scheduled_date=current_date
                    ).first()

                    med_entry = {
                        'prescription_id': prescription.id,
                        'schedule_id': schedule.id,
                        'medication': prescription.medication.to_dict(),
                        'dosage': schedule.dosage or prescription.dosage,
                        'time': schedule.time.strftime('%H:%M'),
                        'label': schedule.label,
                        'instructions': prescription.instructions,
                        'status': log.status if log else 'pending',
                        'log_id': log.id if log else None,
                        'taken_at': log.taken_at.isoformat() if log and log.taken_at else None,
                    }

                    calendar[day_key]['medications'].append(med_entry)

            # Sort medications by time
            calendar[day_key]['medications'].sort(key=lambda x: x['time'])

            current_date += timedelta(days=1)

        return jsonify({
            'calendar': calendar,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        }), 200

    @staticmethod
    @jwt_required()
    def get_today():
        """Get today's medications for the patient."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_patient():
            return jsonify({'error': 'Unauthorized - Patient only'}), 403

        today = date.today()

        # Get active prescriptions
        prescriptions = Prescription.query.filter(
            Prescription.patient_id == user.id,
            Prescription.is_active == True,
            Prescription.start_date <= today,
            db.or_(
                Prescription.end_date.is_(None),
                Prescription.end_date >= today
            )
        ).all()

        medications = []
        for prescription in prescriptions:
            for schedule in prescription.schedules.filter_by(is_active=True).all():
                if not schedule.is_scheduled_for_day(today.weekday()):
                    continue

                # Get or create log
                log = MedicationLog.get_or_create_for_schedule(
                    prescription_id=prescription.id,
                    schedule_id=schedule.id,
                    patient_id=user.id,
                    scheduled_date=today,
                    scheduled_time=schedule.time
                )

                medications.append({
                    'log_id': log.id,
                    'prescription_id': prescription.id,
                    'schedule_id': schedule.id,
                    'medication': prescription.medication.to_dict(),
                    'dosage': schedule.dosage or prescription.dosage,
                    'time': schedule.time.strftime('%H:%M'),
                    'label': schedule.label,
                    'instructions': prescription.instructions,
                    'status': log.status,
                    'taken_at': log.taken_at.isoformat() if log.taken_at else None,
                })

        # Sort by time
        medications.sort(key=lambda x: x['time'])

        return jsonify({
            'date': today.isoformat(),
            'medications': medications,
            'total': len(medications),
            'taken': sum(1 for m in medications if m['status'] == 'taken'),
            'pending': sum(1 for m in medications if m['status'] == 'pending'),
        }), 200

    @staticmethod
    @jwt_required()
    def mark_taken(log_id):
        """Mark medication as taken."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_patient():
            return jsonify({'error': 'Unauthorized - Patient only'}), 403

        log = MedicationLog.query.get(log_id)
        if not log:
            return jsonify({'error': 'Log not found'}), 404

        if log.patient_id != user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json() or {}

        log.mark_as_taken(
            taken_at=datetime.utcnow(),
            notes=data.get('notes')
        )

        return jsonify({
            'message': 'Medication marked as taken',
            'log': log.to_dict()
        }), 200

    @staticmethod
    @jwt_required()
    def mark_skipped(log_id):
        """Mark medication as skipped."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_patient():
            return jsonify({'error': 'Unauthorized - Patient only'}), 403

        log = MedicationLog.query.get(log_id)
        if not log:
            return jsonify({'error': 'Log not found'}), 404

        if log.patient_id != user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json() or {}

        log.mark_as_skipped(reason=data.get('reason'))

        return jsonify({
            'message': 'Medication marked as skipped',
            'log': log.to_dict()
        }), 200

    @staticmethod
    @jwt_required()
    def undo_log(log_id):
        """Undo medication log (reset to pending)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_patient():
            return jsonify({'error': 'Unauthorized - Patient only'}), 403

        log = MedicationLog.query.get(log_id)
        if not log:
            return jsonify({'error': 'Log not found'}), 404

        if log.patient_id != user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        log.status = 'pending'
        log.taken_at = None
        log.skipped_reason = None
        db.session.commit()

        return jsonify({
            'message': 'Log reset to pending',
            'log': log.to_dict()
        }), 200

    @staticmethod
    @jwt_required()
    def get_history():
        """Get medication history for patient."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        patient_id = request.args.get('patient_id', type=int)
        if user.is_patient():
            patient_id = user.id
        elif not patient_id:
            return jsonify({'error': 'patient_id required'}), 400

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)

        query = MedicationLog.query.filter_by(patient_id=patient_id)
        query = query.order_by(MedicationLog.scheduled_date.desc(), MedicationLog.scheduled_time.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'logs': [log.to_dict(include_relations=True) for log in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
        }), 200

    @staticmethod
    @jwt_required()
    def get_stats():
        """Get medication adherence statistics."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        patient_id = request.args.get('patient_id', type=int)
        if user.is_patient():
            patient_id = user.id
        elif not patient_id:
            return jsonify({'error': 'patient_id required'}), 400

        # Get stats for last 30 days
        start_date = date.today() - timedelta(days=30)

        logs = MedicationLog.query.filter(
            MedicationLog.patient_id == patient_id,
            MedicationLog.scheduled_date >= start_date
        ).all()

        total = len(logs)
        taken = sum(1 for log in logs if log.status == 'taken')
        skipped = sum(1 for log in logs if log.status == 'skipped')
        missed = sum(1 for log in logs if log.status == 'missed')
        pending = sum(1 for log in logs if log.status == 'pending')

        adherence_rate = (taken / total * 100) if total > 0 else 0

        return jsonify({
            'period': {
                'start': start_date.isoformat(),
                'end': date.today().isoformat(),
            },
            'stats': {
                'total': total,
                'taken': taken,
                'skipped': skipped,
                'missed': missed,
                'pending': pending,
                'adherence_rate': round(adherence_rate, 1),
            }
        }), 200
