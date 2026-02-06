<template>
  <div class="status-container">
    <div class="omamori-rack">
      <!-- 绳结装饰 -->
      <div class="rope-decoration"></div>
      
      <!-- 御守挂件区域 -->
      <div class="omamori-list">
        <!-- 木头的御守 -->
        <div class="omamori-wrapper animate-sway" style="animation-delay: 0s;">
          <div class="omamori-knot"></div>
          <div 
            class="omamori mutou" 
            :class="{ 'online': mutouStatus.isOnline, 'expanded': mutouExpanded }"
            @click="toggleMutouExpand"
          >
            <div class="omamori-top"></div>
            <div class="omamori-body">
              <div class="omamori-label text-heading">木头</div>
              <div class="omamori-avatar">
                <img :src="`/images/mutou_avatar.jpg?t=${timestamp}`" alt="木头" class="avatar-img" />
              </div>
              
              <!-- 默认显示状态名 -->
              <div class="omamori-status text-handwriting" v-if="!mutouExpanded">
                {{ mutouStatus.name || '获取中' }}
              </div>
              
              <!-- 展开显示详细信息 -->
              <div class="omamori-details" v-else>
                <div class="detail-status">{{ mutouStatus.name }}</div>
                <div class="detail-desc">{{ mutouStatus.description || '暂无描述' }}</div>
                <div class="detail-time">{{ formatLastUpdate(mutouStatus.last_update) }}</div>
              </div>
              
              <!-- 展开指示器 -->
              <div class="expand-indicator">{{ mutouExpanded ? '▲' : '▼' }}</div>
            </div>
          </div>
          <div class="omamori-tassel"></div>
        </div>

        <!-- 乾雨的御守 -->
        <div class="omamori-wrapper animate-sway" style="animation-delay: 1s;">
          <div class="omamori-knot"></div>
          <div 
            class="omamori qianyu" 
            :class="{ 'online': qianyuStatus.isOnline, 'expanded': qianyuExpanded }"
            @click="toggleQianyuExpand"
          >
            <div class="omamori-top"></div>
            <div class="omamori-body">
              <div class="omamori-label text-heading">乾雨</div>
              <div class="omamori-avatar">
                <img :src="`/images/qianyu_avatar.jpg?t=${timestamp}`" alt="乾雨" class="avatar-img" />
              </div>
              
              <div class="omamori-status text-handwriting" v-if="!qianyuExpanded">
                {{ qianyuStatus.name || '获取中' }}
              </div>
              
              <div class="omamori-details" v-else>
                <div class="detail-status">{{ qianyuStatus.name }}</div>
                <div class="detail-desc">{{ qianyuStatus.description || '暂无描述' }}</div>
                <div class="detail-time">{{ formatLastUpdate(qianyuStatus.last_update) }}</div>
              </div>
              
              <div class="expand-indicator">{{ qianyuExpanded ? '▲' : '▼' }}</div>
            </div>
          </div>
          <div class="omamori-tassel"></div>
        </div>
      </div>
      
      <!-- 抽签筒 -->
      <div v-if="userRole === 'mutou'" class="omikuji-container">
        <div 
          class="omikuji-box" 
          :class="{ 'shaking': isShaking, 'disabled': hasDrawnToday }" 
          @click="drawOmikuji"
        >
          <div class="omikuji-label text-heading">运势</div>
          <div class="omikuji-hole"></div>
          <!-- 掉出的签 -->
          <div class="omikuji-stick" :class="{ 'falling': isStickFalling }">
            <span class="stick-text">第{{ currentStickNum }}番</span>
          </div>
        </div>
        <p class="omikuji-hint text-handwriting">
          {{ hasDrawnToday ? '今日已签，明天再来吧~' : '点击签筒抽取今日运势' }}
        </p>
        
        <button class="history-btn text-handwriting" @click="fetchHistory">
          📜 抽签集锦
        </button>
      </div>
      
      <!-- 游客提示 -->
      <div v-else class="guest-hint-container">
        <div class="guest-hint-card">
          <div class="hint-icon">🔒</div>
          <div class="hint-text text-handwriting">
            恋爱神社仅对专属人员开放哦~
          </div>
          <div class="hint-sub text-handwriting">
            (快去叫木头来抽签吧！)
          </div>
        </div>
      </div>
      
      <!-- 签文弹窗 -->
      <Transition name="fade">
        <div v-if="showResult" class="omikuji-result-overlay" @click="closeResult">
          <div class="omikuji-paper" @click.stop>
            <div class="paper-header">
              <div class="shrine-name text-heading">恋爱神社</div>
              <div class="omikuji-rank text-heading">{{ currentResult.result?.rank }}</div>
            </div>
            
            <div class="paper-body text-handwriting">
              <!-- 星座与天气 -->
              <div class="daily-info">
                <div class="info-tag">
                  <span class="icon">🌌</span> {{ currentResult.constellation?.name }}
                </div>
                <div class="info-tag">
                  <span class="icon">{{ currentResult.weather?.weather?.split(' ')[0] }}</span> 
                  {{ currentResult.weather?.temp }}
                </div>
              </div>
              <div class="weather-tip">{{ currentResult.weather?.tip }}</div>

              <div class="omikuji-poem vertical-text">
                {{ currentResult.result?.poem }}
              </div>
              
              <div class="omikuji-items">
                <div class="item">
                  <span class="label">愿望：</span>
                  <span class="value">{{ currentResult.result?.wish }}</span>
                </div>
                <div class="item">
                  <span class="label">待人：</span>
                  <span class="value">{{ currentResult.result?.person }}</span>
                </div>
                <div class="item">
                  <span class="label">恋爱：</span>
                  <span class="value">{{ currentResult.result?.love }}</span>
                </div>
              </div>
              
              <!-- 彩蛋奖品 -->
              <div v-if="currentResult.result?.prize" class="special-prize">
                <div class="prize-title">✨ 获得彩头 ✨</div>
                <div class="prize-content">{{ currentResult.result.prize }}</div>
                <div class="prize-note">截图此券向乾雨兑换</div>
              </div>
            </div>
            
            <button class="close-btn" @click="closeResult">收入囊中</button>
          </div>
        </div>
      </Transition>

      <!-- 历史记录弹窗 -->
      <Transition name="fade">
        <div v-if="showHistoryModal" class="history-overlay" @click="showHistoryModal = false">
          <div class="history-panel" @click.stop>
            <h3 class="history-title text-heading">抽签集锦</h3>
            <div class="history-list">
              <div v-for="record in historyList" :key="record.id" class="history-item">
                <div class="history-date">{{ record.date }}</div>
                <div class="history-rank" :class="getRankClass(record.result.rank)">
                  {{ record.result.rank }}
                </div>
                <div class="history-prize" v-if="record.result.prize">🎁</div>
              </div>
            </div>
            <button class="close-btn small" @click="showHistoryModal = false">关闭</button>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'

