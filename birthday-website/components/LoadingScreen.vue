<template>
  <div class="loading-screen" :class="{ 'fade-out': isComplete }">
    <!-- 和纸纹理背景 -->
    <div class="paper-texture"></div>
    
    <!-- 加载内容 -->
    <div class="loading-content">
      <!-- 动画区域 -->
      <div class="anime-scene">
        <!-- 蝴蝶 -->
        <div class="butterfly-container">
          <div class="butterfly">🦋</div>
        </div>
        
        <!-- 猫咪老师风格圆猫 -->
        <div class="cat-container">
          <div class="cat-body">
            <div class="cat-ears">
              <div class="ear left"></div>
              <div class="ear right"></div>
            </div>
            <div class="cat-face">
              <div class="eyes">
                <div class="eye left"></div>
                <div class="eye right"></div>
              </div>
              <div class="nose"></div>
              <div class="mouth"></div>
              <div class="whiskers">
                <div class="whisker left"></div>
                <div class="whisker right"></div>
              </div>
              <div class="cheeks">
                <div class="cheek left"></div>
                <div class="cheek right"></div>
              </div>
            </div>
          </div>
          <div class="cat-tail"></div>
        </div>
      </div>
      
      <!-- 文字与进度 (增加间距) -->
      <div class="text-container">
        <h2 class="loading-text text-heading">{{ currentText }}</h2>
        
        <!-- 肉球进度条 -->
        <div class="paw-progress">
          <div 
            v-for="n in 5" 
            :key="n"
            class="paw"
            :class="{ active: (progress / 20) >= n }"
          >
            🐾
          </div>
        </div>
        
        <p class="percent text-handwriting">{{ Math.round(progress) }}%</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { gsap } from 'gsap'

const emit = defineEmits(['loading-complete'])

// 状态
const isComplete = ref(false)
const progress = ref(0)
const currentTextIndex = ref(0)

// 文案
const texts = [
  '正在召唤猫咪老师...',
  '准备好团子和清酒...',
  '打开友人帐的封印...',
  '收集散落的缘分...',
  '欢迎回来，木头！'
]

const currentText = computed(() => texts[currentTextIndex.value])

onMounted(() => {
  startLoading()
  animateScene()
})

watch(progress, (val) => {
  // 根据进度切换文案
  const index = Math.min(Math.floor((val / 100) * texts.length), texts.length - 1)
  if (index !== currentTextIndex.value) {
    currentTextIndex.value = index
  }
  
  if (val >= 100) {
    completeLoading()
  }
})

function startLoading() {
  gsap.to(progress, {
    value: 100,
    duration: 5,
    ease: "power2.inOut"
  })
}

function animateScene() {
  // 蝴蝶飞舞
  gsap.to('.butterfly-container', {
    x: 100,
    y: -50,
    rotation: 360,
    duration: 3,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  })
  
  // 猫咪跳跃
  gsap.to('.cat-container', {
    y: -20,
    duration: 0.5,
    repeat: -1,
    yoyo: true,
    ease: "power1.out"
  })
  
  // 尾巴摇摆
  gsap.to('.cat-tail', {
    rotation: 20,
    duration: 1,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  })
}

function completeLoading() {
  isComplete.value = true
  setTimeout(() => {
    emit('loading-complete')
  }, 1000)
}
</script>

<style scoped lang="scss">
.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--bg-paper);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 1s ease;
  
  &.fade-out {
    opacity: 0;
    pointer-events: none;
  }
}

.paper-texture {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.5;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%239C92AC' fill-opacity='0.1' fill-rule='evenodd'/%3E%3C/svg%3E");
}

.loading-content {
  text-align: center;
  color: white;
  z-index: 10;
  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
}

.anime-scene {
  position: relative;
  height: 200px;
  width: 100%;
  max-width: 300px;
  margin: 0 auto 60px; // 增加底部间距
  display: flex;
  justify-content: center;
  align-items: center;
}

.butterfly-container {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 2rem;
  z-index: 2;
}

// 简单的 CSS 猫咪绘制
.cat-container {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 100px;
}

.cat-body {
  width: 100px;
  height: 80px;
  background: white;
  border-radius: 50% 50% 40% 40%;
  border: 3px solid var(--text-ink);
  position: relative;
  margin: 0 auto;
  box-shadow: inset -10px -5px 0 #eee;
}

.cat-ears {
  .ear {
    position: absolute;
    top: -15px;
    width: 0;
    height: 0;
    border-left: 15px solid transparent;
    border-right: 15px solid transparent;
    border-bottom: 25px solid white;
    
    &::after {
      content: '';
      position: absolute;
      top: 5px;
      left: -8px;
      border-left: 8px solid transparent;
      border-right: 8px solid transparent;
      border-bottom: 15px solid var(--primary-pink);
      opacity: 0.6;
    }
    
    &.left { left: 5px; transform: rotate(-15deg); }
    &.right { right: 5px; transform: rotate(15deg); }
  }
}

.cat-face {
  position: relative;
  top: 25px;
  
  .eyes {
    display: flex;
    justify-content: space-between;
    padding: 0 25px;
    
    .eye {
      width: 8px;
      height: 8px;
      background: var(--text-ink);
      border-radius: 50%;
    }
  }
  
  .nose {
    width: 6px;
    height: 4px;
    background: var(--primary-pink);
    border-radius: 50%;
    margin: 5px auto 0;
  }
  
  .mouth {
    width: 12px;
    height: 6px;
    border-bottom: 2px solid var(--text-ink);
    border-radius: 0 0 10px 10px;
    margin: 0 auto;
  }
  
  .cheeks {
    .cheek {
      position: absolute;
      top: 10px;
      width: 12px;
      height: 6px;
      background: var(--primary-pink);
      border-radius: 50%;
      opacity: 0.4;
      
      &.left { left: 15px; }
      &.right { right: 15px; }
    }
  }
}

.text-container {
  text-align: center;
}

.loading-text {
  color: var(--text-ink);
  margin-bottom: 20px;
  min-height: 1.5em;
}

.paw-progress {
  display: flex;
  justify-content: center;
  gap: 15px;
  font-size: 1.5rem;
  margin-bottom: 10px;
  
  .paw {
    opacity: 0.2;
    transition: all 0.3s ease;
    transform: scale(0.8);
    
    &.active {
      opacity: 1;
      transform: scale(1.2);
      color: var(--primary-pink);
    }
  }
}

.percent {
  color: var(--text-light);
  font-size: 1.2rem;
}
</style>
