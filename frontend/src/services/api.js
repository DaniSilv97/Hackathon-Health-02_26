import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Token is set in the auth store
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
