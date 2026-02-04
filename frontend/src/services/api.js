import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
})

// Request interceptor - Add token to every request
api.interceptors.request.use(
  (config) => {
    // First check if Authorization header is already set (from login)
    if (config.headers.Authorization) {
      return config
    }

    // Check axios defaults (set by auth store after login)
    if (api.defaults.headers.common['Authorization']) {
      config.headers.Authorization = api.defaults.headers.common['Authorization']
      return config
    }

    // Fallback: Get token from localStorage (for page refresh)
    const authData = localStorage.getItem('health-auth')
    if (authData) {
      try {
        const parsed = JSON.parse(authData)
        if (parsed.token) {
          config.headers.Authorization = `Bearer ${parsed.token}`
        }
      } catch (e) {
        // Invalid JSON in localStorage
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // Handle 401 errors (unauthorized)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      // Try to refresh the token
      const { useAuthStore } = await import('@/stores/auth')
      const authStore = useAuthStore()

      const refreshed = await authStore.refreshAccessToken()
      if (refreshed) {
        // Retry the original request
        originalRequest.headers['Authorization'] = `Bearer ${authStore.token}`
        return api(originalRequest)
      }
    }

    return Promise.reject(error)
  }
)

export default api
