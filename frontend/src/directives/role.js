import { useAuthStore } from '@/stores/auth'

/**
 * Directive to show element only for admin users
 * Usage: <div v-admin>Admin only content</div>
 */
export const adminDirective = {
  mounted(el) {
    const authStore = useAuthStore()
    if (!authStore.isAdmin) {
      el.style.display = 'none'
    }
  },
  updated(el) {
    const authStore = useAuthStore()
    el.style.display = authStore.isAdmin ? '' : 'none'
  }
}

/**
 * Directive to show element only for clinician users
 * Usage: <div v-clinician>Clinician only content</div>
 */
export const clinicianDirective = {
  mounted(el) {
    const authStore = useAuthStore()
    if (!authStore.isClinician) {
      el.style.display = 'none'
    }
  },
  updated(el) {
    const authStore = useAuthStore()
    el.style.display = authStore.isClinician ? '' : 'none'
  }
}

/**
 * Directive to show element only for patient users
 * Usage: <div v-patient>Patient only content</div>
 */
export const patientDirective = {
  mounted(el) {
    const authStore = useAuthStore()
    if (!authStore.isPatient) {
      el.style.display = 'none'
    }
  },
  updated(el) {
    const authStore = useAuthStore()
    el.style.display = authStore.isPatient ? '' : 'none'
  }
}

/**
 * Directive to show element for any of the specified roles
 * Usage: <div v-role="['admin', 'clinician']">Admin or Clinician content</div>
 */
export const roleDirective = {
  mounted(el, binding) {
    const authStore = useAuthStore()
    const roles = binding.value || []
    if (!authStore.hasAnyRole(roles)) {
      el.style.display = 'none'
    }
  },
  updated(el, binding) {
    const authStore = useAuthStore()
    const roles = binding.value || []
    el.style.display = authStore.hasAnyRole(roles) ? '' : 'none'
  }
}
