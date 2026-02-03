import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Auth pages
import Login from '@/pages/auth/Login.vue'
import Register from '@/pages/auth/Register.vue'

// Dashboard pages
import AdminDashboard from '@/pages/admin/Dashboard.vue'
import ClinicianDashboard from '@/pages/clinician/Dashboard.vue'
import PatientDashboard from '@/pages/patient/Dashboard.vue'

// Admin pages
import AdminUsers from '@/pages/admin/Users.vue'
import AdminMedications from '@/pages/admin/Medications.vue'

// Clinician pages
import ClinicianPatients from '@/pages/clinician/Patients.vue'
import ClinicianPrescriptions from '@/pages/clinician/Prescriptions.vue'

// Patient pages
import PatientCalendar from '@/pages/patient/Calendar.vue'

// Layouts
import AuthLayout from '@/layouts/AuthLayout.vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        name: 'login',
        component: Login,
        meta: { guest: true }
      },
      {
        path: 'register',
        name: 'register',
        component: Register,
        meta: { guest: true }
      }
    ]
  },
  // Admin routes
  {
    path: '/admin',
    component: DashboardLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      {
        path: 'dashboard',
        name: 'admin.dashboard',
        component: AdminDashboard
      },
      {
        path: 'users',
        name: 'admin.users',
        component: AdminUsers
      },
      {
        path: 'medications',
        name: 'admin.medications',
        component: AdminMedications
      }
    ]
  },
  // Clinician routes
  {
    path: '/clinician',
    component: DashboardLayout,
    meta: { requiresAuth: true, role: 'clinician' },
    children: [
      {
        path: 'dashboard',
        name: 'clinician.dashboard',
        component: ClinicianDashboard
      },
      {
        path: 'patients',
        name: 'clinician.patients',
        component: ClinicianPatients
      },
      {
        path: 'prescriptions',
        name: 'clinician.prescriptions',
        component: ClinicianPrescriptions
      },
      {
        path: 'prescriptions/create',
        name: 'clinician-prescription-create',
        component: ClinicianPrescriptions
      }
    ]
  },
  // Patient routes
  {
    path: '/patient',
    component: DashboardLayout,
    meta: { requiresAuth: true, role: 'patient' },
    children: [
      {
        path: 'dashboard',
        name: 'patient.dashboard',
        component: PatientDashboard
      },
      {
        path: 'calendar',
        name: 'patient.calendar',
        component: PatientCalendar
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const userRole = authStore.user?.role

  // Guest only routes (login, register)
  if (to.meta.guest && isAuthenticated) {
    // Redirect authenticated users to their dashboard
    const redirectMap = {
      admin: '/admin/dashboard',
      clinician: '/clinician/dashboard',
      patient: '/patient/dashboard'
    }
    return next(redirectMap[userRole] || '/login')
  }

  // Protected routes
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      return next('/login')
    }

    // Check role access
    if (to.meta.role && to.meta.role !== userRole) {
      const redirectMap = {
        admin: '/admin/dashboard',
        clinician: '/clinician/dashboard',
        patient: '/patient/dashboard'
      }
      return next(redirectMap[userRole] || '/login')
    }
  }

  next()
})

export default router
