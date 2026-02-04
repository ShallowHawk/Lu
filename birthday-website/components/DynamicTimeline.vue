<template>
  <div class="timeline-container">
    <div class="glass-card timeline-card">
      <h3 class="timeline-title">
        <span class="timeline-emoji">📖</span>
        我们的动态时光
        <!-- 刷新按钮 -->
        <button 
          @click="refreshTimeline" 
          :disabled="loading"
          class="refresh-btn"
          title="刷新动态"
        >
          <span class="refresh-icon" :class="{ 'spinning': loading }">🔄</span>
        </button>
      </h3>
      
      <div class="timeline-content">
        <!-- 加载状态 -->
        <div v-if="loading && timelineItems.length === 0" class="timeline-loading">
          <div class="loading-spinner"></div>
          <p>正在加载动态历史...</p>
        </div>
        
        <!-- 错误状态 -->
        <div v-else-if="error && timelineItems.length === 0" class="timeline-error">
          <div class="error-icon">⚠️</div>
          <p>{{ error }}</p>
          <button @click="fetchStatusHistory" class="retry-btn">重试</button>
        </div>
        
        <!-- 时间线内容 -->
        <div v-else>
          <div 
            v-for="(item, index) in displayedItems" 
            :key="item.id"
            class="timeline-item"
            :class="{ 'highlight': item.isHighlight }"
          >
            <!-- 时间线连接线 -->
            <div class="timeline-connector" v-if="index !== displayedItems.length - 1" />
            
            <!-- 时间点 -->
            <div class="timeline-dot" :style="{ backgroundColor: item.color }">
              <span class="dot-emoji">{{ item.emoji }}</span>
            </div>
            
            <!-- 内容卡片 -->
            <div class="timeline-content-card">
              <div class="timeline-header">
                <h4 class="timeline-item-title">{{ item.title }}</h4>
                <span class="timeline-time">{{ formatTime(item.timestamp) }}</span>
              </div>
              
              <p class="timeline-description">{{ item.description }}</p>
              
              <!-- 用户信息 -->
              <div class="timeline-user">
                <span class="user-emoji">{{ item.userEmoji }}</span>
                <span class="user-name">{{ item.userName }}</span>
              </div>
              
              <!-- 特殊内容 -->
              <div v-if="item.type === 'milestone'" class="milestone-badge">
                <span class="milestone-text">🎉 里程碑</span>
              </div>
              
              <div v-if="item.type === 'birthday'" class="birthday-badge">
                <span class="birthday-text">🎂 生日快乐</span>
              </div>
              
              <div v-if="item.type === 'achievement'" class="achievement-badge">
                <span class="achievement-text">🏆 新成就</span>
              </div>
            </div>
          </div>
          
          <!-- 展开/折叠按钮 -->
          <div class="load-more" v-if="hasMoreToShow">
            <button @click="toggleShowAll" class="load-more-btn" :disabled="loading">
              <span class="toggle-icon">{{ showAll ? '👆' : '👇' }}</span>
              <span>{{ showAll ? '折叠动态' : `查看更多动态 (+${timelineItems.length - maxDisplayItems})` }}</span>
            </button>
          </div>
          
          <!-- 空状态 -->
          <div v-if="timelineItems.length === 0 && !loading && !error" class="empty-state">
            <div class="empty-icon">📝</div>
            <p>暂无动态记录</p>
            <small>当有状态变化时，这里会显示历史记录</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// 响应式状态
const timelineItems = ref([])
const hasMore = ref(false)
const loading = ref(false)
const error = ref('')
const timeUpdateInterval = ref(null)
const currentPage = ref(0)
const pageSize = ref(10)
const showAll = ref(false) // 新增：控制是否显示全部动态
const maxDisplayItems = ref(5) // 新增：默认显示的最大条数

// 计算属性：控制显示的动态条数
const displayedItems = computed(() => {
  if (showAll.value) {
    return timelineItems.value
  }
  return timelineItems.value.slice(0, maxDisplayItems.value)
})

