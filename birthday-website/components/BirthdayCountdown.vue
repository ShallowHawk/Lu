<template>
  <div class="countdown-container">
    <div class="wafu-card countdown-card">
      <!-- 装饰用纸带 -->
      <div class="paper-tape"></div>
      
      <!-- 木头生日倒计时 -->
      <div class="countdown-section">
        <h3 class="countdown-title text-heading">
          <img :src="`/images/mutou_avatar.jpg?t=${timestamp}`" class="birthday-avatar" alt="木头" />
          木头的破壳日
        </h3>
        
        <div v-if="mutouCountdown.showCountdown" class="countdown-display">
          <div class="time-block">
            <div class="countdown-number text-heading">{{ mutouCountdown.days }}</div>
            <div class="countdown-label text-handwriting">天</div>
          </div>
          <div class="time-block">
            <div class="countdown-number text-heading">{{ mutouCountdown.hours }}</div>
            <div class="countdown-label text-handwriting">时</div>
          </div>
          <div class="time-block">
            <div class="countdown-number text-heading">{{ mutouCountdown.minutes }}</div>
            <div class="countdown-label text-handwriting">分</div>
          </div>
        </div>
        
        <div v-else class="age-display">
          <div class="age-text text-handwriting">来到这个世界</div>
          <div class="age-number-container">
             <span class="age-number text-heading">{{ mutouCountdown.daysSinceBirth }}</span>
             <span class="age-unit text-handwriting">天</span>
          </div>
        </div>
        
        <div class="countdown-message text-handwriting" v-if="mutouCountdown.isBirthday">
          🎉 今天是木头的破壳日！🎉
        </div>
        <div class="countdown-message text-handwriting" v-else-if="mutouCountdown.days <= 3 && mutouCountdown.showCountdown">
          💝 破壳日快到啦，好期待！
        </div>
      </div>
      
      <div class="divider-line"></div>
      
      <!-- 乾雨生日倒计时 -->
      <div class="countdown-section">
        <h3 class="countdown-title text-heading">
          <img :src="`/images/qianyu_avatar.jpg?t=${timestamp}`" class="birthday-avatar" alt="乾雨" />
          乾雨的破壳日
        </h3>
        
        <div v-if="qianyuCountdown.showCountdown" class="countdown-display">
          <div class="time-block">
            <div class="countdown-number text-heading">{{ qianyuCountdown.days }}</div>
            <div class="countdown-label text-handwriting">天</div>
          </div>
          <div class="time-block">
            <div class="countdown-number text-heading">{{ qianyuCountdown.hours }}</div>
            <div class="countdown-label text-handwriting">时</div>
          </div>
          <div class="time-block">
            <div class="countdown-number text-heading">{{ qianyuCountdown.minutes }}</div>
            <div class="countdown-label text-handwriting">分</div>
          </div>
        </div>
        
        <div v-else class="age-display">
          <div class="age-text text-handwriting">来到这个世界</div>
          <div class="age-number-container">
             <span class="age-number text-heading">{{ qianyuCountdown.daysSinceBirth }}</span>
             <span class="age-unit text-handwriting">天</span>
          </div>
        </div>
        
        <div class="countdown-message text-handwriting" v-if="qianyuCountdown.isBirthday">
          🎊 今天是乾雨的破壳日！🎊
        </div>
        <div class="countdown-message text-handwriting" v-else-if="qianyuCountdown.days <= 7 && qianyuCountdown.showCountdown">
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
const timestamp = ref(Date.now())

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
  padding: 40px 30px;
  max-width: 600px;
  width: 100%;
  text-align: center;
  position: relative;
  background-color: #fff;
  background-image: linear-gradient(0deg, transparent 24%, rgba(220, 220, 220, .3) 25%, rgba(220, 220, 220, .3) 26%, transparent 27%, transparent 74%, rgba(220, 220, 220, .3) 75%, rgba(220, 220, 220, .3) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(220, 220, 220, .3) 25%, rgba(220, 220, 220, .3) 26%, transparent 27%, transparent 74%, rgba(220, 220, 220, .3) 75%, rgba(220, 220, 220, .3) 76%, transparent 77%, transparent);
  background-size: 50px 50px;
}

.paper-tape {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 30px;
  background: rgba(240, 145, 153, 0.6); // 樱花粉胶带
  transform: translateX(-50%) rotate(-2deg);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  
  &::before {
    content: '';
    position: absolute;
    left: -5px;
    top: 0;
    width: 0;
    height: 0;
    border-top: 15px solid transparent;
    border-bottom: 15px solid transparent;
    border-right: 5px solid rgba(240, 145, 153, 0.6);
  }
  
  &::after {
    content: '';
    position: absolute;
    right: -5px;
    top: 0;
    width: 0;
    height: 0;
    border-top: 15px solid transparent;
    border-bottom: 15px solid transparent;
    border-left: 5px solid rgba(240, 145, 153, 0.6);
  }
}

.countdown-section {
  margin-bottom: 30px;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.countdown-title {
  font-size: 1.4rem;
  color: var(--text-ink);
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  
  .birthday-emoji {
    animation: bounce 2s ease-in-out infinite;
  }
  
  .birthday-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid var(--primary-pink);
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
  gap: 20px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.time-block {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.countdown-number {
  font-size: 2.2rem;
  color: var(--primary-red, #CB4042);
  background: transparent;
  padding: 5px 15px;
  border-bottom: 2px solid var(--text-ink);
  min-width: 60px;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: scale(1.1);
  }
}

.countdown-label {
  font-size: 1rem;
  color: var(--text-light);
  margin-top: 5px;
}

.age-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  
  .age-text {
    font-size: 1.1rem;
    color: var(--text-ink);
  }
  
  .age-number-container {
    display: flex;
    align-items: baseline;
    gap: 5px;
    
    .age-number {
      font-size: 3rem;
      color: var(--text-ink);
      line-height: 1;
    }
    
    .age-unit {
      font-size: 1.2rem;
      color: var(--text-light);
    }
  }
}

.countdown-message {
  font-size: 1.1rem;
  color: var(--accent-red);
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 15px;
  border: 1px dashed var(--accent-red);
  display: inline-block;
  margin-top: 10px;
}

.divider-line {
  height: 1px;
  background-image: linear-gradient(to right, transparent, var(--text-light), transparent);
  margin: 30px 0;
  opacity: 0.3;
}

// 响应式设计
@media (max-width: 768px) {
  .countdown-display {
    gap: 15px;
  }
  
  .countdown-number {
    font-size: 1.8rem;
    min-width: 50px;
  }
  
  .age-number-container .age-number {
    font-size: 2.5rem;
  }
}
</style>
