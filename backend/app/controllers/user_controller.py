"""
UserController - Admin management of users.
"""

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User, UserRole


class UserController:
    @staticmethod
    @jwt_required()
    def index():
        """List all users (Admin only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        role = request.args.get('role', type=str)
        search = request.args.get('search', '', type=str)
        active_only = request.args.get('active_only', 'false', type=str).lower() == 'true'

        query = User.query

        if role:
            query = query.filter_by(role=role)

        if active_only:
            query = query.filter_by(is_active=True)

        if search:
            query = query.filter(
                db.or_(
                    User.name.ilike(f'%{search}%'),
                    User.email.ilike(f'%{search}%')
                )
            )

        query = query.order_by(User.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'users': [u.to_dict() for u in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
        }), 200

    @staticmethod
    @jwt_required()
    def show(user_id_param):
        """Get single user (Admin only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        target_user = User.query.get(user_id_param)
        if not target_user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'user': target_user.to_dict()}), 200

    @staticmethod
    @jwt_required()
    def store():
        """Create new user (Admin only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        data = request.get_json()

        # Validation
        required_fields = ['name', 'email', 'password', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Check role is valid
        if data['role'] not in UserRole.all():
            return jsonify({'error': 'Invalid role'}), 400

        # Check email is unique
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400

        new_user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            role=data['role'],
            is_active=data.get('is_active', True),
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': 'User created successfully',
            'user': new_user.to_dict()
        }), 201

    @staticmethod
    @jwt_required()
    def update(user_id_param):
        """Update user (Admin only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        target_user = User.query.get(user_id_param)
        if not target_user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()

        # Update fields
        if 'name' in data:
            target_user.name = data['name']

        if 'email' in data:
            # Check email is unique
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != target_user.id:
                return jsonify({'error': 'Email already exists'}), 400
            target_user.email = data['email']

        if 'password' in data and data['password']:
            target_user.password = data['password']

        if 'role' in data:
            if data['role'] not in UserRole.all():
                return jsonify({'error': 'Invalid role'}), 400
            target_user.role = data['role']

        if 'is_active' in data:
            target_user.is_active = data['is_active']

        db.session.commit()

        return jsonify({
            'message': 'User updated successfully',
            'user': target_user.to_dict()
        }), 200

    @staticmethod
    @jwt_required()
    def destroy(user_id_param):
        """Deactivate user (Admin only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        target_user = User.query.get(user_id_param)
        if not target_user:
            return jsonify({'error': 'User not found'}), 404

        # Prevent self-delete
        if target_user.id == user.id:
            return jsonify({'error': 'Cannot deactivate yourself'}), 400

        # Soft delete
        target_user.is_active = False
        db.session.commit()

        return jsonify({'message': 'User deactivated successfully'}), 200

    @staticmethod
    @jwt_required()
    def activate(user_id_param):
        """Activate user (Admin only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        target_user = User.query.get(user_id_param)
        if not target_user:
            return jsonify({'error': 'User not found'}), 404

        target_user.is_active = True
        db.session.commit()

        return jsonify({
            'message': 'User activated successfully',
            'user': target_user.to_dict()
        }), 200

    @staticmethod
    @jwt_required()
    def get_roles():
        """Get list of available roles."""
        return jsonify({'roles': UserRole.all()}), 200

    @staticmethod
    @jwt_required()
    def get_stats():
        """Get user statistics (Admin only)."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        total = User.query.count()
        active = User.query.filter_by(is_active=True).count()
        admins = User.query.filter_by(role='admin').count()
        clinicians = User.query.filter_by(role='clinician').count()
        patients = User.query.filter_by(role='patient').count()

        return jsonify({
            'stats': {
                'total': total,
                'active': active,
                'inactive': total - active,
                'by_role': {
                    'admin': admins,
                    'clinician': clinicians,
                    'patient': patients,
                }
            }
        }), 200
