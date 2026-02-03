<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const user = computed(() => authStore.user)
const userRole = computed(() => authStore.userRole)

const roleLabels = {
  admin: 'Administrador',
  clinician: 'Clinico',
  patient: 'Paciente'
}

const roleColors = {
  admin: 'bg-purple-100 text-purple-800',
  clinician: 'bg-green-100 text-green-800',
  patient: 'bg-blue-100 text-blue-800'
}

async function handleLogout() {
  await authStore.logout()
}

// Navigation items based on role
const navItems = computed(() => {
  const baseItems = {
    admin: [
      { name: 'Dashboard', path: '/admin/dashboard', icon: 'home' },
      { name: 'Utilizadores', path: '/admin/users', icon: 'users' },
      { name: 'Medicamentos', path: '/admin/medications', icon: 'pill' },
    ],
    clinician: [
      { name: 'Dashboard', path: '/clinician/dashboard', icon: 'home' },
      { name: 'Pacientes', path: '/clinician/patients', icon: 'users' },
      { name: 'Prescricoes', path: '/clinician/prescriptions', icon: 'clipboard' },
    ],
    patient: [
      { name: 'Dashboard', path: '/patient/dashboard', icon: 'home' },
      { name: 'Calendario', path: '/patient/calendar', icon: 'calendar' },
    ]
  }
  return baseItems[userRole.value] || []
})
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="fixed inset-y-0 left-0 w-64 bg-white shadow-lg">
      <!-- Logo -->
      <div class="h-16 flex items-center justify-center border-b">
        <h1 class="text-xl font-bold text-primary-600">Health Platform</h1>
      </div>

      <!-- Navigation -->
      <nav class="mt-6 px-4">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center px-4 py-3 mb-2 rounded-lg text-gray-700 hover:bg-primary-50 hover:text-primary-600 transition-colors"
          active-class="bg-primary-50 text-primary-600 font-medium"
        >
          <span>{{ item.name }}</span>
        </router-link>
      </nav>

      <!-- User info at bottom -->
      <div class="absolute bottom-0 left-0 right-0 p-4 border-t">
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium text-gray-900">{{ user?.name }}</p>
            <span :class="['text-xs px-2 py-1 rounded-full', roleColors[userRole]]">
              {{ roleLabels[userRole] }}
            </span>
          </div>
          <button
            @click="handleLogout"
            class="p-2 text-gray-500 hover:text-red-600 transition-colors"
            title="Logout"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main content -->
    <main class="ml-64 p-8">
      <router-view />
    </main>
  </div>
</template>
