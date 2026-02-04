<template>
  <div class="interactive-container">
    <!-- 留言板区域 -->
    <div class="glass-card message-board-section">
      <h3 class="section-title">
        <span class="section-emoji">💌</span>
        留言板
      </h3>
      
      <!-- 留言输入区 -->
      <div class="message-input-area">
        <textarea 
          :value="editingMessage ? editingMessage.message : newMessage"
          @input="updateMessage"
          :placeholder="editingMessage ? '编辑留言...' : '给木头留个小纸条...'"
          class="message-textarea"
          @keydown.ctrl.enter="editingMessage ? saveEdit() : sendMessage()"
        />
        <div class="input-buttons">
          <button 
            @click="editingMessage ? saveEdit() : sendMessage()" 
            class="send-message-btn"
            :disabled="isLoading"
          >
            {{ isLoading ? '发送中...' : (editingMessage ? '保存修改 ✅' : '发送小纸条 💌') }}
          </button>
          <button 
            v-if="editingMessage"
            @click="cancelEdit()" 
            class="cancel-btn"
          >
            取消编辑
          </button>
        </div>
      </div>
      
      <!-- 留言展示区 -->
      <div class="messages-container">
        <div 
          v-for="message in messages" 
          :key="message.id"
          class="message-note"
          :class="{ 'editing': editingMessage && editingMessage.id === message.id }"
          :style="{ 
            backgroundColor: message.color,
            transform: `rotate(${message.rotation}deg)`,
            top: `${message.y}px`,
            left: `${message.x}px`
          }"
        >
          <div class="message-content">{{ message.message }}</div>
          <div class="message-time">{{ formatMessageTime(message.timestamp) }}</div>
          <div class="message-actions">
            <button 
              @click="editMessage(message)"
              class="edit-btn"
              title="编辑"
            >
              ✏️
            </button>
            <button 
              @click="deleteMessage(message.id)"
              class="delete-btn"
              title="删除"
            >
              🗑️
            </button>
          </div>
        </div>
        
        <!-- 空状态提示 -->
        <div v-if="messages.length === 0" class="empty-state">
          <div class="empty-icon">💌</div>
          <p class="empty-text">还没有留言哦～给木头留个小纸条吧！</p>
        </div>
      </div>
    </div>

    <!-- 甜蜜时刻照片墙 -->
    <div class="glass-card photo-gallery-section">
      <h3 class="section-title">
        <span class="section-emoji">📸</span>
        甜蜜时刻
      </h3>
      
      <!-- 照片墙内容 -->
      <div class="photo-gallery-bg" v-if="displayPhotos.length > 0">
        <div class="waterfall-container">
          <div 
            v-for="(photo, index) in displayPhotos" 
            :key="photo.id"
            class="waterfall-item"
            :style="{
              animationDelay: `${photo.delay}s`,
              width: `${photo.width}px`,
              height: `${photo.height}px`
            }"
          >
            <img 
              :src="photo.url" 
              :alt="photo.filename"
              class="waterfall-image"
              @load="onImageLoad"
              @error="onImageError"
            />
          </div>
        </div>
      </div>
      
      <!-- 照片墙空状态 -->
      <div v-else class="photo-empty-state">
        <div class="empty-icon">📷</div>
        <p class="empty-text">暂无照片</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { gsap } from 'gsap'
import { useApi } from '~/composables/useApi'
import { usePhotoGallery } from '~/composables/usePhotoGallery'

// API实例 (只用于留言板)
const { api } = useApi()

// 照片墙功能 (使用本地图片)
const { photos, hasPhotos, loadPhotos } = usePhotoGallery()
const displayPhotos = ref([])
const loadedImagesCount = ref(0)

// 留言板功能
const newMessage = ref('')
const messages = ref([])
const editingMessage = ref(null)
const isLoading = ref(false)

// 生命周期
onMounted(async () => {
  // 加载本地照片
  await loadPhotos()
  initPhotoGallery()
  
  // 加载留言
  await loadMessages()
})

