<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const role = ref('patient')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

const roles = [
  { value: 'patient', label: 'Paciente' },
  { value: 'clinician', label: 'Clinico' }
]

async function handleRegister() {
  errorMessage.value = ''
  successMessage.value = ''

  // Validate passwords match
  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'As palavras-passe nao coincidem.'
    return
  }

  isLoading.value = true

  try {
    await authStore.register(name.value, email.value, password.value, role.value)
    successMessage.value = 'Registo efetuado com sucesso! Pode agora fazer login.'

    // Redirect to login after 2 seconds
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Falha no registo. Tente novamente.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-900 text-center mb-6">Registar</h2>

    <!-- Success message -->
    <div
      v-if="successMessage"
      class="mb-4 p-4 bg-green-50 border border-green-200 text-green-700 rounded-lg"
    >
      {{ successMessage }}
    </div>

    <!-- Error message -->
    <div
      v-if="errorMessage"
      class="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg"
    >
      {{ errorMessage }}
    </div>

    <form @submit.prevent="handleRegister" class="space-y-5">
      <!-- Name -->
      <div>
        <label for="name" class="label">Nome</label>
        <input
          id="name"
          v-model="name"
          type="text"
          required
          class="input"
          placeholder="O seu nome"
        />
      </div>

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

      <!-- Role -->
      <div>
        <label for="role" class="label">Tipo de conta</label>
        <select id="role" v-model="role" class="input">
          <option v-for="r in roles" :key="r.value" :value="r.value">
            {{ r.label }}
          </option>
        </select>
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
          minlength="6"
        />
      </div>

      <!-- Confirm Password -->
      <div>
        <label for="confirmPassword" class="label">Confirmar palavra-passe</label>
        <input
          id="confirmPassword"
          v-model="confirmPassword"
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
        <span v-if="isLoading">A registar...</span>
        <span v-else>Registar</span>
      </button>
    </form>

    <!-- Login link -->
    <p class="mt-6 text-center text-sm text-gray-600">
      Ja tem conta?
      <router-link to="/login" class="text-primary-600 hover:text-primary-500 font-medium">
        Entrar
      </router-link>
    </p>
  </div>
</template>
