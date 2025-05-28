<template>
  <NuxtLayout>
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">만세력 계산</h1>
        <p class="text-gray-600 mt-2">
          정확한 정보를 입력하여 사주팔자를 계산해보세요
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- 입력 폼 -->
        <div class="card">
          <h2 class="text-xl font-semibold mb-6">기본 정보 입력</h2>

          <form @submit.prevent="handleCalculate" class="space-y-6">
            <!-- 이름 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                이름 *
              </label>
              <input
                  v-model="form.name"
                  type="text"
                  required
                  class="input-field"
                  placeholder="이름을 입력하세요"
              />
            </div>

            <!-- 성별 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                성별 *
              </label>
              <el-radio-group v-model="form.gender">
                <el-radio value="male">남성</el-radio>
                <el-radio value="female">여성</el-radio>
              </el-radio-group>
            </div>

            <!-- 달력 유형 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                달력 유형 *
              </label>
              <el-radio-group v-model="form.calendar_type">
                <el-radio value="solar">양력</el-radio>
                <el-radio value="lunar">음력</el-radio>
              </el-radio-group>
            </div>

            <!-- 월 유형 (음력일 때만) -->
            <div v-if="form.calendar_type === 'lunar'">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                월 유형
              </label>
              <el-radio-group v-model="form.month_type">
                <el-radio value="regular">평달</el-radio>
                <el-radio value="leap">윤달</el-radio>
              </el-radio-group>
            </div>

            <!-- 생년월일 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                생년월일 *
              </label>
              <input
                  v-model="form.birth_date"
                  type="date"
                  required
                  class="input-field"
              />
            </div>

            <!-- 출생시간 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                출생시간 (선택사항)
              </label>
              <input
                  v-model="form.birth_time"
                  type="time"
                  class="input-field"
              />
              <p class="text-xs text-gray-500 mt-1">
                정확한 시간을 모르는 경우 비워두시면 정오(12:00)로 계산됩니다
              </p>
            </div>

            <!-- 제출 버튼 -->
            <el-button
                type="primary"
                native-type="submit"
                :loading="loading"
                class="w-full !h-12"
                size="large"
            >
              <span v-if="loading">계산 중...</span>
              <span v-else>만세력 계산하기</span>
            </el-button>
          </form>
        </div>

        <!-- 계산 결과 미리보기 -->
        <div class="card">
          <h2 class="text-xl font-semibold mb-6">계산 결과</h2>

          <div v-if="!hasResult" class="text-center text-gray-500 py-12">
            <CalendarIcon class="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p>왼쪽 폼을 작성하여 만세력을 계산해보세요</p>
          </div>

          <!-- 계산 결과 표시 -->
          <div v-else class="space-y-6">
            <!-- 기본 정보 -->
            <div>
              <h3 class="font-semibold mb-2">기본 정보</h3>
              <div class="bg-gray-50 p-4 rounded-lg">
                <p><span class="font-medium">이름:</span> {{ currentResult?.name }}</p>
                <p><span class="font-medium">성별:</span> {{ getGenderText(currentResult?.gender) }}</p>
                <p><span class="font-medium">생년월일:</span> {{ currentResult?.birth_info.date }}</p>
                <p v-if="currentResult?.birth_info.time">
                  <span class="font-medium">출생시간:</span> {{ currentResult?.birth_info.time }}
                </p>
              </div>
            </div>

            <!-- 사주팔자 -->
            <div>
              <h3 class="font-semibold mb-2">사주팔자</h3>
              <div class="grid grid-cols-4 gap-2">
                <div class="text-center bg-gray-50 p-3 rounded">
                  <p class="text-xs text-gray-600">연주</p>
                  <p class="font-mono text-lg font-bold">{{ currentResult?.saju_pillars.year }}</p>
                </div>
                <div class="text-center bg-gray-50 p-3 rounded">
                  <p class="text-xs text-gray-600">월주</p>
                  <p class="font-mono text-lg font-bold">{{ currentResult?.saju_pillars.month }}</p>
                </div>
                <div class="text-center bg-gray-50 p-3 rounded">
                  <p class="text-xs text-gray-600">일주</p>
                  <p class="font-mono text-lg font-bold">{{ currentResult?.saju_pillars.day }}</p>
                </div>
                <div class="text-center bg-gray-50 p-3 rounded">
                  <p class="text-xs text-gray-600">시주</p>
                  <p class="font-mono text-lg font-bold">{{ currentResult?.saju_pillars.hour }}</p>
                </div>
              </div>
            </div>

            <!-- 오행 분석 -->
            <div>
              <h3 class="font-semibold mb-2">오행 분석</h3>
              <div class="space-y-2">
                <div v-for="(count, element) in currentResult?.five_elements"
                     :key="element"
                     class="flex items-center justify-between">
                  <span>{{ element }}</span>
                  <div class="flex items-center">
                    <div class="w-20 bg-gray-200 rounded-full h-2 mr-2">
                      <div
                          :class="getElementColor(element)"
                          class="h-2 rounded-full transition-all duration-300"
                          :style="{ width: `${(count / Math.max(...Object.values(currentResult?.five_elements || {}))) * 100}%` }"
                      ></div>
                    </div>
                    <span class="text-sm font-medium">{{ count }}</span>
                  </div>
                </div>
              </div>
            </div>

            <NuxtLink
                v-if="currentResult"
                :to="`/result/${currentResult.id}`"
                class="btn-primary w-full text-center block"
            >
              상세 결과 보기
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { CalendarIcon } from '@heroicons/vue/24/outline'

definePageMeta({
  middleware: 'auth'
})

const { calculate, currentResult, hasResult, loading } = useMansei()
const toast = useToast()

const form = reactive({
  name: '',
  gender: 'male',
  calendar_type: 'solar',
  month_type: 'regular',
  birth_date: '',
  birth_time: ''
})

const handleCalculate = async () => {
  // 필수 필드 검증
  if (!form.name || !form.gender || !form.birth_date) {
    toast.error('필수 정보를 모두 입력해주세요')
    return
  }

  try {
    const result = await calculate(form)

    if (result.success) {
      toast.success('만세력 계산이 완료되었습니다')
    } else {
      toast.error(result.error || '계산에 실패했습니다')
    }
  } catch (error) {
    toast.error('계산 중 오류가 발생했습니다')
  }
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
</script>