// 状态管理
const { api } = useApi()
const mutouStatus = ref({})
const qianyuStatus = ref({})
const mutouExpanded = ref(false)
const qianyuExpanded = ref(false)
const userRole = ref('guest') // 'guest' or 'mutou'
const timestamp = ref(Date.now())

// 抽签相关
const isShaking = ref(false)
const isStickFalling = ref(false)
const showResult = ref(false)
const hasDrawnToday = ref(false)
const currentStickNum = ref(1)
const currentResult = ref({})
const showHistoryModal = ref(false)
const historyList = ref([])

// 状态配置
const statusConfig = {
  1: { name: '安睡', description: '正在梦里抓蝴蝶...' },
  2: { name: '勤勉', description: '为了买猫粮努力工作中' },
  3: { name: '锻炼', description: '燃烧卡路里！' },
  4: { name: '摸鱼', description: '刷B站中，勿扰~' },
  5: { name: '游戏', description: '在海拉鲁大陆探险' },
  6: { name: '听歌', description: '陶醉在音乐世界' },
  7: { name: '学习', description: '好好学习，天天向上' },
  8: { name: '烹饪', description: '正在制作黑暗料理' }
}

onMounted(() => {
  if (process.client) {
    userRole.value = localStorage.getItem('user_role') || 'guest'
  }
  
  fetchCurrentStatus()
  if (userRole.value === 'mutou') {
    checkTodayOmikuji()
  }
  setInterval(fetchCurrentStatus, 30000)
})