// 照片墙方法
async function initPhotoGallery() {
  if (!hasPhotos.value || photos.value.length === 0) {
    console.log('没有找到照片')
    return
  }
  
  // 为照片墙选择合适数量的照片
  const neededPhotos = Math.min(photos.value.length, 15) // 限制显示数量
  
  displayPhotos.value = photos.value.slice(0, neededPhotos).map((photo, index) => {
    const baseSize = 160
    const sizeVariation = Math.random() * 40 - 20
    const finalSize = Math.max(baseSize + sizeVariation, baseSize * 0.8)
    
    return {
      ...photo,
      id: `${photo.id}-${index}`,
      delay: index * 0.1,
      width: finalSize,
      height: finalSize * (0.8 + Math.random() * 0.4),
    }
  })
  
  // 启动照片墙动画
  nextTick(() => {
    animatePhotoGallery()
  })
}

function animatePhotoGallery() {
  const items = document.querySelectorAll('.waterfall-item')
  
  items.forEach((item, index) => {
    gsap.set(item, {
      opacity: 0,
      y: 50,
      scale: 0.8,
      rotation: Math.random() * 20 - 10
    })
    
    gsap.to(item, {
      opacity: 1,
      y: 0,
      scale: 1,
      rotation: 0,
      duration: 0.6,
      delay: index * 0.1,
      ease: "back.out(1.7)",
      onComplete: () => {
        // 添加悬停效果
        item.addEventListener('mouseenter', () => {
          gsap.to(item, {
            scale: 1.05,
            rotation: Math.random() * 10 - 5,
            duration: 0.3,
            ease: "power2.out"
          })
        })
        
        item.addEventListener('mouseleave', () => {
          gsap.to(item, {
            scale: 1,
            rotation: 0,
            duration: 0.3,
            ease: "power2.out"
          })
        })
      }
    })
    
    // 持续的浮动动画
    gsap.to(item, {
      y: "+=10",
      duration: 3 + Math.random() * 2,
      yoyo: true,
      repeat: -1,
      ease: "sine.inOut",
      delay: Math.random() * 2
    })
  })
}

function onImageLoad() {
  loadedImagesCount.value++
}

function onImageError(event) {
  console.warn('图片加载失败:', event.target.src)
  event.target.style.display = 'none'
}

