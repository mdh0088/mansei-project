<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <NuxtLink to="/" class="text-xl font-bold text-primary-600">
              만세력 서비스
            </NuxtLink>
          </div>
          
          <div class="flex items-center space-x-4">
            <template v-if="isLoggedIn">
              <NuxtLink to="/dashboard" class="text-gray-700 hover:text-primary-600">
                대시보드
              </NuxtLink>
              <NuxtLink to="/calculate" class="text-gray-700 hover:text-primary-600">
                만세력 계산
              </NuxtLink>
              <NuxtLink to="/history" class="text-gray-700 hover:text-primary-600">
                계산 기록
              </NuxtLink>
              <div class="relative">
                <button @click="showUserMenu = !showUserMenu" 
                        class="flex items-center text-gray-700 hover:text-primary-600">
                  <span>{{ user?.username }}</span>
                  <ChevronDownIcon class="ml-1 h-4 w-4" />
                </button>
                
                <!-- User dropdown menu -->
                <div v-if="showUserMenu" 
                     class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                  <button @click="logout" 
                          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    로그아웃
                  </button>
                </div>
              </div>
            </template>
            
            <template v-else>
              <NuxtLink to="/login" class="text-gray-700 hover:text-primary-600">
                로그인
              </NuxtLink>
              <NuxtLink to="/register" class="btn-primary">
                회원가입
              </NuxtLink>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main>
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ChevronDownIcon } from '@heroicons/vue/24/outline'

const { user, isLoggedIn, logout } = useAuth()
const showUserMenu = ref(false)

// 클릭 외부 영역 감지하여 메뉴 닫기
onClickOutside(() => {
  showUserMenu.value = false
})
</script>
