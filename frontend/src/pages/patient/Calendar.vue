<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'

const today = ref([])
const stats = ref({ total: 0, taken: 0, pending: 0 })
const loading = ref(true)
const error = ref(null)
const selectedDate = ref(new Date().toISOString().split('T')[0])
const dailySummary = ref('')
const showTTSModal = ref(false)
const ttsText = ref('')
const isSpeaking = ref(false)

async function fetchToday() {
  try {
    loading.value = true
    const response = await api.get('/api/calendar/today')
    today.value = response.data.medications
    stats.value = {
      total: response.data.total,
      taken: response.data.taken,
      pending: response.data.pending,
    }
  } catch (err) {
    error.value = 'Erro ao carregar medicamentos'
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function fetchDailySummary() {
  try {
    const response = await api.get('/api/ollama/daily-summary')
    dailySummary.value = response.data.summary
  } catch (err) {
    console.error('Erro ao carregar resumo:', err)
  }
}

async function markTaken(med) {
  try {
    await api.post(`/api/calendar/log/${med.log_id}/taken`)
    await fetchToday()
  } catch (err) {
    alert(err.response?.data?.error || 'Erro ao marcar')
  }
}

async function markSkipped(med, reason = '') {
  try {
    await api.post(`/api/calendar/log/${med.log_id}/skipped`, { reason })
    await fetchToday()
  } catch (err) {
    alert(err.response?.data?.error || 'Erro ao marcar')
  }
}

async function undoLog(med) {
  try {
    await api.post(`/api/calendar/log/${med.log_id}/undo`)
    await fetchToday()
  } catch (err) {
    alert(err.response?.data?.error || 'Erro ao desfazer')
  }
}

async function speakReminder(med) {
  try {
    const response = await api.post('/api/ollama/tts', {
      medication_name: med.medication.name,
      dosage: med.dosage,
    })
    ttsText.value = response.data.tts_text

    // Use Web Speech API
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(ttsText.value)
      utterance.lang = 'pt-PT'
      utterance.rate = 0.9
      utterance.onstart = () => { isSpeaking.value = true }
      utterance.onend = () => { isSpeaking.value = false }
      speechSynthesis.speak(utterance)
    } else {
      showTTSModal.value = true
    }
  } catch (err) {
    alert('Erro ao gerar lembrete de voz')
  }
}

function stopSpeaking() {
  if ('speechSynthesis' in window) {
    speechSynthesis.cancel()
    isSpeaking.value = false
  }
}

const progressPercentage = computed(() => {
  if (stats.value.total === 0) return 0
  return Math.round((stats.value.taken / stats.value.total) * 100)
})

const statusColors = {
  pending: 'border-yellow-400 bg-yellow-50',
  taken: 'border-green-400 bg-green-50',
  skipped: 'border-gray-400 bg-gray-50',
  missed: 'border-red-400 bg-red-50',
}

const statusLabels = {
  pending: 'Pendente',
  taken: 'Tomado',
  skipped: 'Ignorado',
  missed: 'Perdido',
}

onMounted(() => {
  fetchToday()
  fetchDailySummary()
})
</script>

<template>
  <div>
    <h1 class="page-title">Medicacao de Hoje</h1>

    <!-- Progress Card -->
    <div class="card mb-6 bg-gradient-to-r from-blue-500 to-blue-600 text-white">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-blue-100 text-sm">Progresso de Hoje</p>
          <p class="text-3xl font-bold">{{ stats.taken }} / {{ stats.total }}</p>
          <p class="text-blue-100 text-sm mt-1">medicamentos tomados</p>
        </div>
        <div class="relative w-24 h-24">
          <svg class="w-24 h-24 transform -rotate-90">
            <circle
              cx="48" cy="48" r="40"
              stroke="rgba(255,255,255,0.3)"
              stroke-width="8"
              fill="none"
            />
            <circle
              cx="48" cy="48" r="40"
              stroke="white"
              stroke-width="8"
              fill="none"
              :stroke-dasharray="251.2"
              :stroke-dashoffset="251.2 - (251.2 * progressPercentage / 100)"
              stroke-linecap="round"
            />
          </svg>
          <div class="absolute inset-0 flex items-center justify-center">
            <span class="text-xl font-bold">{{ progressPercentage }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Daily Summary -->
    <div v-if="dailySummary" class="card mb-6 bg-blue-50 border border-blue-200">
      <div class="flex items-start gap-3">
        <div class="p-2 bg-blue-100 rounded-full">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-blue-800">{{ dailySummary }}</p>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-gray-500">A carregar...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="card bg-red-50 text-red-700">
      {{ error }}
    </div>

    <!-- Medications List -->
    <div v-else class="space-y-4">
      <div
        v-for="med in today"
        :key="med.log_id"
        :class="['card border-l-4', statusColors[med.status]]"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center gap-3">
              <span class="text-2xl font-bold text-gray-400">{{ med.time }}</span>
              <div>
                <h3 class="font-semibold text-lg">{{ med.medication.name }}</h3>
                <p class="text-gray-600">{{ med.dosage }}</p>
              </div>
            </div>

            <p v-if="med.label" class="text-sm text-gray-500 mt-1">
              {{ med.label }}
            </p>

            <p v-if="med.instructions" class="text-sm text-gray-600 mt-2 bg-gray-50 p-2 rounded">
              {{ med.instructions }}
            </p>
          </div>

          <div class="flex flex-col items-end gap-2">
            <span
              :class="{
                'bg-yellow-100 text-yellow-800': med.status === 'pending',
                'bg-green-100 text-green-800': med.status === 'taken',
                'bg-gray-100 text-gray-800': med.status === 'skipped',
                'bg-red-100 text-red-800': med.status === 'missed',
              }"
              class="px-3 py-1 rounded-full text-sm font-medium"
            >
              {{ statusLabels[med.status] }}
            </span>

            <!-- Speak Button -->
            <button
              @click="speakReminder(med)"
              :disabled="isSpeaking"
              class="p-2 text-blue-600 hover:bg-blue-50 rounded-full"
              title="Ouvir lembrete"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-4 pt-4 border-t flex gap-2">
          <template v-if="med.status === 'pending'">
            <button
              @click="markTaken(med)"
              class="btn btn-primary flex-1"
            >
              Marcar como Tomado
            </button>
            <button
              @click="markSkipped(med)"
              class="btn btn-secondary"
            >
              Ignorar
            </button>
          </template>

          <template v-else>
            <button
              @click="undoLog(med)"
              class="btn btn-secondary flex-1"
            >
              Desfazer
            </button>
            <span v-if="med.taken_at" class="text-sm text-gray-500 self-center">
              Tomado as {{ new Date(med.taken_at).toLocaleTimeString('pt-PT', { hour: '2-digit', minute: '2-digit' }) }}
            </span>
          </template>
        </div>
      </div>

      <div v-if="today.length === 0" class="text-center py-12">
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900">Sem medicamentos para hoje</h3>
        <p class="text-gray-500 mt-1">Nao tem medicamentos agendados para hoje.</p>
      </div>
    </div>

    <!-- Stop Speaking Button -->
    <div v-if="isSpeaking" class="fixed bottom-4 right-4">
      <button
        @click="stopSpeaking"
        class="btn bg-red-600 text-white hover:bg-red-700 flex items-center gap-2 shadow-lg"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
        </svg>
        Parar
      </button>
    </div>

    <!-- TTS Modal (fallback) -->
    <div v-if="showTTSModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Lembrete</h2>
        <p class="text-gray-700 mb-4">{{ ttsText }}</p>
        <button @click="showTTSModal = false" class="btn btn-primary w-full">
          Fechar
        </button>
      </div>
    </div>
  </div>
</template>
