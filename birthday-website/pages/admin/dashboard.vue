<template>
  <div class="dashboard-container">
    <div class="card control-panel">
      <h1 class="title text-heading">🎮 状态控制台</h1>
      
      <!-- 身份验证 -->
      <div v-if="!isAuthenticated" class="auth-box">
        <p class="hint text-handwriting">请输入控制密钥</p>
        <input 
          v-model="secretInput" 
          type="password" 
          class="secret-input" 
          placeholder="Secret Key"
        />
        <button class="btn-primary" @click="verifySecret">解锁</button>
      </div>

      <!-- 控制面板 -->
      <div v-else class="panel-content">
        <div class="user-switch">
          <label 
            class="user-option" 
            :class="{ active: selectedUser === 'mutou' }"
            @click="selectedUser = 'mutou'"
          >
            🧔🏻‍♂️ 木头
          </label>
          <label 
            class="user-option" 
            :class="{ active: selectedUser === 'qianyu' }"
            @click="selectedUser = 'qianyu'"
          >
            👧🏻 乾雨
          </label>
        </div>

        <div class="quick-actions">
          <button 
            v-for="status in quickStatuses" 
            :key="status.name"
            class="action-btn"
            @click="updateStatus(status.name, status.desc)"
          >
            <span class="emoji">{{ status.emoji }}</span>
            <span class="name">{{ status.name }}</span>
          </button>
        </div>

        <div class="custom-status">
          <h3 class="subtitle text-handwriting">自定义状态</h3>
          <input v-model="customName" placeholder="状态名称 (如: 发呆)" class="input-field" />
          <input v-model="customDesc" placeholder="状态描述 (如: 思考人生中...)" class="input-field" />
          <button class="btn-secondary" @click="updateCustom">更新自定义</button>
        </div>

        <div class="status-log" v-if="lastUpdate">
          ✅ 上次更新: {{ lastUpdate }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

const { api } = useApi()

const isAuthenticated = ref(false)
const secretInput = ref('')
const selectedUser = ref('mutou')
const customName = ref('')
const customDesc = ref('')
const lastUpdate = ref('')

const quickStatuses = [
  { name: '勤勉', desc: '为了买猫粮努力工作中', emoji: '👨🏻‍💻' },
  { name: '摸鱼', desc: '刷B站中，勿扰~', emoji: '🐟' },
  { name: '游戏', desc: '在海拉鲁大陆探险', emoji: '🎮' },
  { name: '安睡', desc: '呼呼大睡中...', emoji: '💤' },
  { name: '吃饭', desc: '正在干饭！', emoji: '🍚' },
  { name: '想你', desc: '正在想念对方...', emoji: '💗' },
  { name: '外出', desc: '不在电脑前哦', emoji: '🚶🏻' },
  { name: '洗澡', desc: '洗香香中', emoji: '🚿' }
]

onMounted(() => {
  const savedSecret = localStorage.getItem('admin_secret')
  if (savedSecret === 'my_love_secret_2024') {
    isAuthenticated.value = true
  }
})

function verifySecret() {
  if (secretInput.value === 'my_love_secret_2024') {
    isAuthenticated.value = true
    localStorage.setItem('admin_secret', 'my_love_secret_2024')
  } else {
    alert('密钥错误！')
  }
}

async function updateStatus(name, description) {
  try {
    const res = await api.post('/api/status/update', {
      secret: 'my_love_secret_2024',
      user_key: selectedUser.value,
      name,
      description,
      is_online: true
    })
    
    if (res.success) {
      lastUpdate.value = `${name} (${new Date().toLocaleTimeString()})`
      // 轻微震动反馈 (手机端)
      if (navigator.vibrate) navigator.vibrate(50)
    } else {
      alert('更新失败: ' + res.message)
    }
  } catch (e) {
    alert('网络错误')
    console.error(e)
  }
}

function updateCustom() {
  if (!customName.value) return
  updateStatus(customName.value, customDesc.value)
}
</script>

<style scoped lang="scss">
.dashboard-container {
  min-height: 100vh;
  padding: 20px;
  background: #f5f5f5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  background: white;
  width: 100%;
  max-width: 400px;
  border-radius: 20px;
  padding: 30px 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.auth-box {
  display: flex;
  flex-direction: column;
  gap: 15px;
  
  .secret-input {
    padding: 12px;
    border: 2px solid #eee;
    border-radius: 8px;
    font-size: 1.1rem;
    text-align: center;
  }
}

.user-switch {
  display: flex;
  background: #eee;
  padding: 5px;
  border-radius: 12px;
  margin-bottom: 25px;
  
  .user-option {
    flex: 1;
    text-align: center;
    padding: 10px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    color: #666;
    transition: all 0.3s;
    
    &.active {
      background: white;
      color: var(--primary-pink);
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
  }
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 30px;
  
  .action-btn {
    background: white;
    border: 2px solid #eee;
    padding: 15px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    cursor: pointer;
    transition: all 0.2s;
    
    &:active {
      transform: scale(0.95);
      background: #f9f9f9;
    }
    
    .emoji { font-size: 1.5rem; }
    .name { font-weight: bold; color: #444; }
  }
}

.custom-status {
  border-top: 1px solid #eee;
  padding-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  
  .input-field {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
}

.btn-primary {
  background: var(--primary-pink);
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.btn-secondary {
  background: #666;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
}

.status-log {
  margin-top: 20px;
  text-align: center;
  color: #4CAF50;
  font-size: 0.9rem;
  font-weight: bold;
}
</style>
