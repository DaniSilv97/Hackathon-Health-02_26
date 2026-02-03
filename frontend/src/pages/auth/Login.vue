<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

async function handleLogin() {
  errorMessage.value = ''
  isLoading.value = true

  try {
    await authStore.login(email.value, password.value)
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Falha no login. Verifique as suas credenciais.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 text-center mb-6">Entrar</h2>

    <!-- Error message -->
    <div
      v-if="errorMessage"
      class="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg"
    >
      {{ errorMessage }}
    </div>

    <form @submit.prevent="handleLogin" class="space-y-6">
      <!-- Email -->
      <div>
        <label for="email" class="label">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          required
          class="input"
          placeholder="seu@email.com"
        />
      </div>

      <!-- Password -->
      <div>
        <label for="password" class="label">Palavra-passe</label>
        <input
          id="password"
          v-model="password"
          type="password"
          required
          class="input"
          placeholder="********"
        />
      </div>

      <!-- Submit -->
      <button
        type="submit"
        :disabled="isLoading"
        class="btn btn-primary w-full"
      >
        <span v-if="isLoading">A entrar...</span>
        <span v-else>Entrar</span>
      </button>
    </form>

    <!-- Register link -->
    <p class="mt-6 text-center text-sm text-gray-600">
      Nao tem conta?
      <router-link to="/register" class="text-primary-600 hover:text-primary-500 font-medium">
        Registar
      </router-link>
    </p>

    <!-- Demo credentials -->
    <div class="mt-6 p-4 bg-gray-50 rounded-lg">
      <p class="text-sm font-medium text-gray-700 mb-2">Credenciais de teste:</p>
      <ul class="text-xs text-gray-600 space-y-1">
        <li><strong>Admin:</strong> admin@health.com</li>
        <li><strong>Clinico:</strong> clinician@health.com</li>
        <li><strong>Paciente:</strong> patient@health.com</li>
        <li class="text-gray-500">(password: qualquer)</li>
      </ul>
    </div>
  </div>
</template>
