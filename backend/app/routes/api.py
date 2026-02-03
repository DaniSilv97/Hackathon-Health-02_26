from flask import Blueprint
from app.controllers.dashboard_controller import DashboardController
from app.controllers.medication_controller import MedicationController
from app.controllers.prescription_controller import PrescriptionController
from app.controllers.calendar_controller import CalendarController
from app.controllers.user_controller import UserController
from app.controllers.ollama_controller import OllamaController

api_bp = Blueprint('api', __name__)

# ==================== Dashboard Routes ====================
api_bp.add_url_rule('/admin/dashboard', 'admin_dashboard', DashboardController.admin_dashboard, methods=['GET'])
api_bp.add_url_rule('/clinician/dashboard', 'clinician_dashboard', DashboardController.clinician_dashboard, methods=['GET'])
api_bp.add_url_rule('/patient/dashboard', 'patient_dashboard', DashboardController.patient_dashboard, methods=['GET'])

# ==================== User Routes (Admin) ====================
api_bp.add_url_rule('/users', 'users_index', UserController.index, methods=['GET'])
api_bp.add_url_rule('/users', 'users_store', UserController.store, methods=['POST'])
api_bp.add_url_rule('/users/<int:user_id_param>', 'users_show', UserController.show, methods=['GET'])
api_bp.add_url_rule('/users/<int:user_id_param>', 'users_update', UserController.update, methods=['PUT'])
api_bp.add_url_rule('/users/<int:user_id_param>', 'users_destroy', UserController.destroy, methods=['DELETE'])
api_bp.add_url_rule('/users/<int:user_id_param>/activate', 'users_activate', UserController.activate, methods=['POST'])
api_bp.add_url_rule('/users/roles', 'users_roles', UserController.get_roles, methods=['GET'])
api_bp.add_url_rule('/users/stats', 'users_stats', UserController.get_stats, methods=['GET'])

# ==================== Medication Routes (Admin) ====================
api_bp.add_url_rule('/medications', 'medications_index', MedicationController.index, methods=['GET'])
api_bp.add_url_rule('/medications', 'medications_store', MedicationController.store, methods=['POST'])
api_bp.add_url_rule('/medications/<int:medication_id>', 'medications_show', MedicationController.show, methods=['GET'])
api_bp.add_url_rule('/medications/<int:medication_id>', 'medications_update', MedicationController.update, methods=['PUT'])
api_bp.add_url_rule('/medications/<int:medication_id>', 'medications_destroy', MedicationController.destroy, methods=['DELETE'])
api_bp.add_url_rule('/medications/dosage-forms', 'medications_dosage_forms', MedicationController.get_dosage_forms, methods=['GET'])

# ==================== Prescription Routes (Clinician) ====================
api_bp.add_url_rule('/prescriptions', 'prescriptions_index', PrescriptionController.index, methods=['GET'])
api_bp.add_url_rule('/prescriptions', 'prescriptions_store', PrescriptionController.store, methods=['POST'])
api_bp.add_url_rule('/prescriptions/<int:prescription_id>', 'prescriptions_show', PrescriptionController.show, methods=['GET'])
api_bp.add_url_rule('/prescriptions/<int:prescription_id>', 'prescriptions_update', PrescriptionController.update, methods=['PUT'])
api_bp.add_url_rule('/prescriptions/<int:prescription_id>', 'prescriptions_destroy', PrescriptionController.destroy, methods=['DELETE'])
api_bp.add_url_rule('/prescriptions/<int:prescription_id>/schedules', 'prescriptions_add_schedule', PrescriptionController.add_schedule, methods=['POST'])
api_bp.add_url_rule('/prescriptions/patients', 'prescriptions_patients', PrescriptionController.get_patients, methods=['GET'])
api_bp.add_url_rule('/prescriptions/frequencies', 'prescriptions_frequencies', PrescriptionController.get_frequencies, methods=['GET'])

# ==================== Calendar Routes (Patient) ====================
api_bp.add_url_rule('/calendar', 'calendar_index', CalendarController.get_calendar, methods=['GET'])
api_bp.add_url_rule('/calendar/today', 'calendar_today', CalendarController.get_today, methods=['GET'])
api_bp.add_url_rule('/calendar/history', 'calendar_history', CalendarController.get_history, methods=['GET'])
api_bp.add_url_rule('/calendar/stats', 'calendar_stats', CalendarController.get_stats, methods=['GET'])
api_bp.add_url_rule('/calendar/log/<int:log_id>/taken', 'calendar_mark_taken', CalendarController.mark_taken, methods=['POST'])
api_bp.add_url_rule('/calendar/log/<int:log_id>/skipped', 'calendar_mark_skipped', CalendarController.mark_skipped, methods=['POST'])
api_bp.add_url_rule('/calendar/log/<int:log_id>/undo', 'calendar_undo', CalendarController.undo_log, methods=['POST'])

# ==================== Ollama Routes (AI Assistant) ====================
api_bp.add_url_rule('/ollama/reminder', 'ollama_reminder', OllamaController.generate_reminder, methods=['POST'])
api_bp.add_url_rule('/ollama/chat', 'ollama_chat', OllamaController.chat, methods=['POST'])
api_bp.add_url_rule('/ollama/daily-summary', 'ollama_daily_summary', OllamaController.get_daily_summary, methods=['GET'])
api_bp.add_url_rule('/ollama/tts', 'ollama_tts', OllamaController.get_tts_text, methods=['POST'])
api_bp.add_url_rule('/ollama/models', 'ollama_models', OllamaController.list_models, methods=['GET'])
api_bp.add_url_rule('/ollama/health', 'ollama_health', OllamaController.health_check, methods=['GET'])
