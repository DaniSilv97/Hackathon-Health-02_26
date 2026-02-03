from flask import Blueprint
from app.controllers.dashboard_controller import DashboardController

api_bp = Blueprint('api', __name__)

# Dashboard routes
api_bp.route('/admin/dashboard', methods=['GET'])(DashboardController.admin_dashboard)
api_bp.route('/clinician/dashboard', methods=['GET'])(DashboardController.clinician_dashboard)
api_bp.route('/patient/dashboard', methods=['GET'])(DashboardController.patient_dashboard)
