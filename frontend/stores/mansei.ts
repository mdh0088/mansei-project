import { defineStore } from 'pinia'

interface ManseiRequest {
  name: string
  gender: 'male' | 'female'
  calendar_type: 'solar' | 'lunar'
  month_type: 'regular' | 'leap'
  birth_date: string
  birth_time?: string
}

interface ManseiResult {
  id: number
  name: string
  gender: string
  birth_info: any
  saju_pillars: {
    year: string
    month: string
    day: string
    hour: string
  }
  lunar_info: any
  five_elements: Record<string, number>
  interpretation: any
  created_at: string
}

interface ManseiState {
  currentResult: ManseiResult | null
  history: ManseiResult[]
  loading: boolean
}

export const useManseiStore = defineStore('mansei', {
  state: (): ManseiState => ({
    currentResult: null,
    history: [],
    loading: false
  }),

  getters: {
    hasResult: (state) => !!state.currentResult,
    resultCount: (state) => state.history.length
  },

  actions: {
    async calculateMansei(request: ManseiRequest) {
      const { $api } = useNuxtApp()
      const authStore = useAuthStore()
      
      this.loading = true
      
      try {
        const result = await $api('/api/v1/mansei/calculate', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${authStore.token}`
          },
          body: request
        })
        
        this.currentResult = result
        this.history.unshift(result) // 최신 결과를 앞에 추가
        
        return { success: true, result }
      } catch (error: any) {
        console.error('Mansei calculation error:', error)
        return { 
          success: false, 
          error: error.data?.detail || '만세력 계산에 실패했습니다' 
        }
      } finally {
        this.loading = false
      }
    },

    async fetchHistory() {
      const { $api } = useNuxtApp()
      const authStore = useAuthStore()
      
      try {
        const history = await $api('/api/v1/mansei/history', {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        this.history = history
        return { success: true }
      } catch (error: any) {
        console.error('Fetch history error:', error)
        return { 
          success: false, 
          error: error.data?.detail || '기록 조회에 실패했습니다' 
        }
      }
    },

    async getResult(id: number) {
      const { $api } = useNuxtApp()
      const authStore = useAuthStore()
      
      try {
        const result = await $api(`/api/v1/mansei/${id}`, {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        
        this.currentResult = result
        return { success: true, result }
      } catch (error: any) {
        console.error('Get result error:', error)
        return { 
          success: false, 
          error: error.data?.detail || '결과 조회에 실패했습니다' 
        }
      }
    },

    clearCurrentResult() {
      this.currentResult = null
    }
  }
})
