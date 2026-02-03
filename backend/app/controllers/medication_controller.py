"""
MedicationController - Admin management of medication catalog.
"""

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.medication import Medication


class MedicationController:
    @staticmethod
    @jwt_required()
    def index():
        """List all medications (paginated)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str)
        active_only = request.args.get('active_only', 'true', type=str).lower() == 'true'

        query = Medication.query

        if active_only:
            query = query.filter_by(is_active=True)

        if search:
            query = query.filter(Medication.name.ilike(f'%{search}%'))

        query = query.order_by(Medication.name)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'medications': [m.to_dict() for m in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
        }), 200

    @staticmethod
    @jwt_required()
    def show(medication_id):
        """Get single medication."""
        medication = Medication.query.get(medication_id)

        if not medication:
            return jsonify({'error': 'Medication not found'}), 404

        return jsonify({'medication': medication.to_dict()}), 200

    @staticmethod
    @jwt_required()
    def store():
        """Create new medication (Admin only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        data = request.get_json()

        # Validation
        required_fields = ['name', 'dosage_form']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        medication = Medication(
            name=data['name'],
            description=data.get('description'),
            dosage_form=data['dosage_form'],
            strength=data.get('strength'),
            manufacturer=data.get('manufacturer'),
            instructions=data.get('instructions'),
            side_effects=data.get('side_effects'),
            is_active=data.get('is_active', True),
        )

        db.session.add(medication)
        db.session.commit()

        return jsonify({
            'message': 'Medication created successfully',
            'medication': medication.to_dict()
        }), 201

    @staticmethod
    @jwt_required()
    def update(medication_id):
        """Update medication (Admin only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        medication = Medication.query.get(medication_id)
        if not medication:
            return jsonify({'error': 'Medication not found'}), 404

        data = request.get_json()

        # Update fields
        if 'name' in data:
            medication.name = data['name']
        if 'description' in data:
            medication.description = data['description']
        if 'dosage_form' in data:
            medication.dosage_form = data['dosage_form']
        if 'strength' in data:
            medication.strength = data['strength']
        if 'manufacturer' in data:
            medication.manufacturer = data['manufacturer']
        if 'instructions' in data:
            medication.instructions = data['instructions']
        if 'side_effects' in data:
            medication.side_effects = data['side_effects']
        if 'is_active' in data:
            medication.is_active = data['is_active']

        db.session.commit()

        return jsonify({
            'message': 'Medication updated successfully',
            'medication': medication.to_dict()
        }), 200

    @staticmethod
    @jwt_required()
    def destroy(medication_id):
        """Delete medication (Admin only) - soft delete."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        medication = Medication.query.get(medication_id)
        if not medication:
            return jsonify({'error': 'Medication not found'}), 404

        # Soft delete - just deactivate
        medication.is_active = False
        db.session.commit()

        return jsonify({'message': 'Medication deactivated successfully'}), 200

    @staticmethod
    @jwt_required()
    def get_dosage_forms():
        """Get list of available dosage forms."""
        return jsonify({'dosage_forms': Medication.DOSAGE_FORMS}), 200
