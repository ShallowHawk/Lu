export default defineNuxtConfig({
  compatibilityDate: '2025-07-14',
  devtools: { enabled: true },
  css: ['~/assets/css/main.scss'],
  
  // 静态网站生成配置
  nitro: {
    preset: 'static'
  },
  
  // 确保静态生成
  ssr: false,
  modules: [
    '@nuxtjs/google-fonts',
    '@hypernym/nuxt-gsap'
  ],
  gsap: {
    extraPlugins: {
      scrollTrigger: true,
      scrollTo: true
    }
  },
  googleFonts: {
    families: {
      'Noto+Serif+SC': [400, 700],
      'PingFang+SC': [300, 400, 500, 600],
      'Abril+Fatface': [400],
      'ZCOOL+KuaiLe': [400],
      'Long+Cang': [400]
    }
  },
  app: {
    head: {
      title: '木头的破壳日 💝',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: '为木头准备的专属生日网站' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    }
  },
  build: {
    transpile: ['three', 'naive-ui']
  }
})