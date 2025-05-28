<template>
  <NuxtLayout>
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 로딩 상태 -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>

      <!-- 결과가 없는 경우 -->
      <div v-else-if="!currentResult" class="text-center py-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">
          결과를 찾을 수 없습니다
        </h2>
        <NuxtLink to="/history" class="btn-primary">
          기록으로 돌아가기
        </NuxtLink>
      </div>

      <!-- 만세력 결과 표시 -->
      <div v-else class="space-y-8">
        <!-- 헤더 -->
        <div class="flex justify-between items-start">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">
              {{ currentResult.name }}님의 만세력
            </h1>
            <p class="text-gray-600 mt-2">
              {{ formatDate(currentResult.created_at) }} 계산됨
            </p>
          </div>
          <button
            @click="goBack"
            class="btn-secondary"
          >
            뒤로 가기
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- 기본 정보 -->
          <div class="card">
            <h2 class="text-xl font-semibold mb-4">기본 정보</h2>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600">이름:</span>
                <span class="font-medium">{{ currentResult.name }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">성별:</span>
                <span class="font-medium">{{ getGenderText(currentResult.gender) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">생년월일:</span>
                <span class="font-medium">{{ currentResult.birth_info.date }}</span>
              </div>
              <div v-if="currentResult.birth_info.time" class="flex justify-between">
                <span class="text-gray-600">출생시간:</span>
                <span class="font-medium">{{ currentResult.birth_info.time }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">달력:</span>
                <span class="font-medium">
                  {{ currentResult.birth_info.calendar_type === 'solar' ? '양력' : '음력' }}
                  {{ currentResult.birth_info.month_type === 'leap' ? '(윤달)' : '' }}
                </span>
              </div>
            </div>
          </div>

          <!-- 사주팔자 -->
          <div class="card">
            <h2 class="text-xl font-semibold mb-4">사주팔자</h2>
            <div class="grid grid-cols-4 gap-4">
              <div class="text-center">
                <div class="bg-primary-50 border-2 border-primary-200 rounded-lg p-4">
                  <p class="text-sm text-gray-600 mb-2">연주</p>
                  <p class="font-mono text-2xl font-bold text-primary-700">
                    {{ currentResult.saju_pillars.year }}
                  </p>
                </div>
              </div>
              <div class="text-center">
                <div class="bg-green-50 border-2 border-green-200 rounded-lg p-4">
                  <p class="text-sm text-gray-600 mb-2">월주</p>
                  <p class="font-mono text-2xl font-bold text-green-700">
                    {{ currentResult.saju_pillars.month }}
                  </p>
                </div>
              </div>
              <div class="text-center">
                <div class="bg-yellow-50 border-2 border-yellow-200 rounded-lg p-4">
                  <p class="text-sm text-gray-600 mb-2">일주</p>
                  <p class="font-mono text-2xl font-bold text-yellow-700">
                    {{ currentResult.saju_pillars.day }}
                  </p>
                </div>
              </div>
              <div class="text-center">
                <div class="bg-purple-50 border-2 border-purple-200 rounded-lg p-4">
                  <p class="text-sm text-gray-600 mb-2">시주</p>
                  <p class="font-mono text-2xl font-bold text-purple-700">
                    {{ currentResult.saju_pillars.hour }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 오행 분석 -->
        <div class="card">
          <h2 class="text-xl font-semibold mb-4">오행 분석</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 class="font-medium mb-4">오행 분포</h3>
              <div class="space-y-3">
                <div v-for="(count, element) in currentResult.five_elements" 
                     :key="element" 
                     class="flex items-center">
                  <div class="w-12 text-center font-medium">{{ element }}</div>
                  <div class="flex-1 mx-4">
                    <div class="w-full bg-gray-200 rounded-full h-3">
                      <div 
                        :class="getElementColor(element)"
                        class="h-3 rounded-full transition-all duration-500"
                        :style="{ width: `${(count / Math.max(...Object.values(currentResult.five_elements))) * 100}%` }"
                      ></div>
                    </div>
                  </div>
                  <div class="w-8 text-center font-bold">{{ count }}</div>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="font-medium mb-4">균형 분석</h3>
              <div class="space-y-2 text-sm">
                <p>
                  <span class="font-medium">가장 강한 오행:</span> 
                  {{ currentResult.interpretation.five_elements_balance.strongest }}
                </p>
                <p>
                  <span class="font-medium">가장 약한 오행:</span> 
                  {{ currentResult.interpretation.five_elements_balance.weakest }}
                </p>
                <p class="text-gray-600 mt-2">
                  {{ currentResult.interpretation.five_elements_balance.analysis }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- 해석 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- 성격 특성 -->
          <div class="card">
            <h2 class="text-xl font-semibold mb-4">성격 특성</h2>
            <div class="mb-4">
              <h3 class="font-medium mb-2">일간 특성</h3>
              <p class="text-sm text-gray-600 mb-2">
                {{ currentResult.interpretation.day_master.description }}
              </p>
              <p class="text-xs text-gray-500">
                일간: {{ currentResult.interpretation.day_master.stem }} 
                ({{ currentResult.interpretation.day_master.element }}, 
                {{ currentResult.interpretation.day_master.yin_yang }})
              </p>
            </div>
            
            <div>
              <h3 class="font-medium mb-2">주요 특징</h3>
              <ul class="space-y-1">
                <li v-for="trait in currentResult.interpretation.general_traits" 
                    :key="trait"
                    class="text-sm text-gray-700 flex items-start">
                  <span class="text-primary-500 mr-2">•</span>
                  {{ trait }}
                </li>
              </ul>
            </div>
          </div>

          <!-- 조언 및 권장사항 -->
          <div class="card">
            <h2 class="text-xl font-semibold mb-4">조언 및 권장사항</h2>
            <div class="space-y-3">
              <div v-for="recommendation in currentResult.interpretation.recommendations" 
                   :key="recommendation"
                   class="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p class="text-sm text-blue-800">{{ recommendation }}</p>
              </div>
            </div>
            
            <div class="mt-6 p-4 bg-gray-50 rounded-lg">
              <p class="text-xs text-gray-600">
                ※ 이 해석은 전통 명리학을 바탕으로 한 기본적인 분석입니다. 
                더 정확하고 상세한 해석을 원하시면 전문가와 상담하시기 바랍니다.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

const route = useRoute()
const { getResult, currentResult, loading } = useMansei()

const resultId = computed(() => parseInt(route.params.id as string))

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getGenderText = (gender: string) => {
  return gender === 'male' ? '남성' : '여성'
}

const getElementColor = (element: string) => {
  const colors = {
    '목': 'bg-green-500',
    '화': 'bg-red-500', 
    '토': 'bg-yellow-500',
    '금': 'bg-gray-500',
    '수': 'bg-blue-500'
  }
  return colors[element as keyof typeof colors] || 'bg-gray-300'
}

const goBack = () => {
  window.history.back()
}

// 페이지 로드 시 결과 가져오기
onMounted(async () => {
  if (resultId.value) {
    await getResult(resultId.value)
  }
})
</script>
