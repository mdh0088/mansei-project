<template>
  <div id="app">
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
// 앱 초기화 시 인증 상태 복원
const authStore = useAuthStore()
onMounted(() => {
  authStore.initializeAuth()
})
</script>
