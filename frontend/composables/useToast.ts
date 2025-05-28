import { ElMessage } from 'element-plus'

export const useToast = () => {
  const toast = {
    success: (message: string) => {
      ElMessage({
        message,
        type: 'success',
        duration: 3000,
        showClose: true
      })
    },

    error: (message: string) => {
      ElMessage({
        message,
        type: 'error',
        duration: 5000,
        showClose: true
      })
    },

    info: (message: string) => {
      ElMessage({
        message,
        type: 'info',
        duration: 3000,
        showClose: true
      })
    },

    warning: (message: string) => {
      ElMessage({
        message,
        type: 'warning',
        duration: 4000,
        showClose: true
      })
    }
  }

  return toast
}
