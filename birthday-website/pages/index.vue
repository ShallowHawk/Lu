<template>
  <div class="home-page">
    <!-- Loading 层 -->
    <LoadingScreen 
      v-if="isLoading" 
      @loading-complete="handleLoadingComplete"
    />
    
    <!-- 主内容 -->
    <div v-else class="main-content">
      <!-- 恋爱时光机 -->
      <section class="section love-timer">
        <LoveTimer />
      </section>
      
      <!-- 状态展示卡片 -->
      <section class="section status-display">
        <StatusCard />
      </section>
      
      <!-- 生日倒计时 -->
      <section class="section birthday-countdown">
        <BirthdayCountdown />
      </section>
      
      <!-- 动态时间线 -->
      <section class="section timeline">
        <DynamicTimeline />
      </section>
      
      <!-- 互动区域 -->
      <section class="section interactive">
        <InteractiveZone />
      </section>
    </div>
    
    <!-- 生日庆典模式覆盖层 -->
    <BirthdayModal v-if="isBirthdayToday" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// 响应式状态
const isLoading = ref(true)
const currentDate = ref(new Date())

// 计算属性
const isBirthdayToday = computed(() => {
  const today = currentDate.value
  const month = today.getMonth() + 1
  const date = today.getDate()
  
  // 检查是否是7月15日（测试）、7月16日（木头生日）或7月27日（乾雨生日）
  return (month === 7 && date === 15) || (month === 7 && date === 16) || (month === 7 && date === 27)
})

// 生命周期
onMounted(() => {
  // 更新当前时间
  updateCurrentTime()
  
  // 检查是否需要显示生日特效
  if (isBirthdayToday.value) {
    console.log('🎂 今天是木头的破壳日！')
  }
})

// 方法
function handleLoadingComplete() {
  isLoading.value = false
}

function updateCurrentTime() {
  currentDate.value = new Date()
  // 每分钟更新一次时间
  setTimeout(updateCurrentTime, 60000)
}
</script>

<style scoped lang="scss">
.home-page {
  position: relative;
  min-height: 100vh;
}

.main-content {
  position: relative;
  z-index: 2;
  padding: 20px 0;
}

.section {
  margin-bottom: 40px;
  
  &:last-child {
    margin-bottom: 0;
  }
  
  @media (max-width: 768px) {
    margin-bottom: 24px;
  }
}

// 响应式布局
@media (max-width: 1024px) {
  .main-content {
    padding: 16px 0;
  }
}
</style>