// 计算属性：是否有更多可展开的内容
const hasMoreToShow = computed(() => {
  return timelineItems.value.length > maxDisplayItems.value
})

// 状态配置（与StatusCard组件保持一致）
const statusConfig = {
  1: { name: '睡觉中', emoji: '😴', color: '#9B59B6' },
  2: { name: '工作中', emoji: '💻', color: '#3498DB' },
  3: { name: '运动中', emoji: '🏃‍♀️', color: '#E74C3C' },
  4: { name: '看B站', emoji: '📱', color: '#FF69B4' },
  5: { name: '玩游戏', emoji: '🎮', color: '#F39C12' },
  6: { name: '听音乐', emoji: '🎵', color: '#1ABC9C' },
  7: { name: '学习中', emoji: '📚', color: '#8E44AD' },
  8: { name: '做饭中', emoji: '👩‍🍳', color: '#E67E22' }
}

// 用户配置
const userConfig = {
  '木头': { emoji: '🪵', displayName: '木头' },
  '乾雨': { emoji: '🦅', displayName: '乾雨' }
}

// 生命周期
onMounted(() => {
  fetchStatusHistory()
  startTimeUpdate()
})

onUnmounted(() => {
  stopTimeUpdate()
})

// 方法
async function fetchStatusHistory() {
  if (loading.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    // 使用API配置文件
    const { api } = useApi()
    // 调用真实的后端历史API
    const response = await fetch(api.baseURL + '/history')
    const data = await response.json()
    
    if (data.history && Array.isArray(data.history)) {
      // 处理历史数据，转换为时间线格式
      const newItems = processHistoryData(data.history)
      
      if (currentPage.value === 0) {
        // 首次加载，替换现有数据
        timelineItems.value = newItems
        // 重置展开状态
        showAll.value = false
      } else {
        // 加载更多，追加数据
        timelineItems.value = [...timelineItems.value, ...newItems]
      }
      
      // 检查是否还有更多数据（简单判断）
      hasMore.value = data.history.length >= pageSize.value
    } else {
      throw new Error('无效的历史数据格式')
    }
  } catch (fetchError) {
    console.error('获取状态历史失败:', fetchError)
    error.value = '连接服务器失败，显示备用数据'
    
    // 使用备用数据
    if (currentPage.value === 0) {
      timelineItems.value = getFallbackTimelineData()
      hasMore.value = false
      showAll.value = false
    }
  }
  
  loading.value = false
}

function processHistoryData(historyData) {
  return historyData.map(item => {
    const statusInfo = statusConfig[item.status_id] || statusConfig[1]
    const userInfo = userConfig[item.user] || { emoji: '👤', displayName: item.user }
    
    // 生成合适的标题和描述
    const title = generateTimelineTitle(item.user, statusInfo.name)
    const description = generateTimelineDescription(item.user, statusInfo.name)
    
    return {
      id: `${item.user}-${item.status_id}-${item.timestamp}`,
      title: title,
      description: description,
      timestamp: new Date(item.timestamp).getTime(),
      emoji: statusInfo.emoji,
      color: statusInfo.color,
      type: determineItemType(item.status_id),
      isHighlight: isHighlightItem(item.status_id),
      userName: userInfo.displayName,
      userEmoji: userInfo.emoji
    }
  })
}

function generateTimelineTitle(user, statusName) {
  const titles = {
    '睡觉中': `${user}进入了梦乡`,
    '工作中': `${user}开始努力工作`,
    '运动中': `${user}开始运动锻炼`,
    '看B站': `${user}在刷B站`,
    '玩游戏': `${user}进入游戏世界`,
    '听音乐': `${user}在享受音乐`,
    '学习中': `${user}开始认真学习`,
    '做饭中': `${user}在准备美食`
  }
  return titles[statusName] || `${user}更新了状态为${statusName}`
}

