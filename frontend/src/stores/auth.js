import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(null)
  const refreshToken = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Initialize axios header from persisted token on store creation
  function initializeFromStorage() {
    const authData = localStorage.getItem('health-auth')
    if (authData) {
      try {
        const parsed = JSON.parse(authData)
        if (parsed.token) {
          api.defaults.headers.common['Authorization'] = `Bearer ${parsed.token}`
          console.log('Auth initialized from storage')
        }
      } catch (e) {
        console.error('Failed to initialize auth from storage:', e)
      }
    }
  }

  // Call immediately when store is created
  initializeFromStorage()

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isClinician = computed(() => user.value?.role === 'clinician')
  const isPatient = computed(() => user.value?.role === 'patient')
  const userRole = computed(() => user.value?.role)

  // Actions
  async function login(email, password) {
    loading.value = true
    error.value = null

    try {
      const response = await api.post('/auth/login', { email, password })
      const data = response.data

      token.value = data.access_token
      refreshToken.value = data.refresh_token
      user.value = data.user

      // Set token in API headers
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`

      // Redirect based on role
      router.push(data.redirect)

      return data
    } catch (err) {
      error.value = err.response?.data?.error || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function register(name, email, password, role = 'patient') {
    loading.value = true
    error.value = null

    try {
      const response = await api.post('/auth/register', {
        name,
        email,
        password,
        role
      })

      return response.data
    } catch (err) {
      error.value = err.response?.data?.error || 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await api.post('/auth/logout')
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear state regardless of API response
      user.value = null
      token.value = null
      refreshToken.value = null
      delete api.defaults.headers.common['Authorization']
      router.push('/login')
    }
  }

  async function fetchUser() {
    if (!token.value) return null

    try {
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      const response = await api.get('/auth/me')
      user.value = response.data.user
      return user.value
    } catch (err) {
      // Token might be expired
      logout()
      return null
    }
  }

  async function refreshAccessToken() {
    if (!refreshToken.value) return false

    try {
      const response = await api.post('/auth/refresh', null, {
        headers: { Authorization: `Bearer ${refreshToken.value}` }
      })
      token.value = response.data.access_token
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      return true
    } catch (err) {
      logout()
      return false
    }
  }

  // Check if user has specific role
  function hasRole(role) {
    return user.value?.role === role
  }

  // Check if user has any of the specified roles
  function hasAnyRole(roles) {
    return roles.includes(user.value?.role)
  }

  return {
    // State
    user,
    token,
    refreshToken,
    loading,
    error,
    // Getters
    isAuthenticated,
    isAdmin,
    isClinician,
    isPatient,
    userRole,
    // Actions
    login,
    register,
    logout,
    fetchUser,
    refreshAccessToken,
    hasRole,
    hasAnyRole
  }
}, {
  persist: {
    key: 'health-auth',
    paths: ['token', 'refreshToken', 'user']
  }
})
