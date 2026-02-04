<template>
  <div class="countdown-container">
    <div class="glass-card countdown-card">
      <!-- 木头生日倒计时 -->
      <div class="countdown-section">
        <h3 class="countdown-title">
          <span class="birthday-emoji">🪵</span>
          木头的破壳日
        </h3>
        
        <div v-if="mutouCountdown.showCountdown" class="countdown-display">
          <div class="countdown-number">{{ mutouCountdown.days }}</div>
          <div class="countdown-label">天</div>
          <div class="countdown-number">{{ mutouCountdown.hours }}</div>
          <div class="countdown-label">小时</div>
          <div class="countdown-number">{{ mutouCountdown.minutes }}</div>
          <div class="countdown-label">分钟</div>
        </div>
        
        <div v-else class="age-display">
          <div class="age-text">木头已经来到了这个世界上</div>
          <div class="age-number">{{ mutouCountdown.daysSinceBirth }}</div>
          <div class="age-label">天</div>
        </div>
        
        <div class="countdown-message" v-if="mutouCountdown.isBirthday">
          🎉 今天是木头的破壳日！🎉
        </div>
        <div class="countdown-message" v-else-if="mutouCountdown.days <= 3 && mutouCountdown.showCountdown">
          💝 破壳日快到啦，好期待！
        </div>
      </div>
      
      <!-- 乾雨生日倒计时 -->
      <div class="countdown-section">
        <h3 class="countdown-title">
          <span class="birthday-emoji">🦅</span>
          乾雨的破壳日
        </h3>
        
        <div v-if="qianyuCountdown.showCountdown" class="countdown-display">
          <div class="countdown-number">{{ qianyuCountdown.days }}</div>
          <div class="countdown-label">天</div>
          <div class="countdown-number">{{ qianyuCountdown.hours }}</div>
          <div class="countdown-label">小时</div>
          <div class="countdown-number">{{ qianyuCountdown.minutes }}</div>
          <div class="countdown-label">分钟</div>
        </div>
        
        <div v-else class="age-display">
          <div class="age-text">乾雨已经来到了这个世界上</div>
          <div class="age-number">{{ qianyuCountdown.daysSinceBirth }}</div>
          <div class="age-label">天</div>
        </div>
        
        <div class="countdown-message" v-if="qianyuCountdown.isBirthday">
          🎊 今天是乾雨的破壳日！🎊
        </div>
        <div class="countdown-message" v-else-if="qianyuCountdown.days <= 7 && qianyuCountdown.showCountdown">
          🎁 乾雨的破壳日也快到了呢~
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// 响应式状态
const currentTime = ref(new Date())
const updateInterval = ref(null)

// 生日日期（出生年份）
const mutouBirthDate = new Date('2003-07-16T00:00:00') // 木头2003年7月16日
const qianyuBirthDate = new Date('2002-07-27T00:00:00') // 乾雨2002年7月27日

// 计算倒计时
const mutouCountdown = computed(() => {
  return calculateCountdownOrAge(mutouBirthDate, '木头')
})

const qianyuCountdown = computed(() => {
  return calculateCountdownOrAge(qianyuBirthDate, '乾雨')
})

// 生命周期
onMounted(() => {
  updateTime()
})

onUnmounted(() => {
  if (updateInterval.value) {
    clearInterval(updateInterval.value)
  }
})

// 方法
function updateTime() {
  currentTime.value = new Date()
  
  // 每分钟更新一次
  updateInterval.value = setInterval(() => {
    currentTime.value = new Date()
  }, 60000)
}

