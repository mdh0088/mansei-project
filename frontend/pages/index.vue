<template>
  <NuxtLayout>
    <div class="min-h-screen">
      <!-- Hero Section -->
      <section class="bg-gradient-to-br from-primary-50 to-indigo-100 py-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center">
            <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              만세력 계산 서비스
            </h1>
            <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              한국 전통 명리학을 바탕으로 정확한 사주팔자를 계산하고 
              개인 맞춤형 해석을 제공합니다
            </p>
            
            <div class="space-x-4">
              <NuxtLink v-if="!isLoggedIn" to="/register" 
                       class="btn-primary text-lg px-8 py-3">
                무료로 시작하기
              </NuxtLink>
              <NuxtLink v-else to="/calculate" 
                       class="btn-primary text-lg px-8 py-3">
                만세력 계산하기
              </NuxtLink>
              <NuxtLink to="/about" 
                       class="btn-secondary text-lg px-8 py-3">
                더 알아보기
              </NuxtLink>
            </div>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">
              왜 우리 서비스를 선택해야 할까요?
            </h2>
            <p class="text-lg text-gray-600">
              정통 명리학 이론을 바탕으로 한 정확하고 상세한 분석
            </p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="text-center">
              <div class="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <CalendarIcon class="h-8 w-8 text-primary-600" />
              </div>
              <h3 class="text-xl font-semibold mb-2">정확한 계산</h3>
              <p class="text-gray-600">
                전통 갑자체계를 바탕으로 한 정확한 사주팔자 계산
              </p>
            </div>
            
            <div class="text-center">
              <div class="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <ChartBarIcon class="h-8 w-8 text-primary-600" />
              </div>
              <h3 class="text-xl font-semibold mb-2">상세한 분석</h3>
              <p class="text-gray-600">
                오행 균형 분석과 개인 맞춤형 해석 제공
              </p>
            </div>
            
            <div class="text-center">
              <div class="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <ClockIcon class="h-8 w-8 text-primary-600" />
              </div>
              <h3 class="text-xl font-semibold mb-2">기록 관리</h3>
              <p class="text-gray-600">
                계산 결과를 안전하게 저장하고 언제든 다시 확인
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { CalendarIcon, ChartBarIcon, ClockIcon } from '@heroicons/vue/24/outline'

const { isLoggedIn } = useAuth()

useSeoMeta({
  title: '만세력 계산 서비스 - 정통 사주팔자 분석',
  description: '한국 전통 명리학을 바탕으로 정확한 사주팔자를 계산하고 개인 맞춤형 해석을 제공하는 만세력 서비스'
})
</script>