async function fetchCurrentStatus() {
  try {
    const res = await api.get('/api/status/latest')
    if (res.success) {
      mutouStatus.value = res.data.mutou
      qianyuStatus.value = res.data.qianyu
    } else {
       // Fallback mock
       mutouStatus.value = { isOnline: true, name: '连接中', description: '正在连接大脑...' }
       qianyuStatus.value = { isOnline: false, name: '离线', description: '信号丢失...' }
    }
  } catch (e) {
    console.error('Status fetch failed', e)
  }
}

async function checkTodayOmikuji() {
  try {
    const data = await api.get('/api/omikuji/today')
    if (data.has_drawn) {
      hasDrawnToday.value = true
      currentResult.value = data.record
    }
  } catch (e) {
    console.error(e)
  }
}

async function drawOmikuji() {
  if (userRole.value !== 'mutou') {
    alert('只有木头才能抽签哦~')
    return
  }

  if (isShaking.value || hasDrawnToday.value) {
    if (hasDrawnToday.value) {
      showResult.value = true
    }
    return
  }
  
  isShaking.value = true
  
  setTimeout(() => {
    isShaking.value = false
    isStickFalling.value = true
    currentStickNum.value = Math.floor(Math.random() * 99) + 1
    
    api.post('/api/omikuji/draw').then(res => {
      if (res.success) {
        currentResult.value = res.data
        hasDrawnToday.value = true
        
        setTimeout(() => {
          showResult.value = true
          isStickFalling.value = false
        }, 1000)
      }
    }).catch(err => {
      isStickFalling.value = false
      alert(err.message || '抽签失败，请稍后再试')
    })
    
  }, 1500)
}

async function fetchHistory() {
  try {
    const res = await api.get('/api/omikuji/history?user=木头')
    if (res.success) {
      historyList.value = res.history
      showHistoryModal.value = true
    }
  } catch (e) {
    console.error(e)
  }
}

function toggleMutouExpand() {
  mutouExpanded.value = !mutouExpanded.value
  if (mutouExpanded.value) qianyuExpanded.value = false
}

function toggleQianyuExpand() {
  qianyuExpanded.value = !qianyuExpanded.value
  if (qianyuExpanded.value) mutouExpanded.value = false
}

function formatLastUpdate(time) {
  if (!time) return ''
  const date = new Date(time)
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')} 更新`
}

function closeResult() {
  showResult.value = false
}

function getRankClass(rank) {
  if (rank.includes('大吉')) return 'rank-best'
  if (rank.includes('吉')) return 'rank-good'
  return 'rank-normal'
}
</script>

<style scoped lang="scss">
.status-container {
  padding: 40px 20px;
  display: flex;
  justify-content: center;
}

.omamori-rack {
  position: relative;
  width: 100%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rope-decoration {
  position: absolute;
  top: -20px;
  left: 0;
  width: 100%;
  height: 4px;
  background: #8B4513;
  border-radius: 2px;
  
  &::before, &::after {
    content: '';
    position: absolute;
    top: -5px;
    width: 14px;
    height: 14px;
    background: #8B4513;
    border-radius: 50%;
  }
  
  &::before { left: 0; }
  &::after { right: 0; }
}

.omamori-list {
  display: flex;
  gap: 40px;
  margin-bottom: 50px;
  align-items: flex-start;
  min-height: 250px;
}

.omamori-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  transform-origin: top center;
  z-index: 2;
}

.omamori-knot {
  width: 4px;
  height: 40px;
  background: #CB4042;
  margin-bottom: -5px;
  position: relative;
  z-index: 2;
  
  &::before {
    content: '';
    position: absolute;
    top: 20px;
    left: -8px;
    width: 20px;
    height: 10px;
    border: 2px solid #CB4042;
    border-radius: 10px;
  }
}

