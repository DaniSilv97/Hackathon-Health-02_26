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
    // Skip for refresh endpoint to avoid loops
    if (config.url?.includes('/auth/refresh')) {
      return config
    }

    // First check if Authorization header is already set
    if (config.headers.Authorization) {
      console.log('Token already in headers')
      return config
    }

    // Check axios defaults (set by auth store after login)
    if (api.defaults.headers.common['Authorization']) {
      config.headers.Authorization = api.defaults.headers.common['Authorization']
      console.log('Token from axios defaults')
      return config
    }

    // Fallback: Get token from localStorage (for page refresh)
    const authData = localStorage.getItem('health-auth')
    console.log('localStorage health-auth:', authData ? 'exists' : 'not found')

    if (authData) {
      try {
        const parsed = JSON.parse(authData)
        console.log('Parsed auth data keys:', Object.keys(parsed))
        if (parsed.token) {
          config.headers.Authorization = `Bearer ${parsed.token}`
          console.log('Token added from localStorage')
        }
      } catch (e) {
        console.error('Failed to parse auth data:', e)
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - simplified, no auto-refresh to avoid loops
api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    // If 401, just reject - let the component handle logout
    if (error.response?.status === 401) {
      console.log('Got 401 - token may be invalid or expired')
    }
    return Promise.reject(error)
  }
)

export default api
