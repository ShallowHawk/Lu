<template>
  <div class="love-timer-container">
    <div class="book-page">
      <!-- 友人帐风格标题 -->
      <div class="book-header">
        <h2 class="book-title text-handwriting">
          <span class="ink-mark">●</span> 结缘帐 <span class="ink-mark">●</span>
        </h2>
        <div class="date-stamp">{{ formatDate(currentTime) }}</div>
      </div>
      
      <!-- 主要数字显示区域 -->
      <div class="timer-display">
        <!-- 天数显示 -->
        <div class="time-column">
          <div class="ink-circle">
            <span class="number text-heading">{{ timeDifference.days }}</span>
          </div>
          <div class="unit-label text-handwriting">天</div>
        </div>
        
        <div class="vertical-divider"></div>
        
        <!-- 小时显示 -->
        <div class="time-column">
          <div class="ink-circle small">
            <span class="number text-heading">{{ timeDifference.hours }}</span>
          </div>
          <div class="unit-label text-handwriting">时</div>
        </div>
        
        <!-- 分钟显示 -->
        <div class="time-column">
          <div class="ink-circle small">
            <span class="number text-heading">{{ timeDifference.minutes }}</span>
          </div>
          <div class="unit-label text-handwriting">分</div>
        </div>
      </div>
      
      <!-- 底部寄语 -->
      <div class="book-footer text-handwriting">
        <p>与你相遇，是这本友人帐最温柔的名字。</p>
      </div>

      <!-- 时间胶囊按钮 -->
      <div class="stamp-seal" @click="showTimeCapsule = !showTimeCapsule" :class="{ active: showTimeCapsule }">
        <div class="seal-inner">缘</div>
      </div>
      
      <!-- 胶囊内容 -->
      <transition name="fade">
        <div v-if="showTimeCapsule" class="capsule-content text-handwriting">
          <p>今日心情：{{ currentMood }}</p>
          <p>正在播放：{{ currentMusic }}</p>
        </div>
      </transition>
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

// 当前状态（模拟数据）
const currentMood = ref('想见你 🌸')
const currentMusic = ref('夏夕空 🎵')

// 生命周期
onMounted(() => {
  updateTime()
  
  // 入场动画
  gsap.from('.book-page', {
    y: 50,
    opacity: 0,
    duration: 1.5,
    ease: "power3.out"
  })
})

// 方法
function updateTime() {
  currentTime.value = new Date()
  setTimeout(updateTime, 60000)
}

function formatDate(date) {
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}
</script>

<style scoped lang="scss">
.love-timer-container {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.book-page {
  background-color: #FDFBF7;
  width: 100%;
  max-width: 600px;
  padding: 40px;
  box-shadow: 
    0 1px 4px rgba(0,0,0,0.05),
    0 5px 25px rgba(0,0,0,0.1);
  position: relative;
  // 纸张纹理
  background-image: linear-gradient(#E8E4D9 1px, transparent 1px);
  background-size: 100% 30px;
  border-left: 4px double #C4B6A6; // 模拟装订线
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, transparent 50%, rgba(0,0,0,0.05) 50%);
    pointer-events: none;
  }
}

.book-header {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
  
  .book-title {
    font-size: 2.5rem;
    color: var(--text-ink);
    margin-bottom: 10px;
    
    .ink-mark {
      color: var(--primary-pink);
      font-size: 1.5rem;
      vertical-align: middle;
    }
  }
  
  .date-stamp {
    font-family: var(--font-body);
    color: var(--text-light);
    font-size: 0.9rem;
    letter-spacing: 2px;
    writing-mode: horizontal-tb; // 保持横排
  }
}

.timer-display {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 40px;
  gap: 20px;
}

.time-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .ink-circle {
    width: 100px;
    height: 100px;
    border: 3px solid var(--text-ink);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
    position: relative;
    
    // 模拟墨迹不规则边缘
    box-shadow: 
      inset 0 0 0 2px rgba(74, 59, 50, 0.1),
      2px 2px 0 rgba(74, 59, 50, 0.1);
      
    &.small {
      width: 70px;
      height: 70px;
      border-width: 2px;
      
      .number { font-size: 1.8rem; }
    }
    
    .number {
      font-size: 2.5rem;
      color: var(--text-ink);
    }
  }
  
  .unit-label {
    font-size: 1.2rem;
    color: var(--text-light);
  }
}

.vertical-divider {
  width: 1px;
  height: 60px;
  background-color: var(--text-light);
  opacity: 0.3;
}

.book-footer {
  text-align: center;
  font-size: 1.2rem;
  color: var(--text-ink);
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px dashed var(--text-light);
}

.stamp-seal {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  border: 3px solid var(--accent-red);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent-red);
  font-family: var(--font-heading);
  font-size: 2rem;
  transform: rotate(-15deg);
  opacity: 0.8;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: rotate(-15deg) scale(1.1);
    opacity: 1;
  }
  
  &.active {
    background: var(--accent-red);
    color: white;
  }
}

.capsule-content {
  margin-top: 20px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  text-align: center;
  font-size: 1.1rem;
  color: var(--text-ink);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// 移动端适配
@media (max-width: 480px) {
  .book-page {
    padding: 20px;
  }
  
  .book-title {
    font-size: 1.8rem !important;
  }
  
  .timer-display {
    gap: 10px;
  }
  
  .ink-circle {
    width: 80px !important;
    height: 80px !important;
    
    &.small {
      width: 50px !important;
      height: 50px !important;
      
      .number { font-size: 1.2rem !important; }
    }
    
    .number { font-size: 1.8rem !important; }
  }
}
</style>
