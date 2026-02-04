<template>
  <div class="status-container">
    <div class="glass-card status-card">
      <!-- 状态标题 -->
      <div class="status-header">
        <h3 class="status-title">
          <span class="status-emoji">📱</span>
          双人状态实时监控
          <!-- 快速刷新按钮 -->
          <button 
            @click="manualRefresh" 
            :disabled="loading"
            class="quick-refresh-btn"
            title="立即刷新状态"
          >
            <span class="refresh-icon" :class="{ 'spinning': loading }">🔄</span>
          </button>
        </h3>
        <div class="last-update">
          {{ lastUpdateText }}
        </div>
      </div>
      
      <!-- 双人状态显示 -->
      <div class="dual-status">
        <!-- 木头状态 -->
        <div class="user-status" :class="{ 'breathing': mutouStatus.id, 'offline': !mutouStatus.isOnline }">
          <div class="user-header">
            <span class="user-emoji">🪵</span>
            <h4 class="user-name">木头</h4>
            <!-- 在线状态指示器 -->
            <div class="online-indicator" :class="{ 'online': mutouStatus.isOnline, 'offline': !mutouStatus.isOnline }">
              <span class="status-dot"></span>
              <span class="status-text">{{ mutouStatus.isOnline ? '在线' : '离线' }}</span>
            </div>
          </div>
          
          <div class="status-content" v-if="mutouStatus.id">
            <!-- 动态Emoji动画 -->
            <div class="animated-emoji" :class="`emoji-${mutouStatus.id}`">
              {{ mutouStatus.emoji }}
            </div>
            
            <!-- 状态描述 -->
            <div class="status-description">
              <h5 class="status-name">{{ mutouStatus.name }}</h5>
              <p class="status-detail">{{ mutouStatus.description }}</p>
            </div>
            
            <!-- 状态颜色指示器 -->
            <div 
              class="status-indicator" 
              :style="{ backgroundColor: mutouStatus.color }"
            />
          </div>
          
          <!-- 加载状态 -->
          <div v-else class="status-loading">
            <div class="loading-spinner"></div>
            <p>获取中...</p>
          </div>
        </div>
        
        <!-- 乾雨状态 -->
        <div class="user-status" :class="{ 'breathing': qianyuStatus.id, 'offline': !qianyuStatus.isOnline }">
          <div class="user-header">
            <span class="user-emoji">🦅</span>
            <h4 class="user-name">乾雨</h4>
            <!-- 在线状态指示器 -->
            <div class="online-indicator" :class="{ 'online': qianyuStatus.isOnline, 'offline': !qianyuStatus.isOnline }">
              <span class="status-dot"></span>
              <span class="status-text">{{ qianyuStatus.isOnline ? '在线' : '离线' }}</span>
            </div>
          </div>
          
          <div class="status-content" v-if="qianyuStatus.id">
            <!-- 动态Emoji动画 -->
            <div class="animated-emoji" :class="`emoji-${qianyuStatus.id}`">
              {{ qianyuStatus.emoji }}
            </div>
            
            <!-- 状态描述 -->
            <div class="status-description">
              <h5 class="status-name">{{ qianyuStatus.name }}</h5>
              <p class="status-detail">{{ qianyuStatus.description }}</p>
            </div>
            
            <!-- 状态颜色指示器 -->
            <div 
              class="status-indicator" 
              :style="{ backgroundColor: qianyuStatus.color }"
            />
          </div>
          
          <!-- 加载状态 -->
          <div v-else class="status-loading">
            <div class="loading-spinner"></div>
            <p>获取中...</p>
          </div>
        </div>
      </div>
      
      <!-- 状态历史 -->
      <div class="status-history" v-if="statusHistory.length > 0">
        <h5 class="history-title">最近状态</h5>
        <div class="history-timeline">
          <div 
            v-for="item in statusHistory.slice(0, 3)" 
            :key="`${item.timestamp}-${item.status}-${item.user}`"
            class="history-item"
          >
            <div class="history-time">{{ formatTime(item.timestamp) }}</div>
            <div class="history-status">
              <span class="history-user">{{ getUserEmoji(item.user) }}</span>
              <span class="history-emoji">{{ getStatusById(item.status)?.emoji }}</span>
              <span class="history-name">{{ getStatusById(item.status)?.name }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 互动按钮 -->
      <div class="status-actions">
        <button 
          class="action-btn like-btn"
          @click="likeStatus"
          :class="{ 'liked': hasLiked }"
        >
          <span class="btn-emoji">{{ hasLiked ? '❤️' : '🤍' }}</span>
          <span class="btn-text">{{ hasLiked ? '已点赞' : '点赞' }}</span>
        </button>
      </div>
      
    </div>
    
    <!-- 状态更新通知 -->
    <transition name="notification">
      <div v-if="showNotification" class="status-notification">
        <span class="notification-emoji">✨</span>
        <span class="notification-text">{{ notificationText }}</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { gsap } from 'gsap'

// 响应式状态
const mutouStatus = ref({})
const qianyuStatus = ref({})
const statusHistory = ref([])
const lastUpdate = ref(null)
const hasLiked = ref(false)
const showNotification = ref(false)
const notificationText = ref('')
const pollingInterval = ref(null)
const timeUpdateInterval = ref(null)
const loading = ref(false) // 新增：用于控制快速刷新按钮的加载状态

// 状态配置（基于后端文档）
const statusConfig = {
  1: { 
    id: 1, 
    name: '睡觉中', 
    emoji: '😴', 
    description: '正在做美梦zzz...', 
    color: '#9B59B6' 
  },
  2: { 
    id: 2, 
    name: '工作中', 
    emoji: '💻', 
    description: '正在努力工作', 
    color: '#3498DB' 
  },
  3: { 
    id: 3, 
    name: '运动中', 
    emoji: '🏃‍♀️', 
    description: '正在运动💪', 
    color: '#E74C3C' 
  },
  4: { 
    id: 4, 
    name: '看B站', 
    emoji: '📱', 
    description: '正在刷B站', 
    color: '#FF69B4' 
  },
  5: { 
    id: 5, 
    name: '玩游戏', 
    emoji: '🎮', 
    description: '在游戏世界里', 
    color: '#F39C12' 
  },
  6: {
    id: 6,
    name: '听音乐',
    emoji: '🎵',
    description: '正在享受音乐',
    color: '#1ABC9C'
  },
  7: {
    id: 7,
    name: '学习中',
    emoji: '📚',
    description: '在认真学习',
    color: '#8E44AD'
  },
  8: {
    id: 8,
    name: '做饭中',
    emoji: '👩‍🍳',
    description: '在准备美食',
    color: '#E67E22'
  }
}

// 计算属性
const lastUpdateText = computed(() => {
  if (!lastUpdate.value) return '暂无更新'
  return formatLastUpdateTime(lastUpdate.value)
})

// 生命周期
onMounted(() => {
  fetchCurrentStatus()
  startPolling()
  loadStatusHistory()
  startTimeUpdate()
})

onUnmounted(() => {
  stopPolling()
  stopTimeUpdate()
})

// 方法
async function fetchCurrentStatus() {
  loading.value = true // 开始加载
  try {
    // 使用API配置文件
    const { api } = useApi()
    // 真实的API调用 - 获取所有用户状态（符合前后端交流文档）
    const response = await fetch(api.baseURL + '/query')
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    
    const data = await response.json()
    
    // 处理API响应
    if (data.users) {
      // 多用户响应格式 - 符合文档规范
      const users = data.users
      
      // 更新木头状态
      if (users.木头) {
        const mutouData = users.木头
        const statusInfo = statusConfig[mutouData.status]
        if (statusInfo) {
          mutouStatus.value = {
            ...statusInfo,
            last_update: mutouData.last_update,
            isOnline: isUserOnline(mutouData.last_update)
          }
          addToHistory('木头', mutouData.status, mutouData.last_update)
        } else {
          // 如果状态信息不存在，使用默认状态
          mutouStatus.value = {
            id: mutouData.status,
            name: '未知状态',
            emoji: '❓',
            description: '状态信息获取中...',
            color: '#95A5A6',
            last_update: mutouData.last_update,
            isOnline: isUserOnline(mutouData.last_update)
          }
        }
      } else {
        // 如果没有用户数据，设置默认状态
        mutouStatus.value = {
          id: '2',
          name: '离线',
          emoji: '🔌',
          description: '连接服务器中...',
          color: '#95A5A6',
          last_update: null,
          isOnline: false
        }
      }
      
      // 更新乾雨状态
      if (users.乾雨) {
        const qianyuData = users.乾雨
        const statusInfo = statusConfig[qianyuData.status]
        if (statusInfo) {
          qianyuStatus.value = {
            ...statusInfo,
            last_update: qianyuData.last_update,
            isOnline: isUserOnline(qianyuData.last_update)
          }
          addToHistory('乾雨', qianyuData.status, qianyuData.last_update)
        } else {
          // 如果状态信息不存在，使用默认状态
          qianyuStatus.value = {
            id: qianyuData.status,
            name: '未知状态',
            emoji: '❓',
            description: '状态信息获取中...',
            color: '#95A5A6',
            last_update: qianyuData.last_update,
            isOnline: isUserOnline(qianyuData.last_update)
          }
        }
      } else {
        // 如果没有用户数据，设置默认状态
        qianyuStatus.value = {
          id: '1',
          name: '离线',
          emoji: '🔌',
          description: '连接服务器中...',
          color: '#95A5A6',
          last_update: null,
          isOnline: false
        }
      }
      
      lastUpdate.value = new Date(data.timestamp)
      
      // 显示连接成功通知（仅首次）
      if (!mutouStatus.value.id && !qianyuStatus.value.id) {
        showNotificationMessage('📡 已连接到状态监控服务')
      }
      
    } else if (data.user) {
      // 单用户响应格式处理（兼容性）
      console.warn('收到单用户响应格式，建议使用多用户查询接口')
      const statusInfo = statusConfig[data.status]
      if (statusInfo && data.user === '木头') {
        mutouStatus.value = {
          ...statusInfo,
          last_update: data.last_update,
          isOnline: isUserOnline(data.last_update)
        }
      } else if (statusInfo && data.user === '乾雨') {
        qianyuStatus.value = {
          ...statusInfo,
          last_update: data.last_update,
          isOnline: isUserOnline(data.last_update)
        }
      }
      lastUpdate.value = new Date(data.timestamp)
    } else {
      throw new Error('API响应格式不正确')
    }
    
  } catch (error) {
    console.error('获取状态失败:', error)
    
    // 显示错误通知
    if (error.message.includes('Failed to fetch')) {
      showNotificationMessage('🔌 连接服务器失败，使用离线模式')
    } else {
      showNotificationMessage(`⚠️ ${error.message}`)
    }
    
    // 网络错误时使用备用数据
    const fallbackData = {
      users: {
        木头: {
          display_name: '木头',
          emoji: '🪵',
          status: '2',
          name: '工作中',
          description: '连接服务器中...',
          color: '#3498DB',
          last_update: new Date(Date.now() - 300000).toISOString(),
          isOnline: false
        },
        乾雨: {
          display_name: '乾雨',
          emoji: '🦅',
          status: '1',
          name: '睡觉中',
          description: '连接服务器中...',
          color: '#9B59B6',
          last_update: new Date(Date.now() - 600000).toISOString(),
          isOnline: false
        }
      },
      timestamp: new Date().toISOString()
    }
    
    // 使用备用数据
    const users = fallbackData.users
    
    // 更新木头状态
    const mutouData = users.木头
    const mutouStatusInfo = statusConfig[mutouData.status]
    if (mutouStatusInfo) {
      mutouStatus.value = {
        ...mutouStatusInfo,
        description: mutouData.description, // 使用备用描述
        last_update: mutouData.last_update,
        isOnline: false
      }
    }
    
    // 更新乾雨状态
    const qianyuData = users.乾雨
    const qianyuStatusInfo = statusConfig[qianyuData.status]
    if (qianyuStatusInfo) {
      qianyuStatus.value = {
        ...qianyuStatusInfo,
        description: qianyuData.description, // 使用备用描述
        last_update: qianyuData.last_update,
        isOnline: false
      }
    }
    
    lastUpdate.value = new Date(fallbackData.timestamp)
  } finally {
    loading.value = false // 结束加载
  }
}

// 新增：判断用户是否在线（基于文档中的在线状态判断逻辑）
function isUserOnline(lastUpdateTime) {
  if (!lastUpdateTime || lastUpdateTime === '从未更新') return false
  
  try {
    const lastTime = new Date(lastUpdateTime)
    const now = new Date()
    const diffMinutes = (now.getTime() - lastTime.getTime()) / (1000 * 60)
    
    // 10分钟内有更新认为在线（符合前后端文档的在线判断逻辑）
    return diffMinutes <= 10
  } catch (error) {
    console.warn('解析最后更新时间失败:', error)
    return false
  }
}

// 新增：获取状态历史的API调用（可选功能，增强历史记录显示）
async function fetchRecentStatusHistory() {
  try {
    const { api } = useApi()
    const response = await fetch(api.baseURL + '/history')
    const data = await response.json()
    
    if (data.history && Array.isArray(data.history)) {
      // 只保留最近的5条记录用于显示
      const recentHistory = data.history.slice(0, 5).map(item => ({
        user: item.user,
        status: item.status_id,
        timestamp: new Date(item.timestamp).getTime(),
        userName: item.display_name || item.user,
        userEmoji: item.emoji || getUserEmoji(item.user)
      }))
      
      // 合并到现有历史记录中，去重
      recentHistory.forEach(newItem => {
        const existingIndex = statusHistory.value.findIndex(
          existing => existing.user === newItem.user && 
                     existing.status === newItem.status &&
                     Math.abs(existing.timestamp - newItem.timestamp) < 60000 // 1分钟内不重复
        )
        
        if (existingIndex === -1) {
          statusHistory.value.unshift(newItem)
        }
      })
      
      // 保持历史记录不超过10条
      if (statusHistory.value.length > 10) {
        statusHistory.value = statusHistory.value.slice(0, 10)
      }
      
      // 保存到本地存储
      localStorage.setItem('statusHistory', JSON.stringify(statusHistory.value))
    }
  } catch (error) {
    console.warn('获取状态历史失败:', error)
  }
}

function startPolling() {
  // 每30秒轮询一次状态更新（符合文档建议的轮询频率）
  pollingInterval.value = setInterval(() => {
    fetchCurrentStatus()
    // 同时获取最新的历史记录
    fetchRecentStatusHistory()
  }, 30000)
}

function stopPolling() {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
  }
}

