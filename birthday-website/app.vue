<template>
  <div id="app">
    <!-- 极光背景 -->
    <div class="aurora-bg" />
    
    <!-- 粒子系统容器 -->
    <div class="particles-container" ref="particlesRef" />
    
    <!-- 主要内容 -->
    <NuxtPage />
    
    <!-- 音效管理器 -->
    <AudioManager />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 页面元数据
useHead({
  title: '木头的破壳日 💝',
  meta: [
    { name: 'description', content: '为木头准备的专属生日网站，充满爱意的数字空间' }
  ]
})

// 粒子系统引用
const particlesRef = ref(null)

onMounted(() => {
  // 初始化粒子系统
  initParticles()
})

// 粒子系统初始化
function initParticles() {
  if (!particlesRef.value) return
  
  // 这里将在后续实现Three.js粒子系统
  console.log('粒子系统准备就绪')
}
</script>

<style>
html {
  scroll-behavior: smooth;
}

#app {
  min-height: 100vh;
  position: relative;
}
</style>