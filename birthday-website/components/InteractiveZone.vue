<template>
  <div class="interactive-container">
    <!-- 留言板区域 -->
    <div class="message-board-section cork-board">
      <!-- 软木板纹理 -->
      <div class="cork-texture"></div>
      
      <h3 class="section-title text-heading">
        <span class="section-emoji">📌</span>
        留言便利贴
      </h3>
      
      <!-- 留言输入区 -->
      <div class="message-input-area sticky-note input-note">
        <div class="pin-tack"></div>
        <div class="user-info-input">
          <label class="user-label">我是：</label>
          <input 
            v-model="userName" 
            placeholder="你的名字" 
            class="name-input text-handwriting"
          />
        </div>
        <textarea 
          :value="editingMessage ? editingMessage.message : newMessage"
          @input="updateMessage"
          :placeholder="editingMessage ? '编辑留言...' : '给木头写张小纸条...'"
          class="message-textarea text-handwriting"
          @keydown.ctrl.enter="editingMessage ? saveEdit() : sendMessage()"
        />
        <div class="input-buttons">
          <button 
            @click="editingMessage ? saveEdit() : sendMessage()" 
            class="send-message-btn text-heading"
            :disabled="isLoading"
          >
            {{ isLoading ? '贴上去...' : (editingMessage ? '保存修改 ✅' : '贴上去 📌') }}
          </button>
          <button 
            v-if="editingMessage"
            @click="cancelEdit()" 
            class="cancel-btn text-heading"
          >
            取消
          </button>
        </div>
      </div>
      
      <!-- 留言展示区 -->
      <div class="messages-container">
        <div 
          v-for="message in messages" 
          :key="message.id"
          class="message-note sticky-note"
          :class="{ 'editing': editingMessage && editingMessage.id === message.id }"
          :style="{ 
            backgroundColor: message.color,
            transform: `rotate(${message.rotation}deg)`,
            top: `${message.y}%`,
            left: `${message.x}%`
          }"
        >
          <div class="pin-tack"></div>
          <div class="message-content text-handwriting">
            <span class="message-user">{{ message.user }}:</span>
            {{ message.message }}
          </div>
          <div class="message-footer">
            <div class="message-time">{{ formatMessageTime(message.timestamp) }}</div>
            <div class="message-actions">
              <button @click="editMessage(message)" class="action-btn">✏️</button>
              <button @click="deleteMessage(message.id)" class="action-btn">🗑️</button>
            </div>
          </div>
        </div>
        
        <!-- 空状态提示 -->
        <div v-if="messages.length === 0" class="empty-state">
          <div class="empty-icon">💌</div>
          <p class="empty-text text-handwriting">还没有留言哦～快来贴第一张！</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

// API实例
const { api } = useApi()

// 留言板功能
const newMessage = ref('')
const userName = ref('') // 用户名字
const messages = ref([])
const editingMessage = ref(null)
const isLoading = ref(false)

// 生命周期
onMounted(async () => {
  // 尝试从本地存储获取上次的名字
  const savedName = localStorage.getItem('visitor_name')
  if (savedName) userName.value = savedName
  
  await loadMessages()
})

// 留言板方法
async function loadMessages() {
  try {
    const data = await api.getMessages()
    // 为每条消息生成随机位置和颜色
    messages.value = data.map(msg => ({
      ...msg,
      color: getRandomColor(),
      rotation: Math.random() * 10 - 5,
      // 随机位置逻辑需要优化，防止重叠过于严重，这里简化处理
      // 实际应用中可能需要网格布局或更复杂的算法
      x: Math.random() * 80, // 0-80%
      y: Math.random() * 80  // 0-80%
    }))
  } catch (error) {
    console.error('加载留言失败:', error)
  }
}

function updateMessage(event) {
  const value = event.target.value
  if (editingMessage.value) {
    editingMessage.value.message = value
  } else {
    newMessage.value = value
  }
}

async function sendMessage() {
  if (newMessage.value.trim()) {
    isLoading.value = true
    
    // 保存名字到本地
    if (userName.value) {
      localStorage.setItem('visitor_name', userName.value)
    }

    try {
      const result = await api.sendMessage(newMessage.value, userName.value || '神秘访客')
      if (result && result.success) {
        const message = {
          ...result.data,
          color: getRandomColor(),
          rotation: Math.random() * 10 - 5,
          x: Math.random() * 60 + 10, // 稍微集中一点
          y: Math.random() * 60 + 10
        }
        
        messages.value.unshift(message) // 添加到最前面
        newMessage.value = ''
      }
    } catch (error) {
      console.error('发送留言失败:', error)
    } finally {
      isLoading.value = false
    }
  }
}

function editMessage(message) {
  editingMessage.value = { ...message }
  // 滚动到输入框
  document.querySelector('.message-input-area')?.scrollIntoView({ behavior: 'smooth' })
}

async function saveEdit() {
  if (editingMessage.value && editingMessage.value.message.trim()) {
    isLoading.value = true
    try {
      const result = await api.updateMessage(editingMessage.value.id, editingMessage.value.message)
      if (result && result.success) {
        const index = messages.value.findIndex(m => m.id === editingMessage.value.id)
        if (index !== -1) {
          messages.value[index] = {
            ...messages.value[index],
            ...result.updated_message
          }
          cancelEdit()
        }
      }
    } catch (error) {
      console.error('更新留言失败:', error)
    } finally {
      isLoading.value = false
    }
  }
}