function startTimeUpdate() {
  // 每30秒更新一次时间显示
  timeUpdateInterval.value = setInterval(() => {
    // 触发计算属性重新计算
    lastUpdate.value = lastUpdate.value
  }, 30000)
}

function stopTimeUpdate() {
  if (timeUpdateInterval.value) {
    clearInterval(timeUpdateInterval.value)
  }
}

function addToHistory(user, statusId, timestamp) {
  const timestampMs = new Date(timestamp).getTime()
  const existingIndex = statusHistory.value.findIndex(
    item => item.user === user && item.status === statusId && 
    Math.abs(item.timestamp - timestampMs) < 60000 // 1分钟内不重复添加
  )
  
  if (existingIndex === -1) {
    statusHistory.value.unshift({
      user: user,
      status: statusId,
      timestamp: timestampMs,
      userName: user,
      userEmoji: getUserEmoji(user)
    })
    
    // 只保留最近10条记录
    if (statusHistory.value.length > 10) {
      statusHistory.value = statusHistory.value.slice(0, 10)
    }
    
    // 保存到本地存储
    localStorage.setItem('statusHistory', JSON.stringify(statusHistory.value))
  }
}

function loadStatusHistory() {
  const saved = localStorage.getItem('statusHistory')
  if (saved) {
    try {
      statusHistory.value = JSON.parse(saved)
    } catch (error) {
      console.error('加载状态历史失败:', error)
    }
  }
}

