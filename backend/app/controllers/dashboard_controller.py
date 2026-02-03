from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User


class DashboardController:
    @staticmethod
    @jwt_required()
    def admin_dashboard():
        """Admin dashboard data."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403

        # Get statistics
        total_users = User.query.count()
        total_clinicians = User.query.filter_by(role='clinician').count()
        total_patients = User.query.filter_by(role='patient').count()

        return jsonify({
            'message': 'Admin Dashboard',
            'user': user.to_dict(),
            'stats': {
                'total_users': total_users,
                'total_clinicians': total_clinicians,
                'total_patients': total_patients,
            }
        }), 200

    @staticmethod
    @jwt_required()
    def clinician_dashboard():
        """Clinician dashboard data."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_clinician():
            return jsonify({'error': 'Unauthorized'}), 403

        # Get patient count (clinicians can see patients)
        total_patients = User.query.filter_by(role='patient').count()

        return jsonify({
            'message': 'Clinician Dashboard',
            'user': user.to_dict(),
            'stats': {
                'total_patients': total_patients,
            }
        }), 200

    @staticmethod
    @jwt_required()
    def patient_dashboard():
        """Patient dashboard data."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_patient():
            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify({
            'message': 'Patient Dashboard',
            'user': user.to_dict(),
        }), 200
