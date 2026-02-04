<template>
  <div class="loading-screen" :class="{ 'fade-out': isComplete }">
    <!-- 瀑布流照片墙背景 -->
    <div class="photo-gallery-bg" ref="photoGalleryRef">
      <div class="waterfall-container" v-if="displayPhotos.length > 0">
        <div 
          v-for="(photo, index) in displayPhotos" 
          :key="photo.id"
          class="waterfall-item"
          :style="{
            animationDelay: `${photo.delay}s`,
            width: `${photo.width}px`,
            height: `${photo.height}px`
          }"
        >
          <img 
            :src="photo.url" 
            :alt="photo.filename"
            class="waterfall-image"
            @load="onImageLoad"
            @error="onImageError"
          />
        </div>
      </div>
    </div>
    
    <!-- 樱花粒子背景 -->
    <div class="sakura-particles" ref="sakuraRef" />
    
    <!-- 中心加载内容 -->
    <div class="loading-content">
      <!-- 打字机效果文案 -->
      <div class="typewriter-text">
        <h1 class="main-title">{{ currentText }}</h1>
        <div class="cursor" :class="{ 'blink': showCursor }">|</div>
      </div>
      
      <!-- 心跳进度指示器 -->
      <div class="progress-container">
        <div class="hearts-progress">
          <div class="heart left-heart" :style="{ transform: `translateX(${leftHeartPosition}px)` }">
            💕
          </div>
          <div class="heart right-heart" :style="{ transform: `translateX(${rightHeartPosition}px)` }">
            💝
          </div>
        </div>
        
        <!-- 进度条 -->
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${progress}%` }" />
        </div>
        
        <p class="progress-text">{{ Math.round(progress) }}%</p>
      </div>
    </div>
    
    <!-- 音频元素 -->
    <audio ref="audioRef" loop style="display: none;">
      <source src="/audio/loading-bgm.mp3" type="audio/mpeg">
    </audio>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { gsap } from 'gsap'
import { usePhotoGallery } from '~/composables/usePhotoGallery'

// Props 和 Emits
const emit = defineEmits(['loading-complete'])

// 响应式状态
const isComplete = ref(false)
const progress = ref(0)
const currentTextIndex = ref(0)
const currentCharIndex = ref(0)
const showCursor = ref(true)

// 引用
const photoGalleryRef = ref(null)
const sakuraRef = ref(null)
const audioRef = ref(null)

// 照片墙功能
const { photos, hasPhotos, loadPhotos } = usePhotoGallery()
const displayPhotos = ref([])
const loadedImagesCount = ref(0)

// 文案数组
const texts = [
  '正在收集我们的甜蜜瞬间...',
  '每一张照片都是一个故事...',
  '回忆在瀑布流中缓缓展开...',
  '准备进入我们的专属世界...',
  '载入完成，欢迎来到木头的破壳日！'
]

// 计算属性
const currentText = computed(() => {
  const text = texts[currentTextIndex.value] || ''
  return text.slice(0, currentCharIndex.value)
})

const leftHeartPosition = computed(() => {
  return -200 + (progress.value / 100) * 180
})

const rightHeartPosition = computed(() => {
  return 200 - (progress.value / 100) * 180
})

// 存储防抖后的resize函数以便清理
let debouncedResize = null

// 防抖函数
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// 生命周期
onMounted(async () => {
  // 先加载照片
  await loadPhotos()
  
  // 初始化瀑布流
  initWaterfallGallery()
  
  // 开始其他加载效果
  startLoading()
  initSakuraParticles()
  
  // 监听窗口大小变化，重新计算布局
  debouncedResize = debounce(initWaterfallGallery, 300)
  window.addEventListener('resize', debouncedResize)
})

// 清理资源
onUnmounted(() => {
  if (debouncedResize) {
    window.removeEventListener('resize', debouncedResize)
  }
})

// 监听进度变化
watch(progress, (newProgress) => {
  if (newProgress >= 100) {
    completeLoading()
  }
})

// 方法
function startLoading() {
  // 开始打字机效果
  typewriterEffect()
  
  // 开始进度动画
  gsap.to(progress, {
    value: 100,
    duration: 8,
    ease: "power2.inOut",
    onUpdate: () => {
      // 心跳效果
      if (progress.value > 0) {
        animateHeartbeat()
      }
    }
  })
  
  // 光标闪烁
  setInterval(() => {
    showCursor.value = !showCursor.value
  }, 500)
}

function typewriterEffect() {
  const currentTextContent = texts[currentTextIndex.value]
  
  if (currentCharIndex.value < currentTextContent.length) {
    currentCharIndex.value++
    setTimeout(typewriterEffect, 100)
  } else {
    // 当前文本完成，等待一段时间后切换到下一个
    setTimeout(() => {
      if (currentTextIndex.value < texts.length - 1) {
        currentTextIndex.value++
        currentCharIndex.value = 0
        typewriterEffect()
      }
    }, 1500)
  }
}

function animateHeartbeat() {
  const hearts = document.querySelectorAll('.heart')
  hearts.forEach(heart => {
    gsap.to(heart, {
      scale: 1.2,
      duration: 0.1,
      yoyo: true,
      repeat: 1,
      ease: "power2.inOut"
    })
  })
}

function initSakuraParticles() {
  if (!sakuraRef.value) return
  
  // 创建樱花粒子
  for (let i = 0; i < 50; i++) {
    createSakuraPetal()
  }
}

function createSakuraPetal() {
  const petal = document.createElement('div')
  petal.className = 'sakura-petal'
  petal.innerHTML = '🌸'
  
  // 随机位置和大小
  const size = Math.random() * 20 + 10
  petal.style.fontSize = `${size}px`
  petal.style.left = `${Math.random() * 100}%`
  petal.style.animationDelay = `${Math.random() * 10}s`
  petal.style.animationDuration = `${Math.random() * 5 + 8}s`
  
  sakuraRef.value?.appendChild(petal)
  
  // 动画完成后移除元素
  setTimeout(() => {
    if (petal.parentNode) {
      petal.parentNode.removeChild(petal)
    }
  }, 13000)
}

function initWaterfallGallery() {
  if (!hasPhotos.value || photos.value.length === 0) {
    console.log('没有找到照片，使用默认动画')
    return
  }
  
  // 动态计算需要的照片数量以填满屏幕
  const screenWidth = window.innerWidth
  const screenHeight = window.innerHeight
  const itemSize = screenWidth > 768 ? 180 : 120 // 根据屏幕调整单个item大小
  const cols = Math.floor(screenWidth / itemSize)
  const rows = Math.ceil(screenHeight / itemSize) + 1 // 多一行确保填满
  const neededPhotos = Math.min(cols * rows, photos.value.length)
  
  console.log(`屏幕尺寸: ${screenWidth}x${screenHeight}, 需要照片数量: ${neededPhotos}`)
  
  // 如果照片不够，复制现有照片来填充
  const availablePhotos = [...photos.value]
  while (availablePhotos.length < neededPhotos && photos.value.length > 0) {
    availablePhotos.push(...photos.value)
  }
  
  // 如果仍然没有足够的照片，至少确保有一些填充
  const finalPhotoCount = Math.max(availablePhotos.length, Math.min(neededPhotos, 20))
  
  // 选择要展示的照片
  displayPhotos.value = availablePhotos.slice(0, finalPhotoCount).map((photo, index) => {
    // 添加随机大小变化使布局更自然
    const baseSize = itemSize
    const sizeVariation = Math.random() * 40 - 20 // -20到+20的随机变化
    const finalSize = Math.max(baseSize + sizeVariation, baseSize * 0.8) // 确保最小尺寸
    
    return {
      ...photo,
      id: `${photo.id}-${index}`, // 确保唯一ID
      delay: index * 0.1, // 减少延迟让动画更快
      width: finalSize,
      height: finalSize * (0.8 + Math.random() * 0.4), // 随机高宽比
    }
  })
  
  console.log(`初始化瀑布流照片墙，展示 ${displayPhotos.value.length} 张照片`)
  
  // 启动瀑布流动画
  nextTick(() => {
    animateWaterfall()
  })
}

function animateWaterfall() {
  const items = document.querySelectorAll('.waterfall-item')
  
  items.forEach((item, index) => {
    // 初始状态：隐藏并位移
    gsap.set(item, {
      opacity: 0,
      y: 100,
      scale: 0.8,
      rotation: Math.random() * 20 - 10 // 随机旋转 -10到10度
    })
    
    // 动画进入
    gsap.to(item, {
      opacity: 1,
      y: 0,
      scale: 1,
      rotation: 0,
      duration: 0.8,
      delay: index * 0.1,
      ease: "back.out(1.7)",
      onComplete: () => {
        // 添加鼠标悬停效果
        item.addEventListener('mouseenter', () => {
          gsap.to(item, {
            scale: 1.05,
            rotation: Math.random() * 10 - 5,
            duration: 0.3,
            ease: "power2.out"
          })
        })
        
        item.addEventListener('mouseleave', () => {
          gsap.to(item, {
            scale: 1,
            rotation: 0,
            duration: 0.3,
            ease: "power2.out"
          })
        })
      }
    })
    
    // 持续的浮动动画
    gsap.to(item, {
      y: "+=20",
      duration: 3 + Math.random() * 2,
      yoyo: true,
      repeat: -1,
      ease: "sine.inOut",
      delay: Math.random() * 2
    })
  })
}

function onImageLoad() {
  loadedImagesCount.value++
  
  // 当大部分图片加载完成时，可以优化进度显示
  if (loadedImagesCount.value >= Math.floor(displayPhotos.value.length * 0.8)) {
    console.log('照片加载完成')
  }
}

function onImageError(event) {
  console.warn('图片加载失败:', event.target.src)
  // 可以设置默认图片或隐藏该项
  event.target.style.display = 'none'
}

function completeLoading() {
  isComplete.value = true
  
  // 淡出动画
  gsap.to('.loading-screen', {
    opacity: 0,
    duration: 1,
    ease: "power2.inOut",
    onComplete: () => {
      emit('loading-complete')
    }
  })
  
  // 停止音频
  if (audioRef.value) {
    audioRef.value.pause()
  }
}
</script>

<style scoped lang="scss">
.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary-start) 0%, var(--primary-end) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  transition: opacity 1s ease-in-out;
  
  &.fade-out {
    opacity: 0;
    pointer-events: none;
  }
}

.photo-gallery-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.15;
  overflow: hidden;
}

.waterfall-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 15px;
  align-content: start;
  justify-content: center;
  
  // 确保填满整个容器
  &::after {
    content: '';
    grid-column: 1 / -1;
    height: 20px; // 底部填充
  }
}

.waterfall-item {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
    background: rgba(255, 255, 255, 0.15);
  }
}

.waterfall-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: scale(1.02);
  }
}

.sakura-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
}

.sakura-petal {
  position: absolute;
  animation: sakura-fall linear infinite;
  opacity: 0.7;
}

@keyframes sakura-fall {
  0% {
    transform: translateY(-100px) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(calc(100vh + 100px)) rotate(360deg);
    opacity: 0;
  }
}

.loading-content {
  text-align: center;
  color: white;
  z-index: 10;
  position: relative;
}

.typewriter-text {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 40px;
  min-height: 60px;
  
  .main-title {
    font-family: var(--font-heading);
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    font-weight: 400;
    margin: 0;
  }
  
  .cursor {
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    margin-left: 4px;
    transition: opacity 0.1s;
    
    &.blink {
      opacity: 0;
    }
  }
}

.progress-container {
  max-width: 400px;
  margin: 0 auto;
}

.hearts-progress {
  position: relative;
  height: 40px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.heart {
  position: absolute;
  font-size: 24px;
  transition: transform 0.3s ease;
  filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.5));
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 16px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #FFB6C1, #FF6B6B);
  border-radius: 2px;
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(255, 182, 193, 0.5);
}

.progress-text {
  font-family: var(--font-display);
  font-size: 1.2rem;
  margin: 0;
  opacity: 0.9;
}

// 响应式设计
@media (max-width: 768px) {
  .loading-content {
    padding: 0 20px;
  }
  
  .hearts-progress {
    height: 30px;
  }
  
  .heart {
    font-size: 20px;
  }
  
  .waterfall-container {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 12px;
    padding: 15px;
  }
  
  .waterfall-item {
    border-radius: 8px;
  }
}

@media (max-width: 480px) {
  .waterfall-container {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 10px;
    padding: 10px;
  }
  
  .photo-gallery-bg {
    opacity: 0.1;
  }
}

@media (min-width: 1200px) {
  .waterfall-container {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 18px;
    padding: 25px;
  }
}
</style>