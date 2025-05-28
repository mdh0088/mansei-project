export default defineNuxtConfig({
  devtools: { enabled: true },

  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@element-plus/nuxt'
  ],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  },

  css: ['~/assets/css/main.css'],

  app: {
    head: {
      title: '만세력 계산 서비스',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: '한국 전통 명리학 기반 만세력 계산 서비스' }
      ]
    }
  },

  ssr: false,

  elementPlus: {
    /** Options */
  }
})
