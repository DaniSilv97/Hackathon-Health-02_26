<script setup>
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'

const authStore = useAuthStore()

onMounted(async () => {
  // Check if user is authenticated on app load
  if (authStore.token) {
    await authStore.fetchUser()
  }
})
</script>

<template>
  <router-view />
</template>