function cancelEdit() {
  editingMessage.value = null
}

async function deleteMessage(messageId) {
  if (confirm('确定要撕掉这张便利贴吗？')) {
    try {
      const result = await api.deleteMessage(messageId)
      if (result && result.success) {
        messages.value = messages.value.filter(m => m.id !== messageId)
        if (editingMessage.value && editingMessage.value.id === messageId) {
          cancelEdit()
        }
      }
    } catch (error) {
      console.error('删除留言失败:', error)
    }
  }
}

function getRandomColor() {
  // 柔和的便利贴颜色
  const colors = [
    '#fff740', // 黄
    '#ff7eb9', // 粉
    '#7afcff', // 蓝
    '#feff9c', // 浅黄
    '#fff655'  // 柠檬黄
  ]
  return colors[Math.floor(Math.random() * colors.length)]
}

function formatMessageTime(timestamp) {
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', { 
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit', 
    minute: '2-digit' 
  })
}
</script>

<style scoped lang="scss">
.interactive-container {
  padding: 20px;
  display: flex;
  justify-content: center;
  width: 100%;
}

.cork-board {
  position: relative;
  width: 100%;
  max-width: 800px;
  min-height: 600px;
  background-color: #6d4c41;
  border: 10px solid #5d4037;
  border-radius: 4px;
  padding: 20px;
  box-shadow: inset 0 0 20px rgba(0,0,0,0.5), 0 10px 20px rgba(0,0,0,0.2);
  overflow: hidden;
}

.cork-texture {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg width='200' height='200' viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.2'/%3E%3C/svg%3E");
  opacity: 0.6;
  pointer-events: none;
}

.section-title {
  text-align: center;
  color: white;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
  margin-bottom: 30px;
  position: relative;
  z-index: 2;
  font-size: 1.8rem;
}

.sticky-note {
  background: #fff740;
  padding: 15px;
  box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
  position: relative;
  transition: transform 0.2s;
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    right: 0;
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, transparent 50%, rgba(0,0,0,0.1) 50%);
    pointer-events: none;
  }
}

.pin-tack {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 12px;
  height: 12px;
  background: #f44336;
  border-radius: 50%;
  box-shadow: 1px 1px 2px rgba(0,0,0,0.3);
  z-index: 5;
  
  &::after {
    content: '';
    position: absolute;
    top: 3px;
    left: 3px;
    width: 4px;
    height: 4px;
    background: rgba(255,255,255,0.5);
    border-radius: 50%;
  }
}

.input-note {
  max-width: 400px;
  margin: 0 auto 40px;
  transform: rotate(-2deg);
  z-index: 10;
  
  &:hover {
    transform: rotate(0) scale(1.02);
    z-index: 20;
  }
}

.message-textarea {
  width: 100%;
  min-height: 100px;
  border: none;
  background: transparent;
  resize: none;
  outline: none;
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 10px;
  
  &::placeholder {
    color: rgba(0,0,0,0.4);
  }
}

.user-info-input {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  
  .user-label {
    font-size: 0.9rem;
    color: #666;
    margin-right: 5px;
  }
  
  .name-input {
    border: none;
    border-bottom: 1px dashed #999;
    background: transparent;
    padding: 2px 5px;
    font-size: 1rem;
    color: #333;
    width: 120px;
    outline: none;
    
    &:focus {
      border-bottom-color: #ff4081;
    }
  }
}

.message-user {
  font-weight: bold;
  color: #d84315;
  margin-right: 5px;
  font-size: 0.95rem;
}
.input-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.send-message-btn, .cancel-btn {
  border: none;
  padding: 5px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: opacity 0.2s;
  
  &:hover {
    opacity: 0.8;
  }
}

.send-message-btn {
  background: #ff4081;
  color: white;
}

.cancel-btn {
  background: #9e9e9e;
  color: white;
}

.messages-container {
  position: relative;
  min-height: 400px;
  // 使用 CSS Grid 或 Flex 在移动端可能更好，这里为了模拟散乱效果使用 absolute
  // 但为了响应式，我们简单地使用 Grid
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  padding: 20px;
}

.message-note {
  min-height: 150px;
  display: flex;
  flex-direction: column;
  cursor: grab;
  
  // 覆盖之前的 absolute 定位逻辑，使用 grid 布局更稳健
  position: relative !important;
  top: auto !important;
  left: auto !important;
  
  &:hover {
    transform: scale(1.05) rotate(0deg) !important;
    z-index: 10;
  }
}

.message-content {
  flex: 1;
  font-size: 1rem;
  line-height: 1.4;
  margin-bottom: 10px;
  word-break: break-all;
}

.message-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: #666;
  border-top: 1px dashed rgba(0,0,0,0.1);
  padding-top: 5px;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 2px;
  opacity: 0.6;
  
  &:hover {
    opacity: 1;
  }
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  color: rgba(255,255,255,0.8);
  margin-top: 50px;
  
  .empty-icon {
    font-size: 4rem;
    margin-bottom: 10px;
  }
}

// 移动端适配
@media (max-width: 480px) {
  .cork-board {
    padding: 10px;
    border-width: 5px;
  }
  
  .messages-container {
    grid-template-columns: repeat(2, 1fr); // 两列布局
    gap: 10px;
  }
  
  .message-note {
    min-height: 120px;
    padding: 10px;
  }
  
  .message-content {
    font-size: 0.9rem;
  }
}
</style>
