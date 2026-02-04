<template>
  <div class="love-timer-container">
    <div class="glass-card timer-card">
      <!-- 标题区域 -->
      <div class="timer-header">
        <h2 class="timer-title">
          <span class="emoji">💕</span>
          我们在一起已经
          <span class="emoji">💕</span>
        </h2>
      </div>
      
      <!-- 主要数字显示区域 -->
      <div class="timer-display">
        <!-- 天数显示 -->
        <div class="time-unit days">
          <div class="liquid-number" ref="daysRef">
            <span class="number">{{ timeDifference.days }}</span>
          </div>
          <div class="unit-label">天</div>
        </div>
        
        <!-- 分隔符 -->
        <div class="separator">🌟</div>
        
        <!-- 小时显示 -->
        <div class="time-unit hours">
          <div class="liquid-number" ref="hoursRef">
            <span class="number">{{ timeDifference.hours }}</span>
          </div>
          <div class="unit-label">小时</div>
        </div>
        
        <!-- 分隔符 -->
        <div class="separator">🌟</div>
        
        <!-- 分钟显示 -->
        <div class="time-unit minutes">
          <div class="liquid-number" ref="minutesRef">
            <span class="number">{{ timeDifference.minutes }}</span>
          </div>
          <div class="unit-label">分钟</div>
        </div>
      </div>
      
      <!-- 里程碑展示 -->
      <div class="milestones">
        <div class="milestone-item" v-for="milestone in milestones" :key="milestone.id">
          <span class="milestone-emoji">{{ milestone.emoji }}</span>
          <span class="milestone-text">{{ milestone.text }}</span>
        </div>
      </div>
      
      <!-- 时间胶囊 -->
      <div class="time-capsule" @click="showTimeCapsule = !showTimeCapsule">
        <div class="capsule-trigger">
          <span class="capsule-emoji">📮</span>
          <span class="capsule-text">此刻的我们</span>
        </div>
        
        <transition name="capsule">
          <div v-if="showTimeCapsule" class="capsule-content">
            <div class="capsule-item">
              <span class="capsule-label">天气：</span>
              <span class="capsule-value">{{ currentWeather }}</span>
            </div>
            <div class="capsule-item">
              <span class="capsule-label">心情：</span>
              <span class="capsule-value">{{ currentMood }}</span>
            </div>
            <div class="capsule-item">
              <span class="capsule-label">正在听：</span>
              <span class="capsule-value">{{ currentMusic }}</span>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { gsap } from 'gsap'

// 响应式状态
const currentTime = ref(new Date())
const showTimeCapsule = ref(false)
const animationInterval = ref(null)

// 引用
const daysRef = ref(null)
const hoursRef = ref(null)
const minutesRef = ref(null)

// 恋爱开始时间
const loveStartDate = new Date('2022-11-02T00:00:00')

// 计算属性
const timeDifference = computed(() => {
  const now = currentTime.value
  const diff = now.getTime() - loveStartDate.getTime()
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  
  return { days, hours, minutes }
})

// 里程碑计算
const milestones = computed(() => {
  const days = timeDifference.value.days
  const result = []
  
  // 检查特殊天数里程碑
  if (days >= 100 && days < 200) {
    result.push({ id: 1, emoji: '🎉', text: '已经100天啦！' })
  } else if (days >= 365 && days < 730) {
    result.push({ id: 2, emoji: '🎊', text: '已经一年啦！' })
  } else if (days >= 730) {
    result.push({ id: 3, emoji: '🎈', text: `已经${Math.floor(days/365)}年啦！` })
  }
  
  // 即将到来的里程碑
  const nextMilestone = getNextMilestone(days)
  if (nextMilestone) {
    result.push(nextMilestone)
  }
  
  return result
})

// 当前状态（模拟数据）
const currentWeather = ref('晴朗 ☀️')
const currentMood = ref('甜甜的 🥰')
const currentMusic = ref('我们的歌 🎵')

// 生命周期
onMounted(() => {
  updateTime()
  startAnimation()
  initLiquidNumbers()
})

onUnmounted(() => {
  if (animationInterval.value) {
    clearInterval(animationInterval.value)
  }
})

// 方法
function updateTime() {
  currentTime.value = new Date()
  
  // 每分钟更新一次
  setTimeout(updateTime, 60000)
}

function startAnimation() {
  // 数字跳动动画
  animationInterval.value = setInterval(() => {
    animateNumbers()
  }, 2000)
}