function generateTimelineDescription(user, statusName) {
  const descriptions = {
    '睡觉中': '正在做美梦，进入甜蜜的睡眠时光zzz...',
    '工作中': '正在专注工作，为美好的明天努力奋斗',
    '运动中': '正在挥洒汗水，保持健康的生活状态💪',
    '看B站': '正在B站上发现有趣的内容，享受休闲时光',
    '玩游戏': '在虚拟世界中寻找快乐和成就感',
    '听音乐': '沉浸在美妙的音乐中，享受艺术的熏陶',
    '学习中': '正在汲取知识的养分，不断提升自己',
    '做饭中': '正在厨房里忙碌，准备美味的食物'
  }
  return descriptions[statusName] || `${user}切换到了${statusName}状态`
}

function determineItemType(statusId) {
  const typeMap = {
    '1': 'rest',      // 睡觉
    '2': 'work',      // 工作
    '3': 'exercise',  // 运动
    '4': 'entertainment', // B站
    '5': 'gaming',    // 游戏
    '6': 'music',     // 音乐
    '7': 'study',     // 学习
    '8': 'cooking'    // 做饭
  }
  return typeMap[statusId] || 'activity'
}

function isHighlightItem(statusId) {
  // 特殊状态设为高亮（运动、学习、做饭）
  return ['3', '7', '8'].includes(statusId)
}

function getFallbackTimelineData() {
  // 备用数据（当API无法访问时使用）
  return [
    {
      id: 'fallback-1',
      title: '连接状态监控服务中...',
      description: '正在尝试连接到状态监控系统，请稍后再试',
      timestamp: Date.now(),
      emoji: '🔄',
      color: '#3498DB',
      type: 'system',
      isHighlight: true,
      userName: '系统',
      userEmoji: '⚙️'
    },
    {
      id: 'fallback-2',
      title: '服务暂时不可用',
      description: '状态历史记录暂时无法获取，请检查网络连接',
      timestamp: Date.now() - 300000,
      emoji: '⚠️',
      color: '#E74C3C',
      type: 'error',
      isHighlight: false,
      userName: '系统',
      userEmoji: '⚙️'
    }
  ]
}

function loadMoreItems() {
  // 暂时简化，因为后端API不支持分页
  // 实际项目中可以添加分页参数
  console.log('加载更多功能暂未实现（后端API不支持分页）')
}

function startTimeUpdate() {
  // 每30秒更新一次时间显示
  timeUpdateInterval.value = setInterval(() => {
    // 强制重新渲染组件以更新时间显示
    timelineItems.value = [...timelineItems.value]
  }, 30000)
}

function stopTimeUpdate() {
  if (timeUpdateInterval.value) {
    clearInterval(timeUpdateInterval.value)
  }
}

function formatTime(timestamp) {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  // 时间差计算（毫秒）
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  const weeks = Math.floor(days / 7)
  const months = Math.floor(days / 30)
  
  // 未来时间处理
  if (diff < 0) {
    return date.toLocaleString('zh-CN', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  
  // 相对时间显示（与StatusCard组件保持一致）
  if (seconds < 30) {
    return '刚刚'
  } else if (seconds < 60) {
    return `${seconds}秒前`
  } else if (minutes < 60) {
    return `${minutes}分钟前`
  } else if (hours < 24) {
    return `${hours}小时前`
  } else if (days === 1) {
    return '昨天 ' + date.toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    })
  } else if (days < 7) {
    return `${days}天前`
  } else if (weeks === 1) {
    return '1周前'
  } else if (weeks < 4) {
    return `${weeks}周前`
  } else if (months === 1) {
    return '1个月前'
  } else if (months < 12) {
    return `${months}个月前`
  } else {
    // 超过一年显示具体日期
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }
}

// 新增：切换显示全部/折叠
function toggleShowAll() {
  showAll.value = !showAll.value
}

// 新增：刷新动态数据
async function refreshTimeline() {
  currentPage.value = 0
  await fetchStatusHistory()
}
</script>

