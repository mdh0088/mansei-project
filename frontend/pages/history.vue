<template>
  <NuxtLayout>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">계산 기록</h1>
        <p class="text-gray-600 mt-2">
          이전에 계산한 만세력 결과들을 확인해보세요
        </p>
      </div>

      <!-- 기록이 없는 경우 -->
      <div v-if="history.length === 0" class="text-center py-12">
        <ClockIcon class="h-12 w-12 mx-auto mb-4 text-gray-300" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">
          아직 계산 기록이 없습니다
        </h3>
        <p class="text-gray-600 mb-6">
          첫 번째 만세력을 계산해보세요
        </p>
        <NuxtLink to="/calculate" class="btn-primary">
          만세력 계산하기
        </NuxtLink>
      </div>

      <!-- 계산 기록 목록 -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="result in history"
          :key="result.id"
          class="card hover:shadow-lg transition-shadow cursor-pointer"
          @click="navigateTo(`/result/${result.id}`)"
        >
          <!-- 기본 정보 -->
          <div class="mb-4">
            <h3 class="text-lg font-semibold">{{ result.name }}</h3>
            <p class="text-sm text-gray-600">
              {{ formatDate(result.created_at) }}
            </p>
          </div>

          <!-- 사주팔자 미리보기 -->
          <div class="grid grid-cols-4 gap-1 mb-4">
            <div class="text-center bg-gray-50 p-2 rounded text-xs">
              <p class="text-gray-600">연</p>
              <p class="font-mono font-semibold">{{ result.saju_pillars.year }}</p>
            </div>
            <div class="text-center bg-gray-50 p-2 rounded text-xs">
              <p class="text-gray-600">월</p>
              <p class="font-mono font-semibold">{{ result.saju_pillars.month }}</p>
            </div>
            <div class="text-center bg-gray-50 p-2 rounded text-xs">
              <p class="text-gray-600">일</p>
              <p class="font-mono font-semibold">{{ result.saju_pillars.day }}</p>
            </div>
            <div class="text-center bg-gray-50 p-2 rounded text-xs">
              <p class="text-gray-600">시</p>
              <p class="font-mono font-semibold">{{ result.saju_pillars.hour }}</p>
            </div>
          </div>

          <!-- 간단한 정보 -->
          <div class="flex justify-between items-center text-sm text-gray-600">
            <span>{{ getGenderText(result.gender) }}</span>
            <span>{{ result.birth_info.date }}</span>
          </div>

          <!-- 상세 보기 버튼 -->
          <div class="mt-4 pt-4 border-t border-gray-100">
            <button class="text-primary-600 hover:text-primary-700 text-sm font-medium">
              상세 결과 보기 →
            </button>
          </div>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { ClockIcon } from '@heroicons/vue/24/outline'

definePageMeta({
  middleware: 'auth'
})

const { history, fetchHistory } = useMansei()

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getGenderText = (gender: string) => {
  return gender === 'male' ? '남성' : '여성'
}

// 페이지 로드 시 기록 가져오기
onMounted(async () => {
  await fetchHistory()
})
</script>
