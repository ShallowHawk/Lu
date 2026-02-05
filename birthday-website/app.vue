<template>
  <div id="app">
    <!-- 紫藤花装饰 (顶部) -->
    <div class="wisteria-decoration"></div>
    
    <!-- 粒子系统容器 (保留樱花效果) -->
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
  title: '木头的破壳日 🌸',
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

// 粒子系统初始化 (保留樱花飘落)
function initParticles() {
  if (!particlesRef.value) return
  
  // 简单的樱花生成器
  setInterval(() => {
    createSakura()
  }, 1000)
}

function createSakura() {
  if (!particlesRef.value) return
  
  const sakura = document.createElement('div')
  sakura.innerHTML = '🌸'
  sakura.className = 'sakura-particle'
  sakura.style.left = Math.random() * 100 + 'vw'
  sakura.style.animationDuration = Math.random() * 5 + 5 + 's'
  sakura.style.fontSize = Math.random() * 10 + 10 + 'px'
  
  particlesRef.value.appendChild(sakura)
  
  setTimeout(() => {
    sakura.remove()
  }, 10000)
}
</script>

<style lang="scss">
html {
  scroll-behavior: smooth;
}

#app {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

// 紫藤花装饰
.wisteria-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 120px;
  z-index: 10;
  pointer-events: none;
  background-image: radial-gradient(circle at 50% 0, #A59ACA 10px, transparent 15px),
                    radial-gradient(circle at 30% 0, #A59ACA 8px, transparent 12px),
                    radial-gradient(circle at 70% 0, #A59ACA 12px, transparent 18px),
                    linear-gradient(to bottom, #A59ACA 2px, transparent 2px);
  background-size: 100px 100px, 120px 80px, 90px 120px, 20px 20px;
  background-repeat: repeat-x;
  opacity: 0.8;
  
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 150px;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'%3E%3Cpath d='M0,0 Q25,50 50,0 T100,0' fill='none' stroke='%23A59ACA' stroke-width='2' opacity='0.5'/%3E%3C/svg%3E");
    background-size: 200px 100px;
  }
}

.particles-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.sakura-particle {
  position: absolute;
  top: -20px;
  animation: fall linear forwards;
  opacity: 0.7;
}

@keyframes fall {
  to {
    transform: translateY(100vh) rotate(360deg);
  }
}
</style>
