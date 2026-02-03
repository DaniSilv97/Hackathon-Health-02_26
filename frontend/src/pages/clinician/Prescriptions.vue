<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const route = useRoute()

const prescriptions = ref([])
const patients = ref([])
const medications = ref([])
const frequencies = ref([])
const loading = ref(true)
const error = ref(null)
const showModal = ref(false)

const form = ref({
  patient_id: '',
  medication_id: '',
  dosage: '',
  frequency: 'once_daily',
  instructions: '',
  notes: '',
  start_date: new Date().toISOString().split('T')[0],
  end_date: '',
  schedules: [],
})

const newSchedule = ref({
  time: '08:00',
  label: 'Manha',
  dosage: '',
})

async function fetchData() {
  try {
    loading.value = true
    const [prescRes, patientsRes, medsRes, freqRes] = await Promise.all([
      api.get('/api/prescriptions'),
      api.get('/api/prescriptions/patients'),
      api.get('/api/medications'),
      api.get('/api/prescriptions/frequencies'),
    ])
    prescriptions.value = prescRes.data.prescriptions
    patients.value = patientsRes.data.patients
    medications.value = medsRes.data.medications
    frequencies.value = freqRes.data.frequencies

    // Check if patient_id in query
    if (route.query.patient_id) {
      form.value.patient_id = parseInt(route.query.patient_id)
      showModal.value = true
    }
  } catch (err) {
    error.value = 'Erro ao carregar dados'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  form.value = {
    patient_id: '',
    medication_id: '',
    dosage: '',
    frequency: 'once_daily',
    instructions: '',
    notes: '',
    start_date: new Date().toISOString().split('T')[0],
    end_date: '',
    schedules: [],
  }
  showModal.value = true
}

function addSchedule() {
  form.value.schedules.push({ ...newSchedule.value })
  newSchedule.value = { time: '08:00', label: '', dosage: '' }
}

function removeSchedule(index) {
  form.value.schedules.splice(index, 1)
}

async function savePrescription() {
  try {
    await api.post('/api/prescriptions', form.value)
    showModal.value = false
    await fetchData()
  } catch (err) {
    alert(err.response?.data?.error || 'Erro ao guardar')
  }
}

async function deactivatePrescription(prescription) {
  if (!confirm('Tem a certeza que deseja desativar esta prescricao?')) return
  try {
    await api.delete(`/api/prescriptions/${prescription.id}`)
    await fetchData()
  } catch (err) {
    alert(err.response?.data?.error || 'Erro ao desativar')
  }
}

function getPatientName(id) {
  const patient = patients.value.find(p => p.id === id)
  return patient ? patient.name : 'Desconhecido'
}

function getMedicationName(id) {
  const med = medications.value.find(m => m.id === id)
  return med ? med.name : 'Desconhecido'
}

function getFrequencyLabel(value) {
  const freq = frequencies.value.find(f => f[0] === value)
  return freq ? freq[1] : value
}

onMounted(fetchData)
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="page-title mb-0">Prescricoes</h1>
      <button @click="openCreateModal" class="btn btn-primary">
        + Nova Prescricao
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-gray-500">A carregar...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="card bg-red-50 text-red-700">
      {{ error }}
    </div>

    <!-- Prescriptions List -->
    <div v-else class="space-y-4">
      <div
        v-for="prescription in prescriptions"
        :key="prescription.id"
        :class="['card', !prescription.is_active && 'opacity-60']"
      >
        <div class="flex justify-between items-start">
          <div>
            <h3 class="font-semibold text-lg">
              {{ prescription.medication?.name || getMedicationName(prescription.medication_id) }}
            </h3>
            <p class="text-gray-600">
              Paciente: {{ prescription.patient?.name || getPatientName(prescription.patient_id) }}
            </p>
          </div>
          <span
            :class="prescription.is_current ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
            class="px-2 py-1 rounded-full text-xs"
          >
            {{ prescription.is_current ? 'Ativa' : 'Inativa' }}
          </span>
        </div>

        <div class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span class="text-gray-500">Dosagem:</span>
            <p class="font-medium">{{ prescription.dosage }}</p>
          </div>
          <div>
            <span class="text-gray-500">Frequencia:</span>
            <p class="font-medium">{{ getFrequencyLabel(prescription.frequency) }}</p>
          </div>
          <div>
            <span class="text-gray-500">Inicio:</span>
            <p class="font-medium">{{ prescription.start_date }}</p>
          </div>
          <div>
            <span class="text-gray-500">Fim:</span>
            <p class="font-medium">{{ prescription.end_date || 'Indefinido' }}</p>
          </div>
        </div>

        <!-- Schedules -->
        <div v-if="prescription.schedules?.length" class="mt-4 pt-4 border-t">
          <p class="text-sm text-gray-500 mb-2">Horarios:</p>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="schedule in prescription.schedules"
              :key="schedule.id"
              class="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm"
            >
              {{ schedule.time }} {{ schedule.label ? `(${schedule.label})` : '' }}
            </span>
          </div>
        </div>

        <div v-if="prescription.instructions" class="mt-4 text-sm text-gray-600">
          <strong>Instrucoes:</strong> {{ prescription.instructions }}
        </div>

        <div class="mt-4 pt-4 border-t flex justify-end">
          <button
            v-if="prescription.is_active"
            @click="deactivatePrescription(prescription)"
            class="text-red-600 hover:text-red-800 text-sm"
          >
            Desativar
          </button>
        </div>
      </div>

      <div v-if="prescriptions.length === 0" class="text-center py-8 text-gray-500">
        Nenhuma prescricao encontrada.
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <h2 class="text-xl font-bold mb-4">Nova Prescricao</h2>

        <form @submit.prevent="savePrescription" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label">Paciente *</label>
              <select v-model="form.patient_id" required class="input">
                <option value="">Selecionar...</option>
                <option v-for="patient in patients" :key="patient.id" :value="patient.id">
                  {{ patient.name }}
                </option>
              </select>
            </div>
            <div>
              <label class="label">Medicamento *</label>
              <select v-model="form.medication_id" required class="input">
                <option value="">Selecionar...</option>
                <option v-for="med in medications" :key="med.id" :value="med.id">
                  {{ med.name }} {{ med.strength ? `(${med.strength})` : '' }}
                </option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label">Dosagem *</label>
              <input v-model="form.dosage" type="text" required class="input" placeholder="ex: 1 comprimido" />
            </div>
            <div>
              <label class="label">Frequencia *</label>
              <select v-model="form.frequency" required class="input">
                <option v-for="[value, label] in frequencies" :key="value" :value="value">
                  {{ label }}
                </option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label">Data Inicio *</label>
              <input v-model="form.start_date" type="date" required class="input" />
            </div>
            <div>
              <label class="label">Data Fim (opcional)</label>
              <input v-model="form.end_date" type="date" class="input" />
            </div>
          </div>

          <div>
            <label class="label">Instrucoes</label>
            <textarea v-model="form.instructions" class="input" rows="2"></textarea>
          </div>

          <!-- Schedules -->
          <div class="border rounded-lg p-4">
            <label class="label">Horarios de Toma</label>

            <div class="flex gap-2 mb-4">
              <input v-model="newSchedule.time" type="time" class="input w-32" />
              <input v-model="newSchedule.label" type="text" class="input flex-1" placeholder="Label (ex: Manha)" />
              <button type="button" @click="addSchedule" class="btn btn-secondary">
                Adicionar
              </button>
            </div>

            <div v-if="form.schedules.length" class="space-y-2">
              <div
                v-for="(schedule, index) in form.schedules"
                :key="index"
                class="flex items-center gap-2 bg-gray-50 p-2 rounded"
              >
                <span class="font-medium">{{ schedule.time }}</span>
                <span v-if="schedule.label" class="text-gray-600">- {{ schedule.label }}</span>
                <button
                  type="button"
                  @click="removeSchedule(index)"
                  class="ml-auto text-red-600 hover:text-red-800"
                >
                  Remover
                </button>
              </div>
            </div>

            <p v-else class="text-gray-500 text-sm">
              Adicione horarios para a medicacao.
            </p>
          </div>

          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="showModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              Criar Prescricao
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