function getStatusById(id) {
  return statusConfig[id]
}

function getUserEmoji(username) {
  const userEmojis = {
    '木头': '🪵',
    '乾雨': '🦅'
  }
  return userEmojis[username] || '👤'
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
  
  // 相对时间显示
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

// 添加专门的最后更新时间格式化函数
function formatLastUpdateTime(timestamp) {
  if (!timestamp) return '从未更新'
  
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (minutes < 1) {
    return '刚刚更新'
  } else if (minutes < 60) {
    return `${minutes}分钟前更新`
  } else if (hours < 24) {
    return `${hours}小时前更新`
  } else if (days === 1) {
    return '昨天更新'
  } else if (days < 30) {
    return `${days}天前更新`
  } else {
    return date.toLocaleDateString('zh-CN', {
      month: 'short',
      day: 'numeric'
    }) + '更新'
  }
}

function likeStatus() {
  hasLiked.value = !hasLiked.value
  
  if (hasLiked.value) {
    showNotificationMessage('已为大家点赞 ❤️')
    
    // 点赞动画
    gsap.fromTo('.like-btn', 
      { scale: 1 },
      { 
        scale: 1.2, 
        duration: 0.2, 
        yoyo: true, 
        repeat: 1,
        ease: "power2.out"
      }
    )
  }
}

function showNotificationMessage(message, isError = false) {
  notificationText.value = message
  showNotification.value = true
  
  // 根据是否为错误改变通知样式
  if (isError) {
    document.querySelector('.status-notification')?.classList.add('error')
  } else {
    document.querySelector('.status-notification')?.classList.remove('error')
  }
  
  setTimeout(() => {
    showNotification.value = false
  }, 3000)
}

function manualRefresh() {
  fetchCurrentStatus()
  fetchRecentStatusHistory()
  showNotificationMessage('状态已刷新')
}
</script>

<style scoped lang="scss">
.status-container {
  padding: 20px;
  display: flex;
  justify-content: center;
  position: relative;
}

.status-card {
  padding: 30px;
  max-width: 800px;
  width: 100%;
  text-align: center;
  position: relative;
}

.status-header {
  margin-bottom: 30px;
  
  .status-title {
    font-family: var(--font-heading);
    font-size: 1.3rem;
    color: white;
    margin: 0 0 8px 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    
    .status-emoji {
      margin-right: 8px;
    }
    
    .quick-refresh-btn {
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
  
  .last-update {
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.7);
  }
}

.dual-status {
  display: flex;
  gap: 24px;
  margin-bottom: 30px;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 16px;
  }
}

.user-status {
  flex: 1;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  
  &.breathing {
    animation: breathing 3s ease-in-out infinite;
  }
  
  .user-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-bottom: 16px;
    flex-wrap: wrap;
    
    .user-emoji {
      font-size: 1.5rem;
    }
    
    .user-name {
      font-size: 1.1rem;
      color: white;
      margin: 0;
      font-weight: 600;
    }
  }
  
  .online-indicator {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 0.75rem;
    padding: 2px 6px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    
    .status-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    
    .status-text {
      font-weight: 500;
    }
    
    &.online {
      .status-dot {
        background-color: #4CAF50;
        animation: pulse-green 2s infinite;
      }
      .status-text {
        color: #4CAF50;
      }
    }
    
    &.offline {
      .status-dot {
        background-color: #757575;
      }
      .status-text {
        color: #757575;
      }
    }
  }
  
  // 添加离线状态的整体样式
  &.offline {
    opacity: 0.7;
    filter: grayscale(20%);
  }
  
  @keyframes pulse-green {
    0% { 
      box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); 
    }
    70% { 
      box-shadow: 0 0 0 6px rgba(76, 175, 80, 0); 
    }
    100% { 
      box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); 
    }
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
}

