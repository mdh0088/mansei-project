export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase
  
  const api = async (endpoint: string, options: any = {}) => {
    const url = `${baseURL}${endpoint}`
    
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
  
  return { api }
}