// 留言板方法
async function loadMessages() {
  try {
    const data = await api.getMessages()
    messages.value = data.map(msg => ({
      ...msg,
      color: getRandomColor(),
      rotation: Math.random() * 10 - 5,
      x: Math.random() * 200,
      y: Math.random() * 100
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
    try {
      const result = await api.sendMessage(newMessage.value)
      if (result && result.success) {
        const message = {
          ...result.data,
          color: getRandomColor(),
          rotation: Math.random() * 10 - 5,
          x: Math.random() * 200,
          y: Math.random() * 100
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
            ...result.updated_message,
            color: messages.value[index].color,
            rotation: messages.value[index].rotation,
            x: messages.value[index].x,
            y: messages.value[index].y
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
  if (confirm('确定要删除这条留言吗？')) {
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
  const colors = [
    '#FFE5E5', '#E5F3FF', '#F0E5FF', '#E5FFE5',
    '#FFF0E5', '#FFE5F0', '#E5FFF0', '#F0FFE5',
    '#FFE5CC', '#E5FFCC', '#CCE5FF', '#FFCCF0'
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
  flex-direction: column;
  align-items: center;
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 30px;
  width: 100%;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all var(--duration-normal) var(--ease-in-out);
  
  &:hover {
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
  }
}

.section-title {
  font-family: var(--font-heading);
  font-size: 1.3rem;
  color: white;
  margin: 0 0 30px 0;
  text-align: center;
  
  .section-emoji {
    margin-right: 8px;
    animation: bounce 2s ease-in-out infinite;
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

// 留言板样式
.message-board-section {
  max-width: 800px;
}

.message-input-area {
  margin-bottom: 30px;
}

.message-textarea {
  width: 100%;
  min-height: 100px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white;
  font-size: 0.9rem;
  resize: vertical;
  outline: none;
  margin-bottom: 16px;
  transition: all var(--duration-fast) var(--ease-in-out);
  
  &::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }
  
  &:focus {
    border-color: rgba(255, 182, 193, 0.5);
    background: rgba(255, 255, 255, 0.15);
  }
}

.input-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.send-message-btn {
  padding: 12px 20px;
  background: linear-gradient(135deg, var(--primary-start), var(--primary-end));
  border: none;
  border-radius: 20px;
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  transition: transform var(--duration-fast) var(--ease-in-out);
  
  &:hover:not(:disabled) {
    transform: scale(1.05);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.cancel-btn {
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }
}

.messages-container {
  position: relative;
  min-height: 300px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  overflow: hidden;
}

.message-note {
  position: absolute;
  max-width: 220px;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
  
  &:hover {
    transform: scale(1.05) !important;
    
    .message-actions {
      opacity: 1;
    }
  }
  
  &.editing {
    box-shadow: 0 0 0 2px rgba(255, 182, 193, 0.5);
    transform: scale(1.02) !important;
  }
  
  .message-content {
    font-size: 0.9rem;
    color: #333;
    margin-bottom: 8px;
    word-wrap: break-word;
    line-height: 1.4;
  }
  
  .message-time {
    font-size: 0.7rem;
    color: #666;
    text-align: right;
    margin-bottom: 8px;
  }
  
  .message-actions {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
    opacity: 0;
    transition: opacity var(--duration-fast) var(--ease-in-out);
    
    .edit-btn,
    .delete-btn {
      background: none;
      border: none;
      font-size: 0.8rem;
      cursor: pointer;
      padding: 4px;
      border-radius: 4px;
      transition: all var(--duration-fast) var(--ease-in-out);
      
      &:hover {
        background: rgba(0, 0, 0, 0.1);
      }
    }
    
    .delete-btn:hover {
      background: rgba(255, 0, 0, 0.1);
    }
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: rgba(255, 255, 255, 0.6);
  
  .empty-icon {
    font-size: 3rem;
    margin-bottom: 16px;
    opacity: 0.7;
  }
  
  .empty-text {
    font-size: 1rem;
    margin: 0;
    text-align: center;
  }
}

// 照片墙样式
.photo-gallery-section {
  max-width: 100%;
}

.photo-gallery-bg {
  position: relative;
  min-height: 300px;
  overflow: hidden;
  border-radius: 12px;
  background: transparent; // 改为透明背景
  padding: 20px;
}

.waterfall-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 15px;
  justify-content: center;
  align-content: start;
}

.waterfall-item {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    background: rgba(255, 255, 255, 0.15);
  }
}

.waterfall-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: scale(1.02);
  }
}

.photo-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: rgba(255, 255, 255, 0.6);
  
  .empty-icon {
    font-size: 3rem;
    margin-bottom: 16px;
    opacity: 0.7;
  }
  
  .empty-text {
    font-size: 1rem;
    margin: 0;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .interactive-container {
    padding: 16px;
    gap: 30px;
  }
  
  .glass-card {
    padding: 20px;
  }
  
  .waterfall-container {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 12px;
  }
  
  .message-note {
    max-width: 180px;
    
    .message-actions {
      opacity: 1;
    }
  }
  
  .input-buttons {
    flex-direction: column;
    
    .send-message-btn,
    .cancel-btn {
      width: 100%;
    }
  }
}

@media (max-width: 480px) {
  .waterfall-container {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 10px;
  }
  
  .message-note {
    max-width: 150px;
    font-size: 0.8rem;
  }
  
  .message-textarea {
    min-height: 80px;
  }
}

@media (min-width: 1024px) {
  .waterfall-container {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 18px;
  }
}
</style>