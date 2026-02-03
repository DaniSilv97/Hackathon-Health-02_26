from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app import db
from app.models.user import User, UserRole


class AuthController:
    @staticmethod
    def login():
        """Handle user login."""
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401

        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401

        # Create tokens
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'role': user.role}
        )
        refresh_token = create_refresh_token(identity=user.id)

        # Determine redirect based on role
        redirect_map = {
            UserRole.ADMIN: '/admin/dashboard',
            UserRole.CLINICIAN: '/clinician/dashboard',
            UserRole.PATIENT: '/patient/dashboard',
        }

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict(),
            'redirect': redirect_map.get(user.role, '/dashboard')
        }), 200

    @staticmethod
    def register():
        """Handle user registration."""
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', UserRole.PATIENT)

        if not all([name, email, password]):
            return jsonify({'error': 'Name, email and password are required'}), 400

        if role not in UserRole.all():
            return jsonify({'error': 'Invalid role'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409

        user = User(name=name, email=email, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': 'Registration successful',
            'user': user.to_dict()
        }), 201

    @staticmethod
    @jwt_required()
    def logout():
        """Handle user logout."""
        # In a real application, you might want to blacklist the token
        return jsonify({'message': 'Logout successful'}), 200

    @staticmethod
    @jwt_required()
    def me():
        """Get current authenticated user."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'user': user.to_dict()}), 200

    @staticmethod
    @jwt_required(refresh=True)
    def refresh():
        """Refresh access token."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        access_token = create_access_token(
            identity=user.id,
            additional_claims={'role': user.role}
        )

        return jsonify({'access_token': access_token}), 200
