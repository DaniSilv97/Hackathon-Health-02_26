from flask import Blueprint, jsonify

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def index():
    """Home page."""
    return jsonify({
        'message': 'Welcome to Health API',
        'version': '1.0.0'
    })


@web_bp.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})
