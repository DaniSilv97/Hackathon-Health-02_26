<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()

const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    await api.get('/api/patient/dashboard')
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
    <h1 class="page-title">Dashboard do Paciente</h1>

    <!-- Welcome message -->
    <div class="card mb-6">
      <h2 class="text-lg font-semibold text-gray-900">
        Bem-vindo, {{ authStore.user?.name }}!
      </h2>
      <p class="text-gray-600 mt-1">
        O seu portal de saude pessoal.
      </p>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-8">
      <p class="text-gray-500">A carregar...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="card bg-red-50 border border-red-200">
      <p class="text-red-700">{{ error }}</p>
    </div>

    <!-- Content -->
    <div v-else>
      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <!-- Appointments -->
        <div class="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-blue-100 text-sm">Proximas Consultas</p>
              <p class="text-3xl font-bold mt-1">0</p>
            </div>
            <div class="p-3 bg-blue-400 bg-opacity-30 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Prescriptions -->
        <div class="card bg-gradient-to-br from-green-500 to-green-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-green-100 text-sm">Receitas Ativas</p>
              <p class="text-3xl font-bold mt-1">0</p>
            </div>
            <div class="p-3 bg-green-400 bg-opacity-30 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Messages -->
        <div class="card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-purple-100 text-sm">Mensagens</p>
              <p class="text-3xl font-bold mt-1">0</p>
            </div>
            <div class="p-3 bg-purple-400 bg-opacity-30 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Patient-only content using directive -->
      <div v-patient class="mb-8">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Acoes Rapidas</h3>
          <p class="text-gray-600">
            Este conteudo so e visivel para pacientes (usando a diretiva v-patient).
          </p>
          <div class="mt-4 flex flex-wrap gap-4">
            <button class="btn btn-primary">Marcar Consulta</button>
            <button class="btn btn-secondary">Ver Historico</button>
            <button class="btn btn-secondary">Contactar Medico</button>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Consultas Recentes</h3>
          <p class="text-gray-500 text-sm">Nenhuma consulta registada ainda.</p>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Ultimas Receitas</h3>
          <p class="text-gray-500 text-sm">Nenhuma receita registada ainda.</p>
        </div>
      </div>
    </div>
  </div>
</template>
