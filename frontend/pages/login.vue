<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          로그인
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          만세력 서비스에 오신 것을 환영합니다
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              이메일
            </label>
            <input
                id="email"
                v-model="email"
                type="email"
                required
                class="input-field"
                placeholder="이메일을 입력하세요"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              비밀번호
            </label>
            <input
                id="password"
                v-model="password"
                type="password"
                required
                class="input-field"
                placeholder="비밀번호를 입력하세요"
            />
          </div>
        </div>

        <div>
          <el-button
              type="primary"
              native-type="submit"
              :loading="loading"
              class="w-full !h-12"
              size="large"
          >
            <span v-if="loading">로그인 중...</span>
            <span v-else>로그인</span>
          </el-button>
        </div>

        <div class="text-center">
          <p class="text-sm text-gray-600">
            계정이 없으신가요?
            <NuxtLink to="/register" class="font-medium text-primary-600 hover:text-primary-500">
              회원가입
            </NuxtLink>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false
})

const { login } = useAuth()
const toast = useToast()

const email = ref('')
const password = ref('')
const loading = ref(false)

const handleLogin = async () => {
  if (!email.value || !password.value) {
    toast.error('이메일과 비밀번호를 입력해주세요')
    return
  }

  loading.value = true

  try {
    const result = await login(email.value, password.value)

    if (result.success) {
      toast.success('로그인되었습니다')
      await navigateTo('/dashboard')
    } else {
      toast.error(result.error || '로그인에 실패했습니다')
    }
  } catch (error) {
    toast.error('로그인 중 오류가 발생했습니다')
  } finally {
    loading.value = false
  }
}

// 이미 로그인된 경우 대시보드로 이동
const { isLoggedIn } = useAuth()
watch(isLoggedIn, (newVal) => {
  if (newVal) {
    navigateTo('/dashboard')
  }
}, { immediate: true })
</script>
