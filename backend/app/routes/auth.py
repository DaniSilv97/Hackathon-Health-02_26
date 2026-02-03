from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

# Authentication routes
auth_bp.route('/login', methods=['POST'])(AuthController.login)
auth_bp.route('/register', methods=['POST'])(AuthController.register)
auth_bp.route('/logout', methods=['POST'])(AuthController.logout)
auth_bp.route('/me', methods=['GET'])(AuthController.me)
auth_bp.route('/refresh', methods=['POST'])(AuthController.refresh)