function calculateCountdownOrAge(birthDate, name) {
  const now = currentTime.value
  const thisYear = now.getFullYear()
  
  // 计算今年的生日
  const thisYearBirthday = new Date(thisYear, birthDate.getMonth(), birthDate.getDate())
  
  // 检查是否是生日当天
  const isBirthday = now.getMonth() === birthDate.getMonth() && now.getDate() === birthDate.getDate()
  
  // 如果今年生日已过，计算明年的生日
  let nextBirthday = thisYearBirthday
  if (thisYearBirthday < now) {
    nextBirthday = new Date(thisYear + 1, birthDate.getMonth(), birthDate.getDate())
  }
  
  // 计算距离下次生日的天数
  const timeDiff = nextBirthday.getTime() - now.getTime()
  const daysUntilBirthday = Math.ceil(timeDiff / (1000 * 60 * 60 * 24))
  
  // 计算出生以来的天数
  const daysSinceBirth = Math.floor((now.getTime() - birthDate.getTime()) / (1000 * 60 * 60 * 24))
  
  // 如果是生日当天，显示年龄和生日消息
  if (isBirthday) {
    return {
      showCountdown: false,
      isBirthday: true,
      days: 0,
      hours: 0,
      minutes: 0,
      daysSinceBirth: daysSinceBirth
    }
  }
  
  // 判断是否显示倒计时（30天内）
  const showCountdown = daysUntilBirthday <= 30
  
  if (showCountdown) {
    // 显示倒计时
    const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24))
    const hours = Math.floor((timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
    const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60))
    
    return {
      showCountdown: true,
      isBirthday: false,
      days: days,
      hours: hours,
      minutes: minutes,
      daysSinceBirth: daysSinceBirth
    }
  } else {
    // 显示出生天数
    return {
      showCountdown: false,
      isBirthday: false,
      days: 0,
      hours: 0,
      minutes: 0,
      daysSinceBirth: daysSinceBirth
    }
  }
}
</script>

<style scoped lang="scss">
.countdown-container {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.countdown-card {
  padding: 30px;
  max-width: 600px;
  width: 100%;
  text-align: center;
}

.countdown-section {
  margin-bottom: 40px;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.countdown-title {
  font-family: var(--font-heading);
  font-size: 1.3rem;
  color: white;
  margin: 0 0 20px 0;
  
  .birthday-emoji {
    margin-right: 8px;
    animation: bounce 2s ease-in-out infinite;
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.countdown-display {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.countdown-number {
  font-family: var(--font-display);
  font-size: 2.5rem;
  font-weight: bold;
  color: white;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px 20px;
  min-width: 80px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: transform var(--duration-fast) var(--ease-in-out);
  
  &:hover {
    transform: scale(1.1);
  }
  
  @media (max-width: 768px) {
    font-size: 2rem;
    padding: 12px 16px;
    min-width: 60px;
  }
}

.countdown-label {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.age-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  
  .age-text {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.9);
    font-weight: 500;
  }
  
  .age-number {
    font-family: var(--font-display);
    font-size: 3rem;
    font-weight: bold;
    color: white;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 20px 30px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    animation: ageGlow 3s ease-in-out infinite;
    
    @media (max-width: 768px) {
      font-size: 2.5rem;
      padding: 16px 24px;
    }
  }
  
  .age-label {
    font-size: 1.2rem;
    color: rgba(255, 255, 255, 0.8);
    font-weight: 600;
  }
}

@keyframes ageGlow {
  0%, 100% { 
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
  }
  50% { 
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.6);
  }
}

.countdown-message {
  font-size: 1.1rem;
  color: white;
  font-weight: 600;
  padding: 12px 20px;
  background: rgba(255, 107, 107, 0.3);
  border-radius: 20px;
  border: 1px solid rgba(255, 107, 107, 0.5);
  animation: messageGlow 2s ease-in-out infinite;
}

@keyframes messageGlow {
  0%, 100% { box-shadow: 0 0 10px rgba(255, 107, 107, 0.5); }
  50% { box-shadow: 0 0 20px rgba(255, 107, 107, 0.8); }
}

// 响应式设计
@media (max-width: 768px) {
  .countdown-display {
    gap: 12px;
  }
  
  .countdown-title {
    font-size: 1.1rem;
  }
  
  .countdown-message {
    font-size: 1rem;
    padding: 10px 16px;
  }
}
</style>