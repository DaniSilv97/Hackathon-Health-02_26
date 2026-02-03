import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'

// Import directives
import { adminDirective, clinicianDirective, patientDirective } from './directives/role'

// Import styles
import './assets/main.css'

const app = createApp(App)

// Setup Pinia
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// Setup Router
app.use(router)

// Register role directives
app.directive('admin', adminDirective)
app.directive('clinician', clinicianDirective)
app.directive('patient', patientDirective)

app.mount('#app')
