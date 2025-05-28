import { defineStore } from 'pinia'

interface User {
  id: number
  email: string
  username: string
  is_active: boolean
  created_at: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
    isAuthenticated: false
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated && !!state.token
  },

  actions: {
    setAuth(token: string, user: User) {
      this.token = token
      this.user = user
      this.isAuthenticated = true
      
      // 토큰을 localStorage에 저장
      if (process.client) {
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(user))
      }
    },

    clearAuth() {
      this.token = null
      this.user = null
      this.isAuthenticated = false
      
      // localStorage에서 제거
      if (process.client) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      }
    },

    initializeAuth() {
      if (process.client) {
        const token = localStorage.getItem('token')
        const userStr = localStorage.getItem('user')
        
        if (token && userStr) {
          try {
            const user = JSON.parse(userStr)
            this.setAuth(token, user)
          } catch (error) {
            console.error('Failed to parse user data:', error)
            this.clearAuth()
          }
        }
      }
    },

    async login(email: string, password: string) {
      const { $api } = useNuxtApp()
      
      try {
        const response = await $api('/api/v1/auth/login', {
          method: 'POST',
          body: { email, password }
        })
        
        // 사용자 정보 가져오기
        const userResponse = await $api('/api/v1/auth/me', {
          headers: {
            Authorization: `Bearer ${response.access_token}`
          }
        })
        
        this.setAuth(response.access_token, userResponse)
        
        return { success: true }
      } catch (error: any) {
        console.error('Login error:', error)
        return { 
          success: false, 
          error: error.data?.detail || '로그인에 실패했습니다' 
        }
      }
    },

    async register(email: string, username: string, password: string) {
      const { $api } = useNuxtApp()
      
      try {
        await $api('/api/v1/auth/register', {
          method: 'POST',
          body: { email, username, password }
        })
        
        return { success: true }
      } catch (error: any) {
        console.error('Register error:', error)
        return { 
          success: false, 
          error: error.data?.detail || '회원가입에 실패했습니다' 
        }
      }
    },

    logout() {
      this.clearAuth()
      navigateTo('/login')
    }
  }
})