<style scoped lang="scss">
.timeline-container {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.timeline-card {
  padding: 30px;
  max-width: 800px;
  width: 100%;
}

.timeline-title {
  font-family: var(--font-heading);
  font-size: 1.3rem;
  color: white;
  margin: 0 0 30px 0;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  
  .timeline-emoji {
    margin-right: 8px;
  }
  
  .refresh-btn {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-left: 12px;
    
    &:hover:not(:disabled) {
      background: rgba(255, 255, 255, 0.2);
      transform: scale(1.1);
    }
    
    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    .refresh-icon {
      font-size: 1rem;
      transition: transform 0.3s ease;
      
      &.spinning {
        animation: spin 1s linear infinite;
      }
    }
  }
}

.timeline-content {
  position: relative;
}

.timeline-item {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 30px;
  padding-left: 20px;
  
  &.highlight {
    .timeline-content-card {
      background: rgba(255, 107, 107, 0.1);
      border-color: rgba(255, 107, 107, 0.3);
      
      &::before {
        content: '✨';
        position: absolute;
        top: -8px;
        right: -8px;
        font-size: 1.2rem;
      }
    }
  }
  
  &:last-child {
    margin-bottom: 0;
  }
}

.timeline-connector {
  position: absolute;
  left: 35px;
  top: 50px;
  width: 2px;
  height: calc(100% + 10px);
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.3),
    rgba(255, 255, 255, 0.1)
  );
}

.timeline-dot {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  position: relative;
  z-index: 2;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  
  .dot-emoji {
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  }
}

.timeline-content-card {
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  color: white;
  position: relative;
  transition: all var(--duration-normal) var(--ease-in-out);
  
  &:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
  }
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 16px;
}

.timeline-item-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  flex: 1;
}

.timeline-time {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
  white-space: nowrap;
}

.timeline-description {
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0 0 12px 0;
  opacity: 0.9;
}

.milestone-badge,
.birthday-badge,
.achievement-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.milestone-badge {
  background: rgba(233, 30, 99, 0.2);
  border: 1px solid rgba(233, 30, 99, 0.3);
}

.birthday-badge {
  background: rgba(255, 107, 107, 0.2);
  border: 1px solid rgba(255, 107, 107, 0.3);
}

.achievement-badge {
  background: rgba(76, 175, 80, 0.2);
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.load-more {
  text-align: center;
  padding-top: 20px;
  
  .load-more-btn {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.9rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0 auto;
    
    &:hover:not(:disabled) {
      background: rgba(255, 255, 255, 0.2);
      transform: translateY(-2px);
    }
    
    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    .toggle-icon {
      font-size: 1rem;
      transition: transform 0.3s ease;
    }
  }
}

.timeline-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 40px;
  gap: 16px;
  
  .loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-top: 3px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  p {
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
  }
}

.timeline-error {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 40px;
  gap: 16px;
  text-align: center;
  
  .error-icon {
    font-size: 2rem;
  }
  
  p {
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
  }
  
  .retry-btn {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      background: rgba(255, 255, 255, 0.2);
    }
  }
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 60px 20px;
  gap: 12px;
  text-align: center;
  
  .empty-icon {
    font-size: 3rem;
    opacity: 0.6;
  }
  
  p {
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
    font-size: 1.1rem;
  }
  
  small {
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.9rem;
  }
}

.timeline-user {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
  
  .user-emoji {
    font-size: 1rem;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

// 响应式设计
@media (max-width: 768px) {
  .timeline-card {
    padding: 20px;
  }
  
  .timeline-item {
    gap: 16px;
    padding-left: 16px;
  }
  
  .timeline-connector {
    left: 31px;
  }
  
  .timeline-dot {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .timeline-content-card {
    padding: 16px;
  }
  
  .timeline-header {
    flex-direction: column;
    gap: 8px;
  }
  
  .timeline-time {
    align-self: flex-start;
  }
}
</style>