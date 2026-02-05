<template>
  <div class="login-container">
    <div class="login-card wafu-card">
      <div class="card-decoration">🌸</div>
      <h2 class="login-title text-heading">开启我们的故事</h2>
      
      <div class="login-form">
        <div class="input-group">
          <label class="input-label text-handwriting">请输入专属暗号</label>
          <input 
            v-model="password" 
            type="password" 
            class="secret-input" 
            placeholder="✨✨✨✨✨✨"
            @keyup.enter="handleLogin"
          />
        </div>
        
        <button class="login-btn btn-primary" @click="handleLogin" :disabled="loading">
          {{ loading ? '芝麻开门中...' : '芝麻开门' }}
        </button>
        
        <div class="divider text-handwriting">或者</div>
        
        <button class="guest-btn text-handwriting" @click="handleGuestLogin">
          我是朋友，来送祝福 🎁
        </button>
      </div>
    </div>
    
    <!-- 烟花特效容器 -->
    <div v-if="showFireworks" class="fireworks-container"></div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '~/composables/useApi'

const router = useRouter()
const { api } = useApi()

const password = ref('')
const loading = ref(false)
const showFireworks = ref(false)

async function handleLogin() {
  if (!password.value) return
  
  loading.value = true
  try {
    const res = await api.post('/api/login', { password: password.value })
    
    if (res.success) {
      // 登录成功
      localStorage.setItem('auth_token', res.token)
      localStorage.setItem('user_role', 'mutou')
      
      // 播放特效
      showFireworks.value = true
      setTimeout(() => {
        router.push('/')
      }, 2000)
    } else {
      alert('暗号不对哦，是不是走错门啦？')
    }
  } catch (error) {
    console.error(error)
    alert('服务器开小差了，请稍后再试')
  } finally {
    loading.value = false
  }
}

function handleGuestLogin() {
  localStorage.setItem('user_role', 'guest')
  router.push('/')
}
</script>

<style scoped lang="scss">
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-paper);
  background-image: 
    radial-gradient(#e6e6e6 1px, transparent 1px),
    radial-gradient(#e6e6e6 1px, transparent 1px);
  background-size: 20px 20px;
  background-position: 0 0, 10px 10px;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 40px 30px;
  text-align: center;
  position: relative;
  
  .card-decoration {
    position: absolute;
    top: -20px;
    right: -20px;
    font-size: 3rem;
    animation: float 3s ease-in-out infinite;
  }
}

.login-title {
  font-size: 2rem;
  color: var(--text-ink);
  margin-bottom: 40px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  text-align: left;
  
  .input-label {
    display: block;
    margin-bottom: 8px;
    color: var(--text-light);
    font-size: 1.1rem;
  }
}

.secret-input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1.2rem;
  text-align: center;
  outline: none;
  transition: all 0.3s ease;
  font-family: monospace;
  letter-spacing: 4px;
  
  &:focus {
    border-color: var(--primary-pink);
    box-shadow: 0 0 0 3px rgba(240, 145, 153, 0.2);
  }
}

.login-btn {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

.divider {
  position: relative;
  color: var(--text-light);
  font-size: 0.9rem;
  margin: 10px 0;
  
  &::before, &::after {
    content: '';
    position: absolute;
    top: 50%;
    width: 40%;
    height: 1px;
    background: #e0e0e0;
  }
  
  &::before { left: 0; }
  &::after { right: 0; }
}

.guest-btn {
  background: none;
  border: 2px dashed var(--text-light);
  color: var(--text-light);
  padding: 10px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: var(--primary-green);
    color: var(--primary-green);
    background: rgba(136, 176, 75, 0.1);
  }
}

.fireworks-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 999;
  background: rgba(255, 255, 255, 0.2);
  // 这里可以后续接入 canvas 烟花库
}
</style>
