export const useAuth = () => {
  const authStore = useAuthStore()
  
  const login = async (email: string, password: string) => {
    return await authStore.login(email, password)
  }
  
  const register = async (email: string, username: string, password: string) => {
    return await authStore.register(email, username, password)
  }
  
  const logout = () => {
    authStore.logout()
  }
  
  const requireAuth = () => {
    if (!authStore.isLoggedIn) {
      navigateTo('/login')
      return false
    }
    return true
  }
  
  return {
    user: computed(() => authStore.user),
    isLoggedIn: computed(() => authStore.isLoggedIn),
    login,
    register,
    logout,
    requireAuth
  }
}
