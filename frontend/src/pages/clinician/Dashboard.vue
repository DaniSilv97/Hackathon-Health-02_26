<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()

const stats = ref({
  total_patients: 0
})
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await api.get('/api/clinician/dashboard')
    stats.value = response.data.stats
  } catch (err) {
    error.value = 'Erro ao carregar dados do dashboard'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <h1 class="page-title">Dashboard do Clinico</h1>

    <!-- Welcome message -->
    <div class="card mb-6">
      <h2 class="text-lg font-semibold text-gray-900">
        Bem-vindo, Dr(a). {{ authStore.user?.name }}!
      </h2>
      <p class="text-gray-600 mt-1">
        Painel de controlo clinico para gestao de pacientes.
      </p>
    </div>

    <!-- Stats Grid -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-gray-500">A carregar...</p>
    </div>

    <div v-else-if="error" class="card bg-red-50 border border-red-200">
      <p class="text-red-700">{{ error }}</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Total Patients -->
      <div class="card bg-gradient-to-br from-green-500 to-green-600 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-green-100 text-sm">Total de Pacientes</p>
            <p class="text-3xl font-bold mt-1">{{ stats.total_patients }}</p>
          </div>
          <div class="p-3 bg-green-400 bg-opacity-30 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Today's Appointments -->
      <div class="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-blue-100 text-sm">Consultas Hoje</p>
            <p class="text-3xl font-bold mt-1">0</p>
          </div>
          <div class="p-3 bg-blue-400 bg-opacity-30 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Clinician-only content using directive -->
    <div v-clinician class="mt-8">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Acoes do Clinico</h3>
        <p class="text-gray-600">
          Este conteudo so e visivel para clinicos (usando a diretiva v-clinician).
        </p>
        <div class="mt-4 flex gap-4">
          <button class="btn btn-primary">Ver Pacientes</button>
          <button class="btn btn-secondary">Agendar Consulta</button>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Pacientes Recentes</h3>
        <p class="text-gray-500 text-sm">Nenhum paciente registado ainda.</p>
      </div>

      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Proximas Consultas</h3>
        <p class="text-gray-500 text-sm">Nenhuma consulta agendada.</p>
      </div>
    </div>
  </div>
</template>
