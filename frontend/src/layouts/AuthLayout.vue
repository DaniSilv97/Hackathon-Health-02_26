<script setup>
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-primary-700 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full">
      <!-- Logo -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-white">Health Platform</h1>
        <p class="mt-2 text-primary-100">Sistema de Gestao de Saude</p>
      </div>

      <!-- Content -->
      <div class="bg-white rounded-xl shadow-2xl p-8">
        <router-view />
      </div>
    </div>
  </div>
</template>
