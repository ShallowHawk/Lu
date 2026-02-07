<template>
  <div class="home-page">
    <!-- Loading 层 -->
    <LoadingScreen 
      v-if="isLoading" 
      @loading-complete="handleLoadingComplete"
    />
    
    <!-- 主内容 -->
    <div v-else class="main-content">
      <!-- 头部留白，给紫藤花 -->
      <div class="header-spacer"></div>
      
      <!-- Tab 内容区域 -->
      <Transition name="fade-slide" mode="out-in">
        <!-- 首页 Tab -->
        <div v-if="currentTab === 'home'" key="home" class="tab-content">
          <!-- 恋爱时光机 -->
          <section class="section love-timer scroll-reveal">
            <LoveTimer />
          </section>
          
          <!-- 状态展示卡片 -->
          <section class="section status-display scroll-reveal">
            <div class="section-title-wrapper">
              <h3 class="section-title text-heading">
                <span class="decoration-line"></span>
                灵力与运势
                <span class="decoration-line"></span>
              </h3>
            </div>
            <StatusCard />
          </section>
          
          <!-- 生日倒计时 -->
          <section class="section birthday-countdown scroll-reveal">
            <div class="section-title-wrapper">
              <h3 class="section-title text-heading">
                <span class="decoration-line"></span>
                庆典倒计时
                <span class="decoration-line"></span>
              </h3>
            </div>
            <BirthdayCountdown />
          </section>
        </div>
        
        <!-- 时光 Tab -->
        <div v-else-if="currentTab === 'timeline'" key="timeline" class="tab-content">
          <section class="section timeline">
            <DynamicTimeline />
          </section>
        </div>
        
        <!-- 留言 Tab -->
        <div v-else-if="currentTab === 'message'" key="message" class="tab-content">
          <section class="section interactive">
            <InteractiveZone />
          </section>
        </div>
      </Transition>
      
      <!-- 底部留白 -->
      <div class="footer-spacer"></div>
    </div>
    
    <!-- 移动端底部导航 -->
    <div class="mobile-nav" v-if="!isLoading">
      <div 
        class="nav-item" 
        :class="{ active: currentTab === 'home' }"
        @click="currentTab = 'home'"
      >
        <span class="nav-icon">🏠</span>
        <span class="nav-label" v-if="currentTab === 'home'">首页</span>
      </div>
      <div 
        class="nav-item" 
        :class="{ active: currentTab === 'timeline' }"
        @click="currentTab = 'timeline'"
      >
        <span class="nav-icon">📸</span>
        <span class="nav-label" v-if="currentTab === 'timeline'">时光</span>
      </div>
      <div 
        class="nav-item" 
        :class="{ active: currentTab === 'message' }"
        @click="currentTab = 'message'"
      >
        <span class="nav-icon">💌</span>
        <span class="nav-label" v-if="currentTab === 'message'">留言</span>
      </div>
    </div>
    
    <!-- 生日庆典模式覆盖层 -->
    <BirthdayModal v-if="isBirthdayToday" />

    <!-- 公告卷轴 -->
    <ScrollLetter v-model="showScrollLetter" @close="handleScrollClose" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import ScrollLetter from '~/components/ScrollLetter.vue'

// 使用中间件进行路由保护
definePageMeta({
  middleware: 'auth'
})

// 注册插件
gsap.registerPlugin(ScrollTrigger)

// 响应式状态
const isLoading = ref(true)
const currentDate = ref(new Date())
const currentTab = ref('home')
const showScrollLetter = ref(false)

// 计算属性
const isBirthdayToday = computed(() => {
  const today = currentDate.value
  const month = today.getMonth() + 1
  const date = today.getDate()
  return (month === 7 && date === 15) || (month === 7 && date === 16) || (month === 7 && date === 27)
})

// 生命周期
onMounted(() => {
  updateCurrentTime()
})

// 监听 Tab 切换，重新初始化动画
watch(currentTab, () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
  nextTick(() => {
    initScrollAnimations()
  })
})

// 方法
function handleLoadingComplete() {
  isLoading.value = false
  // 等待DOM更新后初始化滚动动画
  nextTick(() => {
    initScrollAnimations()
    checkScrollLetter()
  })
}

function checkScrollLetter() {
  // 优先从 Cookie 获取角色，如果 Cookie 没有再看 localStorage
  const roleCookie = useCookie('user_role')
  const role = roleCookie.value || localStorage.getItem('user_role')
  
  if (role !== 'mutou') return
  
  // 检查是否已经看过
  const hasSeen = localStorage.getItem('has_seen_notice_2026_feb_v2')
  
  // 临时逻辑：如果需要调试，可以把这里改为 !hasSeen || true
  if (!hasSeen) {
    // 延迟一点显示，让用户先看到主界面
    setTimeout(() => {
        showScrollLetter.value = true
    }, 1000)
  }
}

function handleScrollClose(markAsRead) {
  if (markAsRead) {
    // 只有点击“朕已阅”才标记已读
    // 设置过期时间？目前永久标记，除非清除缓存
    localStorage.setItem('has_seen_notice_2026_feb_v2', 'true')
  }
}

function initScrollAnimations() {
  const sections = document.querySelectorAll('.scroll-reveal')
  
  // 清除旧的 ScrollTrigger
  ScrollTrigger.getAll().forEach(st => st.kill())
  
  sections.forEach((section, index) => {
    gsap.fromTo(section, 
      { 
        opacity: 0, 
        y: 30,
        filter: 'blur(5px)'
      },
      {
        opacity: 1,
        y: 0,
        filter: 'blur(0px)',
        duration: 0.8,
        ease: "power2.out",
        scrollTrigger: {
          trigger: section,
          start: "top 85%", 
          toggleActions: "play none none reverse"
        }
      }
    )
  })
}

function updateCurrentTime() {
  currentDate.value = new Date()
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
  padding: 0 16px;
  max-width: 800px;
  margin: 0 auto;
}

.header-spacer {
  height: 80px;
}

.footer-spacer {
  height: 120px; // 增加底部空间
}

.section {
  margin-bottom: 40px;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.section-title-wrapper {
  text-align: center;
  margin-bottom: 30px;
  
  .section-title {
    font-size: 1.5rem;
    color: var(--text-ink);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    
    .decoration-line {
      width: 40px;
      height: 2px;
      background: var(--primary-pink);
      position: relative;
      
      &::after {
        content: '';
        position: absolute;
        top: -4px;
        right: 0;
        width: 10px;
        height: 10px;
        background: var(--primary-pink);
        border-radius: 50%;
        opacity: 0.5;
      }
      
      &:first-child::after {
        left: 0;
        right: auto;
      }
    }
  }
}

.mobile-nav {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(15px);
  padding: 8px 10px;
  border-radius: 40px;
  display: flex;
  gap: 15px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
  border: 1px solid rgba(255, 255, 255, 0.6);
  z-index: 100;
  
  .nav-item {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 8px 15px;
    border-radius: 30px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    opacity: 0.6;
    
    .nav-icon {
      font-size: 1.4rem;
    }
    
    .nav-label {
      font-size: 0.9rem;
      font-weight: bold;
      color: var(--text-ink);
      white-space: nowrap;
    }
    
    &.active {
      background: #FFE4E1; // 浅粉色背景
      opacity: 1;
      transform: scale(1.05);
      
      .nav-icon {
        transform: scale(1.1);
      }
    }
    
    &:hover:not(.active) {
      background: rgba(0,0,0,0.05);
      opacity: 0.8;
    }
  }
}

// Tab 切换动画
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
