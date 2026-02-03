import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

/**
 * Composable for authentication utilities
 */
export function useAuth() {
  const authStore = useAuthStore()

  const user = computed(() => authStore.user)
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const isAdmin = computed(() => authStore.isAdmin)
  const isClinician = computed(() => authStore.isClinician)
  const isPatient = computed(() => authStore.isPatient)
  const userRole = computed(() => authStore.userRole)
  const loading = computed(() => authStore.loading)
  const error = computed(() => authStore.error)

  /**
   * Check if user can access a resource based on roles
   */
  function canAccess(allowedRoles) {
    return authStore.hasAnyRole(allowedRoles)
  }

  /**
   * Get dashboard route based on user role
   */
  function getDashboardRoute() {
    const routes = {
      admin: '/admin/dashboard',
      clinician: '/clinician/dashboard',
      patient: '/patient/dashboard'
    }
    return routes[userRole.value] || '/login'
  }

  return {
    user,
    isAuthenticated,
    isAdmin,
    isClinician,
    isPatient,
    userRole,
    loading,
    error,
    canAccess,
    getDashboardRoute,
    login: authStore.login,
    logout: authStore.logout,
    register: authStore.register
  }
}
