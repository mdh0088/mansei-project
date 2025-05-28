<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          회원가입
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          만세력 서비스를 시작해보세요
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              이메일
            </label>
            <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="input-field"
                placeholder="이메일을 입력하세요"
            />
          </div>

          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              사용자명
            </label>
            <input
                id="username"
                v-model="form.username"
                type="text"
                required
                class="input-field"
                placeholder="사용자명을 입력하세요"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              비밀번호
            </label>
            <input
                id="password"
                v-model="form.password"
                type="password"
                required
                class="input-field"
                placeholder="비밀번호를 입력하세요"
            />
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">
              비밀번호 확인
            </label>
            <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                type="password"
                required
                class="input-field"
                placeholder="비밀번호를 다시 입력하세요"
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
            <span v-if="loading">가입 중...</span>
            <span v-else>회원가입</span>
          </el-button>
        </div>

        <div class="text-center">
          <p class="text-sm text-gray-600">
            이미 계정이 있으신가요?
            <NuxtLink to="/login" class="font-medium text-primary-600 hover:text-primary-500">
              로그인
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

const { register } = useAuth()
const toast = useToast()

const form = reactive({
  email: '',
  username: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)

const handleRegister = async () => {
  // 유효성 검사
  if (!form.email || !form.username || !form.password || !form.confirmPassword) {
    toast.error('모든 필드를 입력해주세요')
    return
  }

  if (form.password !== form.confirmPassword) {
    toast.error('비밀번호가 일치하지 않습니다')
    return
  }

  if (form.password.length < 6) {
    toast.error('비밀번호는 최소 6자 이상이어야 합니다')
    return
  }

  loading.value = true

  try {
    const result = await register(form.email, form.username, form.password)

    if (result.success) {
      toast.success('회원가입이 완료되었습니다. 로그인해주세요.')
      await navigateTo('/login')
    } else {
      toast.error(result.error || '회원가입에 실패했습니다')
    }
  } catch (error) {
    toast.error('회원가입 중 오류가 발생했습니다')
  } finally {
    loading.value = false
  }
}
</script>