@keyframes breathing {
  0%, 100% { 
    transform: scale(1);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
  }
  50% { 
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
  }
}

.status-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  position: relative;
}

.animated-emoji {
  font-size: 4rem;
  position: relative;
  
  // 不同状态的动画
  &.emoji-1 { // 睡觉
    animation: sleeping 3s ease-in-out infinite;
  }
  
  &.emoji-2 { // 工作
    animation: typing 1s linear infinite;
  }
  
  &.emoji-3 { // 运动
    animation: running 0.8s linear infinite;
  }
  
  &.emoji-4 { // 看B站
    animation: browsing 2s ease-in-out infinite;
  }
  
  &.emoji-5 { // 游戏
    animation: gaming 1.5s ease-in-out infinite;
  }
  
  &.emoji-6 { // 音乐
    animation: music 2s ease-in-out infinite;
  }
  
  &.emoji-7 { // 学习
    animation: studying 2.5s ease-in-out infinite;
  }
  
  &.emoji-8 { // 做饭
    animation: cooking 1.8s ease-in-out infinite;
  }
}

// Emoji动画定义
@keyframes sleeping {
  0%, 100% { transform: rotate(-5deg) scale(1); }
  50% { transform: rotate(5deg) scale(1.05); }
}

@keyframes typing {
  0%, 50% { transform: scale(1); }
  25%, 75% { transform: scale(1.1); }
}

