<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const patients = ref([])
const loading = ref(true)
const error = ref(null)
const searchQuery = ref('')

const filteredPatients = computed(() => {
  if (!searchQuery.value) return patients.value
  const query = searchQuery.value.toLowerCase()
  return patients.value.filter(p =>
    p.name.toLowerCase().includes(query) ||
    p.email.toLowerCase().includes(query)
  )
})

async function fetchPatients() {
  try {
    loading.value = true
    const response = await api.get('/api/prescriptions/patients')
    patients.value = response.data.patients
  } catch (err) {
    error.value = 'Erro ao carregar pacientes'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function viewPatient(patient) {
  router.push({ name: 'clinician-patient-detail', params: { id: patient.id } })
}

function createPrescription(patient) {
  router.push({ name: 'clinician-prescription-create', query: { patient_id: patient.id } })
}

onMounted(fetchPatients)
</script>

<template>
  <div>
    <h1 class="page-title">Pacientes</h1>

    <!-- Search -->
    <div class="card mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Pesquisar pacientes..."
        class="input"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-gray-500">A carregar...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="card bg-red-50 text-red-700">
      {{ error }}
    </div>

    <!-- Patients List -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="patient in filteredPatients"
        :key="patient.id"
        class="card hover:shadow-lg transition-shadow cursor-pointer"
        @click="viewPatient(patient)"
      >
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
            <span class="text-blue-600 font-bold text-lg">
              {{ patient.name.charAt(0).toUpperCase() }}
            </span>
          </div>
          <div class="flex-1">
            <h3 class="font-semibold">{{ patient.name }}</h3>
            <p class="text-sm text-gray-500">{{ patient.email }}</p>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t flex justify-between">
          <button
            @click.stop="viewPatient(patient)"
            class="text-blue-600 hover:text-blue-800 text-sm"
          >
            Ver Detalhes
          </button>
          <button
            @click.stop="createPrescription(patient)"
            class="text-green-600 hover:text-green-800 text-sm"
          >
            + Prescricao
          </button>
        </div>
      </div>

      <div v-if="filteredPatients.length === 0" class="col-span-full text-center py-8 text-gray-500">
        Nenhum paciente encontrado.
      </div>
    </div>
  </div>
</template>
