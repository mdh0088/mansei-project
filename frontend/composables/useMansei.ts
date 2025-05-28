export const useMansei = () => {
  const manseiStore = useManseiStore()
  
  const calculate = async (request: any) => {
    return await manseiStore.calculateMansei(request)
  }
  
  const fetchHistory = async () => {
    return await manseiStore.fetchHistory()
  }
  
  const getResult = async (id: number) => {
    return await manseiStore.getResult(id)
  }
  
  return {
    currentResult: computed(() => manseiStore.currentResult),
    history: computed(() => manseiStore.history),
    loading: computed(() => manseiStore.loading),
    hasResult: computed(() => manseiStore.hasResult),
    calculate,
    fetchHistory,
    getResult,
    clearResult: () => manseiStore.clearCurrentResult()
  }
}
