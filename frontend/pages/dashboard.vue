<template>
  <NuxtLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">
          안녕하세요, {{ user?.username }}님!
        </h1>
        <p class="text-gray-600 mt-2">
          만세력 계산 서비스 대시보드입니다
        </p>
      </div>

      <!-- 통계 카드 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="card">
          <div class="flex items-center">
            <div class="bg-primary-100 rounded-full p-3">
              <ChartBarIcon class="h-6 w-6 text-primary-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">총 계산 횟수</p>
              <p class="text-2xl font-bold text-gray-900">{{ historyCount }}</p>
            </div>
          </div>
        </div>
        
        <div class="card">
          <div class="flex items-center">
            <div class="bg-green-100 rounded-full p-3">
              <ClockIcon class="h-6 w-6 text-green-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">최근 계산</p>
              <p class="text-lg font-semibold text-gray-900">
                {{ lastCalculation || '없음' }}
              </p>
            </div>
          </div>
        </div>
        
        <div class="card">
          <div class="flex items-center">
            <div class="bg-purple-100 rounded-full p-3">
              <UserIcon class="h-6 w-6 text-purple-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">회원 가입일</p>
              <p class="text-lg font-semibold text-gray-900">
                {{ formatDate(user?.created_at) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- 빠른 액션 버튼 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">새로운 만세력 계산</h3>
          <p class="text-gray-600 mb-4">
            정확한 생년월일과 시간을 입력하여 사주팔자를 계산해보세요
          </p>
          <NuxtLink to="/calculate" class="btn-primary">
            만세력 계산하기
          </NuxtLink>
        </div>
        
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">계산 기록 보기</h3>
          <p class="text-gray-600 mb-4">
            이전에 계산한 만세력 결과들을 다시 확인해보세요
          </p>
          <NuxtLink to="/history" class="btn-secondary">
            기록 보기
          </NuxtLink>
        </div>
      </div>

      <!-- 최근 계산 결과 -->
      <div class="card" v-if="recentResults.length > 0">
        <h3 class="text-lg font-semibold mb-4">최근 계산 결과</h3>
        <div class="space-y-4">
          <div
            v-for="result in recentResults.slice(0, 3)"
            :key="result.id"
            class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
          >
            <div>
              <p class="font-medium">{{ result.name }}</p>
              <p class="text-sm text-gray-600">
                {{ formatDate(result.created_at) }}
              </p>
            </div>
            <div class="text-right">
              <p class="text-sm text-gray-600">사주:</p>
              <p class="font-mono text-sm">
                {{ Object.values(result.saju_pillars).join(' ') }}
              </p>
            </div>
            <NuxtLink
              :to="`/result/${result.id}`"
              class="text-primary-600 hover:text-primary-700 text-sm font-medium"
            >
              자세히 보기
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { ChartBarIcon, ClockIcon, UserIcon } from '@heroicons/vue/24/outline'

definePageMeta({
  middleware: 'auth'
})

const { user } = useAuth()
const { history, fetchHistory } = useMansei()

const recentResults = computed(() => history.value)
const historyCount = computed(() => history.value.length)
const lastCalculation = computed(() => {
  if (history.value.length > 0) {
    return formatDate(history.value[0].created_at)
  }
  return null
})

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('ko-KR')
}

// 페이지 로드 시 기록 가져오기
onMounted(async () => {
  await fetchHistory()
})
</script>
