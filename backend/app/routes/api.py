from flask import Blueprint
from app.controllers.dashboard_controller import DashboardController
from app.controllers.medication_controller import MedicationController
from app.controllers.prescription_controller import PrescriptionController
from app.controllers.calendar_controller import CalendarController
from app.controllers.user_controller import UserController
from app.controllers.ollama_controller import OllamaController

api_bp = Blueprint('api', __name__)

# ==================== Dashboard Routes ====================
api_bp.route('/admin/dashboard', methods=['GET'])(DashboardController.admin_dashboard)
api_bp.route('/clinician/dashboard', methods=['GET'])(DashboardController.clinician_dashboard)
api_bp.route('/patient/dashboard', methods=['GET'])(DashboardController.patient_dashboard)

# ==================== User Routes (Admin) ====================
api_bp.route('/users', methods=['GET'])(UserController.index)
api_bp.route('/users/<int:user_id_param>', methods=['GET'])(UserController.show)
api_bp.route('/users', methods=['POST'])(UserController.store)
api_bp.route('/users/<int:user_id_param>', methods=['PUT'])(UserController.update)
api_bp.route('/users/<int:user_id_param>', methods=['DELETE'])(UserController.destroy)
api_bp.route('/users/<int:user_id_param>/activate', methods=['POST'])(UserController.activate)
api_bp.route('/users/roles', methods=['GET'])(UserController.get_roles)
api_bp.route('/users/stats', methods=['GET'])(UserController.get_stats)

# ==================== Medication Routes (Admin) ====================
api_bp.route('/medications', methods=['GET'])(MedicationController.index)
api_bp.route('/medications/<int:medication_id>', methods=['GET'])(MedicationController.show)
api_bp.route('/medications', methods=['POST'])(MedicationController.store)
api_bp.route('/medications/<int:medication_id>', methods=['PUT'])(MedicationController.update)
api_bp.route('/medications/<int:medication_id>', methods=['DELETE'])(MedicationController.destroy)
api_bp.route('/medications/dosage-forms', methods=['GET'])(MedicationController.get_dosage_forms)

# ==================== Prescription Routes (Clinician) ====================
api_bp.route('/prescriptions', methods=['GET'])(PrescriptionController.index)
api_bp.route('/prescriptions/<int:prescription_id>', methods=['GET'])(PrescriptionController.show)
api_bp.route('/prescriptions', methods=['POST'])(PrescriptionController.store)
api_bp.route('/prescriptions/<int:prescription_id>', methods=['PUT'])(PrescriptionController.update)
api_bp.route('/prescriptions/<int:prescription_id>', methods=['DELETE'])(PrescriptionController.destroy)
api_bp.route('/prescriptions/<int:prescription_id>/schedules', methods=['POST'])(PrescriptionController.add_schedule)
api_bp.route('/prescriptions/patients', methods=['GET'])(PrescriptionController.get_patients)
api_bp.route('/prescriptions/frequencies', methods=['GET'])(PrescriptionController.get_frequencies)

# ==================== Calendar Routes (Patient) ====================
api_bp.route('/calendar', methods=['GET'])(CalendarController.get_calendar)
api_bp.route('/calendar/today', methods=['GET'])(CalendarController.get_today)
api_bp.route('/calendar/history', methods=['GET'])(CalendarController.get_history)
api_bp.route('/calendar/stats', methods=['GET'])(CalendarController.get_stats)
api_bp.route('/calendar/log/<int:log_id>/taken', methods=['POST'])(CalendarController.mark_taken)
api_bp.route('/calendar/log/<int:log_id>/skipped', methods=['POST'])(CalendarController.mark_skipped)
api_bp.route('/calendar/log/<int:log_id>/undo', methods=['POST'])(CalendarController.undo_log)

# ==================== Ollama Routes (AI Assistant) ====================
api_bp.route('/ollama/reminder', methods=['POST'])(OllamaController.generate_reminder)
api_bp.route('/ollama/chat', methods=['POST'])(OllamaController.chat)
api_bp.route('/ollama/daily-summary', methods=['GET'])(OllamaController.get_daily_summary)
api_bp.route('/ollama/tts', methods=['POST'])(OllamaController.get_tts_text)
api_bp.route('/ollama/models', methods=['GET'])(OllamaController.list_models)
api_bp.route('/ollama/health', methods=['GET'])(OllamaController.health_check)