.omamori {
  width: 100px;
  height: 160px;
  position: relative;
  filter: drop-shadow(0 5px 15px rgba(0,0,0,0.2));
  transition: all 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
  cursor: pointer;
  
  &:hover {
    transform: scale(1.05);
  }
  
  &.expanded {
    height: 240px;
    width: 140px;
    transform: translateY(20px);
    z-index: 10;
    
    .omamori-body {
      width: 140px;
      height: 200px;
    }
    
    .omamori-top {
      border-left-width: 70px;
      border-right-width: 70px;
    }
    
    .omamori-avatar {
      width: 80px;
      height: 80px;
      margin-bottom: 10px;
    }
  }
  
  &.mutou {
    .omamori-body { background: var(--accent-blue); }
    .omamori-top { border-bottom-color: var(--accent-blue); }
  }
  
  &.qianyu {
    .omamori-body { background: var(--primary-pink); }
    .omamori-top { border-bottom-color: var(--primary-pink); }
  }
  
  &.online {
    filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.6));
  }
}

.omamori-top {
  width: 0;
  height: 0;
  border-left: 50px solid transparent;
  border-right: 50px solid transparent;
  border-bottom: 40px solid #ccc;
  position: absolute;
  top: 0;
  transition: all 0.5s ease;
}

.omamori-body {
  width: 100px;
  height: 120px;
  background: #ccc;
  position: absolute;
  top: 40px;
  border-radius: 0 0 10px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  color: white;
  transition: all 0.5s ease;
  overflow: hidden;
  
  background-image: repeating-linear-gradient(
    45deg,
    rgba(255,255,255,0.1),
    rgba(255,255,255,0.1) 10px,
    transparent 10px,
    transparent 20px
  );
}

.omamori-label {
  background: white;
  color: var(--text-ink);
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 1rem;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  flex-shrink: 0;
}

.omamori-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 5px;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  transition: all 0.5s ease;
  flex-shrink: 0;
  
  .avatar-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.omamori-status {
  font-size: 1.2rem;
  font-weight: bold;
}

.omamori-details {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  animation: fadeIn 0.5s ease;
  
  .detail-status {
    font-size: 1.4rem;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .detail-desc {
    font-size: 0.9rem;
    text-align: center;
    opacity: 0.9;
    margin-bottom: 10px;
    line-height: 1.2;
  }
  
  .detail-time {
    font-size: 0.8rem;
    opacity: 0.7;
    margin-top: auto;
  }
}

.expand-indicator {
  margin-top: auto;
  font-size: 0.8rem;
  opacity: 0.6;
}

.omamori-tassel {
  width: 6px;
  height: 40px;
  background: #CB4042;
  margin-top: -5px;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: -7px;
    width: 20px;
    height: 20px;
    background: #CB4042;
    border-radius: 50% 50% 0 0;
    clip-path: polygon(0 0, 100% 0, 80% 100%, 20% 100%);
  }
}

// 抽签筒样式
.omikuji-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.omikuji-box {
  width: 100px;
  height: 140px;
  background: #8B4513; // 木质颜色
  border-radius: 5px;
  position: relative;
  display: flex;
  justify-content: center;
  cursor: pointer;
  box-shadow: inset 5px 0 10px rgba(0,0,0,0.3), 5px 5px 15px rgba(0,0,0,0.2);
  
  // 木纹
  background-image: repeating-linear-gradient(90deg, rgba(255,255,255,0.05) 0px, rgba(255,255,255,0.05) 2px, transparent 2px, transparent 10px);
  
  &.shaking {
    animation: shake 0.5s ease-in-out infinite;
  }
  
  &.disabled {
    opacity: 0.8;
    cursor: default;
  }
}

.omikuji-label {
  position: absolute;
  top: 40px;
  background: white;
  padding: 5px 15px;
  writing-mode: vertical-rl;
  border: 1px solid #333;
  font-size: 1.2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.omikuji-hole {
  position: absolute;
  top: 0;
  width: 80%;
  height: 10px;
  background: #3e1f08;
  border-radius: 0 0 10px 10px;
}

.omikuji-stick {
  position: absolute;
  top: 0;
  width: 10px;
  height: 80px;
  background: #f5deb3;
  z-index: -1;
  transition: transform 0.5s ease;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  padding-bottom: 5px;
  border: 1px solid #d2b48c;
  
  .stick-text {
    font-size: 0.6rem;
    writing-mode: vertical-rl;
    color: #8B4513;
  }
  
  &.falling {
    animation: stickFall 1s ease-out forwards;
    z-index: 1;
  }
}

.omikuji-hint {
  margin-top: 10px;
  color: var(--text-light);
  font-size: 0.9rem;
}

.history-btn {
  margin-top: 10px;
  background: transparent;
  border: 1px dashed var(--text-light);
  padding: 5px 15px;
  border-radius: 15px;
  color: var(--text-light);
  cursor: pointer;
  font-size: 0.9rem;
  
  &:hover {
    background: rgba(0,0,0,0.05);
  }
}

// 签文弹窗
.omikuji-result-overlay, .history-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.6);
  z-index: 100;
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(5px);
}

