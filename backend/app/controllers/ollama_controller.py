"""
OllamaController - AI assistant for medication reminders and TTS.
"""

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.prescription import Prescription
from app.models.medication_log import MedicationLog
from app.services.ollama_service import OllamaService
from datetime import date, datetime


class OllamaController:
    @staticmethod
    @jwt_required()
    def generate_reminder():
        """Generate a friendly medication reminder using Ollama."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json() or {}
        medication_name = data.get('medication_name', 'your medication')
        dosage = data.get('dosage', '')
        time = data.get('time', '')

        # Create prompt for friendly reminder
        prompt = f"""You are a friendly health assistant. Generate a short, warm reminder
for a patient to take their medication. Keep it brief (1-2 sentences), friendly, and encouraging.

Medication: {medication_name}
Dosage: {dosage}
Scheduled time: {time}

Generate only the reminder message, nothing else. Write in Portuguese (Portugal)."""

        ollama = OllamaService()
        result = ollama.generate(prompt, model='llama2')

        if 'error' in result:
            # Fallback message if Ollama is not available
            fallback = f"Olá! Está na hora de tomar {medication_name}"
            if dosage:
                fallback += f" ({dosage})"
            fallback += ". Cuide bem de si!"
            return jsonify({
                'reminder': fallback,
                'generated': False,
                'error': result['error']
            }), 200

        return jsonify({
            'reminder': result.get('response', '').strip(),
            'generated': True
        }), 200

    @staticmethod
    @jwt_required()
    def chat():
        """Chat with AI assistant about medications."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        if not data or not data.get('message'):
            return jsonify({'error': 'message is required'}), 400

        user_message = data['message']

        # Get user's current medications for context
        medications_context = ""
        if user.is_patient():
            prescriptions = Prescription.query.filter_by(
                patient_id=user.id,
                is_active=True
            ).all()

            if prescriptions:
                medications_context = "Patient's current medications:\n"
                for p in prescriptions:
                    medications_context += f"- {p.medication.name}: {p.dosage}, {p.frequency}\n"

        system_prompt = f"""You are a helpful health assistant named HealthBot. You help patients
with medication-related questions. Be friendly, supportive, and informative.

IMPORTANT:
- Always recommend consulting a doctor for medical advice
- Never provide medical diagnosis
- Focus on medication reminders and general wellness tips
- Keep responses concise and easy to understand
- Respond in Portuguese (Portugal)

{medications_context}"""

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ]

        ollama = OllamaService()
        result = ollama.chat(messages, model='llama2')

        if 'error' in result:
            return jsonify({
                'response': 'Desculpe, não consigo responder neste momento. Por favor, tente novamente mais tarde.',
                'error': result['error']
            }), 200

        return jsonify({
            'response': result.get('message', {}).get('content', '').strip()
        }), 200

    @staticmethod
    @jwt_required()
    def get_daily_summary():
        """Get AI-generated daily summary for patient."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_patient():
            return jsonify({'error': 'Unauthorized - Patient only'}), 403

        today = date.today()

        # Get today's logs
        logs = MedicationLog.query.filter_by(
            patient_id=user.id,
            scheduled_date=today
        ).all()

        total = len(logs)
        taken = sum(1 for log in logs if log.status == 'taken')
        pending = sum(1 for log in logs if log.status == 'pending')

        # Generate summary with Ollama
        prompt = f"""You are a health assistant. Generate a brief, encouraging daily summary
for a patient about their medication adherence today.

Statistics:
- Total medications scheduled: {total}
- Taken: {taken}
- Pending: {pending}

Patient name: {user.name}

Generate a short (2-3 sentences), friendly summary in Portuguese (Portugal).
Be encouraging and supportive. If they took all medications, congratulate them.
If some are pending, gently remind them."""

        ollama = OllamaService()
        result = ollama.generate(prompt, model='llama2')

        summary = ""
        if 'error' in result:
            # Fallback message
            if pending == 0 and taken > 0:
                summary = f"Parabéns {user.name}! Tomou todos os medicamentos de hoje. Continue assim!"
            elif pending > 0:
                summary = f"Olá {user.name}! Ainda tem {pending} medicamento(s) para tomar hoje. Não se esqueça!"
            else:
                summary = f"Olá {user.name}! Verifique o seu calendário de medicação para hoje."
        else:
            summary = result.get('response', '').strip()

        return jsonify({
            'summary': summary,
            'stats': {
                'total': total,
                'taken': taken,
                'pending': pending,
            }
        }), 200

    @staticmethod
    @jwt_required()
    def get_tts_text():
        """Get text for Text-to-Speech reminder."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json() or {}

        medication_name = data.get('medication_name', 'o seu medicamento')
        dosage = data.get('dosage', '')
        patient_name = data.get('patient_name', user.name)

        # Simple TTS text (no AI needed)
        tts_text = f"Olá {patient_name}. "
        tts_text += f"Está na hora de tomar {medication_name}"
        if dosage:
            tts_text += f", {dosage}"
        tts_text += ". Não se esqueça de registar quando tomar."

        return jsonify({
            'tts_text': tts_text,
            'language': 'pt-PT'
        }), 200

    @staticmethod
    @jwt_required()
    def list_models():
        """List available Ollama models."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not user.is_admin():
            return jsonify({'error': 'Unauthorized - Admin only'}), 403

        ollama = OllamaService()
        result = ollama.list_models()

        return jsonify(result), 200

    @staticmethod
    @jwt_required()
    def health_check():
        """Check if Ollama service is available."""
        ollama = OllamaService()
        result = ollama.list_models()

        if 'error' in result:
            return jsonify({
                'status': 'unavailable',
                'error': result['error']
            }), 503

        return jsonify({
            'status': 'available',
            'models': result.get('models', [])
        }), 200