@keyframes running {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes browsing {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1) rotate(5deg); }
}

@keyframes gaming {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
}

@keyframes music {
  0%, 100% { transform: scale(1) rotate(0deg); }
  33% { transform: scale(1.1) rotate(-5deg); }
  66% { transform: scale(1.1) rotate(5deg); }
}

@keyframes studying {
  0%, 100% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.05) rotate(-2deg); }
}

@keyframes cooking {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-5px) rotate(-5deg); }
  75% { transform: translateY(-3px) rotate(5deg); }
}

.status-description {
  text-align: center;
  color: white;
  
  .status-name {
    font-size: 1.2rem;
    margin: 0 0 8px 0;
    font-weight: 600;
  }
  
  .status-detail {
    font-size: 0.95rem;
    margin: 0;
    opacity: 0.9;
  }
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  position: absolute;
  top: -5px;
  right: -5px;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
  animation: pulse-indicator 2s ease-in-out infinite;
}

@keyframes pulse-indicator {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.5); opacity: 0.7; }
}

.status-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: rgba(255, 255, 255, 0.8);
  
  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.2);
    border-top: 3px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.status-history {
  margin-bottom: 20px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  
  .history-title {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.8);
    margin: 0 0 16px 0;
    text-align: left;
  }
  
  .history-timeline {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .history-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    font-size: 0.85rem;
    
    .history-time {
      color: rgba(255, 255, 255, 0.6);
    }
    
    .history-status {
      color: white;
      display: flex;
      align-items: center;
      gap: 4px;
      
      .history-user {
        font-size: 0.9rem;
        margin-right: 2px;
      }
      
      .history-emoji {
        margin-right: 6px;
      }
    }
  }
}

.status-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 20px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }
  
  &.liked {
    background: rgba(255, 107, 107, 0.3);
    border-color: rgba(255, 107, 107, 0.5);
  }
}

.status-notification {
  &.error {
    background: rgba(220, 53, 69, 0.9);
  }
}

.status-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 12px 20px;
  border-radius: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 1000;
  backdrop-filter: blur(10px);
  
  .notification-emoji {
    font-size: 1.1rem;
  }
}

// 过渡动画
.notification-enter-active,
.notification-leave-active {
  transition: all var(--duration-normal) var(--ease-in-out);
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

// 响应式设计
@media (max-width: 768px) {
  .status-card {
    padding: 20px;
  }
  
  .animated-emoji {
    font-size: 3rem;
  }
  
  .status-actions {
    flex-direction: column;
  }
  
  .action-btn {
    justify-content: center;
  }
}
</style>