function animateNumbers() {
  const elements = [daysRef.value, hoursRef.value, minutesRef.value]
  
  elements.forEach((el, index) => {
    if (el) {
      gsap.to(el, {
        scale: 1.1,
        duration: 0.2,
        yoyo: true,
        repeat: 1,
        ease: "power2.inOut",
        delay: index * 0.1
      })
    }
  })
}

function initLiquidNumbers() {
  // 初始化液态数字效果
  const liquidElements = document.querySelectorAll('.liquid-number')
  
  liquidElements.forEach(el => {
    // 添加液态背景
    const liquidBg = document.createElement('div')
    liquidBg.className = 'liquid-bg'
    el.appendChild(liquidBg)
    
    // 液态动画
    gsap.to(liquidBg, {
      scaleY: 1.2,
      duration: 2,
      ease: "sine.inOut",
      repeat: -1,
      yoyo: true
    })
  })
}

function getNextMilestone(currentDays) {
  const milestones = [100, 200, 365, 500, 730, 1000, 1095]
  
  for (const milestone of milestones) {
    if (currentDays < milestone) {
      const daysLeft = milestone - currentDays
      return {
        id: `next-${milestone}`,
        emoji: '🎯',
        text: `距离${milestone}天还有${daysLeft}天`
      }
    }
  }
  
  // 如果超过所有预设里程碑，计算下一个百天
  const nextHundred = Math.ceil(currentDays / 100) * 100
  const daysLeft = nextHundred - currentDays
  return {
    id: `next-${nextHundred}`,
    emoji: '🎯',
    text: `距离${nextHundred}天还有${daysLeft}天`
  }
}

// 鼠标悬停时间凝固效果
function handleMouseEnter() {
  gsap.to('.timer-display', {
    filter: 'hue-rotate(180deg)',
    duration: 0.5,
    ease: "power2.out"
  })
}

function handleMouseLeave() {
  gsap.to('.timer-display', {
    filter: 'hue-rotate(0deg)',
    duration: 0.5,
    ease: "power2.out"
  })
}
</script>

<style scoped lang="scss">
.love-timer-container {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.timer-card {
  padding: 40px;
  text-align: center;
  max-width: 800px;
  width: 100%;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  
  &:hover {
    .timer-display {
      transform: scale(1.02);
    }
  }
}

.timer-header {
  margin-bottom: 40px;
  
  .timer-title {
    font-family: var(--font-heading);
    font-size: clamp(1.5rem, 4vw, 2rem);
    color: white;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
    .emoji {
      margin: 0 8px;
      animation: pulse 2s ease-in-out infinite;
    }
  }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.timer-display {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
  transition: all var(--duration-normal) var(--ease-in-out);
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 16px;
  }
}

.time-unit {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.liquid-number {
  position: relative;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
  
  .number {
    font-family: var(--font-display);
    font-size: 2.5rem;
    font-weight: bold;
    color: white;
    z-index: 2;
    position: relative;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
  
  .liquid-bg {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 30%;
    background: linear-gradient(180deg, 
      rgba(255, 182, 193, 0.8) 0%, 
      rgba(255, 107, 107, 0.6) 100%);
    z-index: 1;
    border-radius: 0 0 20px 20px;
  }
  
  @media (max-width: 768px) {
    width: 100px;
    height: 100px;
    
    .number {
      font-size: 2rem;
    }
  }
}

.unit-label {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.separator {
  font-size: 1.5rem;
  animation: twinkle 1.5s ease-in-out infinite;
  
  @media (max-width: 768px) {
    display: none;
  }
}

@keyframes twinkle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

.milestones {
  margin-bottom: 30px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
}

.milestone-item {
  background: rgba(255, 255, 255, 0.1);
  padding: 12px 20px;
  border-radius: 25px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 0.9rem;
  
  .milestone-emoji {
    margin-right: 8px;
  }
}

.time-capsule {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 30px;
  cursor: pointer;
}

.capsule-trigger {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.8);
  transition: color var(--duration-fast) var(--ease-in-out);
  
  &:hover {
    color: white;
  }
  
  .capsule-emoji {
    font-size: 1.2rem;
  }
}

.capsule-content {
  margin-top: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.capsule-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  color: white;
  font-size: 0.9rem;
  
  .capsule-label {
    opacity: 0.8;
  }
  
  .capsule-value {
    font-weight: 500;
  }
}

// 过渡动画
.capsule-enter-active,
.capsule-leave-active {
  transition: all var(--duration-normal) var(--ease-in-out);
}

.capsule-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.capsule-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>