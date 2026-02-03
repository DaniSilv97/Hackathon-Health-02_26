<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'

const users = ref([])
const loading = ref(true)
const error = ref(null)
const showModal = ref(false)
const editingUser = ref(null)
const searchQuery = ref('')
const roleFilter = ref('')

const form = ref({
  name: '',
  email: '',
  password: '',
  role: 'patient',
  is_active: true,
})

const roles = ['admin', 'clinician', 'patient']

const filteredUsers = computed(() => {
  let filtered = users.value
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(u =>
      u.name.toLowerCase().includes(query) ||
      u.email.toLowerCase().includes(query)
    )
  }
  if (roleFilter.value) {
    filtered = filtered.filter(u => u.role === roleFilter.value)
  }
  return filtered
})

async function fetchUsers() {
  try {
    loading.value = true
    const response = await api.get('/api/users')
    users.value = response.data.users
  } catch (err) {
    error.value = 'Erro ao carregar utilizadores'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  editingUser.value = null
  form.value = { name: '', email: '', password: '', role: 'patient', is_active: true }
  showModal.value = true
}

function openEditModal(user) {
  editingUser.value = user
  form.value = { ...user, password: '' }
  showModal.value = true
}

async function saveUser() {
  try {
    if (editingUser.value) {
      await api.put(`/api/users/${editingUser.value.id}`, form.value)
    } else {
      await api.post('/api/users', form.value)
    }
    showModal.value = false
    await fetchUsers()
  } catch (err) {
    alert(err.response?.data?.error || 'Erro ao guardar')
  }
}

async function toggleActive(user) {
  try {
    if (user.is_active) {
      await api.delete(`/api/users/${user.id}`)
    } else {
      await api.post(`/api/users/${user.id}/activate`)
    }
    await fetchUsers()
  } catch (err) {
    alert(err.response?.data?.error || 'Erro ao alterar estado')
  }
}

function getRoleBadgeClass(role) {
  const classes = {
    admin: 'bg-red-100 text-red-800',
    clinician: 'bg-blue-100 text-blue-800',
    patient: 'bg-green-100 text-green-800',
  }
  return classes[role] || 'bg-gray-100 text-gray-800'
}

function getRoleLabel(role) {
  const labels = { admin: 'Admin', clinician: 'Clinico', patient: 'Paciente' }
  return labels[role] || role
}

onMounted(fetchUsers)
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="page-title mb-0">Gestao de Utilizadores</h1>
      <button @click="openCreateModal" class="btn btn-primary">
        + Novo Utilizador
      </button>
    </div>

    <!-- Filters -->
    <div class="card mb-6">
      <div class="flex flex-wrap gap-4">
        <div class="flex-1 min-w-[200px]">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Pesquisar por nome ou email..."
            class="input"
          />
        </div>
        <div>
          <select v-model="roleFilter" class="input">
            <option value="">Todos os roles</option>
            <option v-for="role in roles" :key="role" :value="role">
              {{ getRoleLabel(role) }}
            </option>
          </select>
        </div>
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

    <!-- Users Table -->
    <div v-else class="card overflow-hidden p-0">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-600">Nome</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-600">Email</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-600">Role</th>
            <th class="px-4 py-3 text-left text-sm font-medium text-gray-600">Estado</th>
            <th class="px-4 py-3 text-right text-sm font-medium text-gray-600">Acoes</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 text-sm">{{ user.name }}</td>
            <td class="px-4 py-3 text-sm text-gray-600">{{ user.email }}</td>
            <td class="px-4 py-3">
              <span :class="['px-2 py-1 rounded-full text-xs font-medium', getRoleBadgeClass(user.role)]">
                {{ getRoleLabel(user.role) }}
              </span>
            </td>
            <td class="px-4 py-3">
              <span :class="user.is_active ? 'text-green-600' : 'text-red-600'" class="text-sm">
                {{ user.is_active ? 'Ativo' : 'Inativo' }}
              </span>
            </td>
            <td class="px-4 py-3 text-right">
              <button @click="openEditModal(user)" class="text-blue-600 hover:text-blue-800 mr-3">
                Editar
              </button>
              <button
                @click="toggleActive(user)"
                :class="user.is_active ? 'text-red-600 hover:text-red-800' : 'text-green-600 hover:text-green-800'"
              >
                {{ user.is_active ? 'Desativar' : 'Ativar' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">
          {{ editingUser ? 'Editar Utilizador' : 'Novo Utilizador' }}
        </h2>

        <form @submit.prevent="saveUser" class="space-y-4">
          <div>
            <label class="label">Nome</label>
            <input v-model="form.name" type="text" required class="input" />
          </div>

          <div>
            <label class="label">Email</label>
            <input v-model="form.email" type="email" required class="input" />
          </div>

          <div>
            <label class="label">Password {{ editingUser ? '(deixe vazio para manter)' : '' }}</label>
            <input v-model="form.password" type="password" :required="!editingUser" class="input" />
          </div>

          <div>
            <label class="label">Role</label>
            <select v-model="form.role" class="input">
              <option v-for="role in roles" :key="role" :value="role">
                {{ getRoleLabel(role) }}
              </option>
            </select>
          </div>

          <div class="flex items-center">
            <input v-model="form.is_active" type="checkbox" id="is_active" class="mr-2" />
            <label for="is_active">Ativo</label>
          </div>

          <div class="flex justify-end gap-3 pt-4">
            <button type="button" @click="showModal = false" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
