export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  
  const api = async (endpoint: string, options: any = {}) => {
    const url = `${config.public.apiBase}${endpoint}`
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    }
    
    try {
      const response = await $fetch(url, {
        ...defaultOptions,
        ...options
      })
      
      return response
    } catch (error: any) {
      console.error(`API Error [${endpoint}]:`, error)
      throw error
    }
  }
  
  return {
    provide: {
      api
    }
  }
})