.omikuji-paper {
  width: 300px;
  background: #fffdf5;
  padding: 30px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  // 纸张纹理
  &::before {
    content: '';
    position: absolute;
    top: 5px;
    left: 5px;
    right: 5px;
    bottom: 5px;
    border: 2px double #CB4042;
    pointer-events: none;
  }
}

.daily-info {
  display: flex;
  gap: 10px;
  margin-top: 10px;
  
  .info-tag {
    background: rgba(165, 154, 202, 0.1);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.9rem;
    color: var(--accent-purple);
  }
}

.weather-tip {
  font-size: 0.8rem;
  color: var(--text-light);
  margin-top: 5px;
  text-align: center;
}

.paper-header {
  text-align: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #CB4042;
  padding-bottom: 10px;
  width: 100%;
}

.shrine-name {
  font-size: 1rem;
  color: var(--text-light);
  margin-bottom: 5px;
}

.omikuji-rank {
  font-size: 2.5rem;
  color: #CB4042;
  font-weight: bold;
}

.paper-body {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.omikuji-poem {
  font-size: 1.2rem;
  margin: 20px 0;
  line-height: 1.8;
  color: var(--text-ink);
  font-weight: bold;
}

.vertical-text {
  writing-mode: vertical-rl;
  text-orientation: upright;
  max-height: 200px;
}

.omikuji-items {
  width: 100%;
  margin-top: 20px;
  
  .item {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px dashed #ccc;
    padding: 8px 0;
    
    .label { color: var(--text-light); }
    .value { font-weight: bold; color: var(--text-ink); }
  }
}

.special-prize {
  margin-top: 20px;
  background: rgba(255, 215, 0, 0.1);
  border: 1px solid gold;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  width: 100%;
  
  .prize-title { color: #d4af37; font-weight: bold; margin-bottom: 5px; }
  .prize-content { font-size: 1.2rem; font-weight: bold; color: var(--text-ink); }
  .prize-note { font-size: 0.8rem; color: var(--text-light); margin-top: 5px; }
}

.history-panel {
  background: white;
  width: 320px;
  max-height: 500px;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  
  .history-title {
    text-align: center;
    margin-bottom: 15px;
  }
  
  .history-list {
    flex: 1;
    overflow-y: auto;
    border-top: 1px solid #eee;
    
    .history-item {
      display: flex;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid #eee;
      
      .history-date { color: #666; }
      .history-rank { font-weight: bold; }
      .rank-best { color: #CB4042; }
      .rank-good { color: #FF9800; }
    }
  }
}

.close-btn {
  margin-top: 20px;
  background: #CB4042;
  color: white;
  border: none;
  padding: 10px 30px;
  border-radius: 20px;
  cursor: pointer;
  font-family: var(--font-heading);
  transition: background 0.3s;
  
  &:hover { background: #a0282a; }
  
  &.small {
    margin-top: 10px;
    padding: 5px 20px;
    font-size: 0.9rem;
    background: #999;
  }
}

// 动画
@keyframes shake {
  0% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  50% { transform: rotate(0deg); }
  75% { transform: rotate(10deg); }
  100% { transform: rotate(0deg); }
}

@keyframes stickFall {
  0% { transform: translateY(0); opacity: 0; }
  100% { transform: translateY(-120px) rotate(20deg); opacity: 1; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.guest-hint-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.guest-hint-card {
  background: rgba(255, 255, 255, 0.8);
  padding: 20px 30px;
  border-radius: 12px;
  border: 2px dashed #e0e0e0;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  
  .hint-icon {
    font-size: 2rem;
  }
  
  .hint-text {
    font-size: 1.1rem;
    color: var(--text-ink);
    font-weight: bold;
  }
  
  .hint-sub {
    font-size: 0.9rem;
    color: var(--text-light);
  }
}
</style>
