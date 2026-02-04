<template>
  <div class="birthday-modal" v-if="showModal">
    <!-- 全屏烟花背景 -->
    <div class="fireworks-container" ref="fireworksRef" />
    
    <!-- 3D 生日蛋糕 -->
    <div class="cake-container" ref="cakeRef" />
    
    <!-- 生日祝福内容 -->
    <div class="birthday-content">
      <!-- 主标题 -->
      <div class="birthday-title">
        <h1 class="main-greeting">{{ currentGreeting }}</h1>
        <div class="subtitle">{{ currentSubtitle }}</div>
      </div>
      
      <!-- 年龄显示 -->
      <div class="age-display">
        <div class="age-number">{{ currentAge }}</div>
        <div class="age-label">岁生日快乐！</div>
      </div>
      
      <!-- 生日祝福轮播 -->
      <div class="wishes-carousel">
        <div class="wish-text">{{ currentWish }}</div>
      </div>
      
      <!-- 互动按钮 -->
      <div class="birthday-actions">
        <button @click="triggerFireworks" class="action-btn fireworks-btn">
          🎆 放烟花
        </button>
        <button @click="playBirthdayMusic" class="action-btn music-btn">
          🎵 {{ isPlaying ? '暂停' : '播放' }}生日歌
        </button>
        <button @click="showGiftBox = true" class="action-btn gift-btn">
          🎁 打开礼物
        </button>
      </div>
      
      <!-- 关闭按钮 -->
      <button @click="closeModal" class="close-btn">
        ✕
      </button>
    </div>
    
    <!-- 礼物盒子模态框 -->
    <div v-if="showGiftBox" class="gift-modal">
      <div class="gift-content">
        <div class="gift-box" @click="openGift">
          <div class="gift-emoji">🎁</div>
          <div class="gift-text">点击打开礼物</div>
        </div>
        
        <div v-if="giftOpened" class="gift-surprise">
          <div class="surprise-emoji">💝</div>
          <h3 class="surprise-title">专属于你的生日网站！</h3>
          <p class="surprise-message">
            这个网站是我为你精心制作的生日礼物～<br>
            里面记录了我们的美好时光，<br>
            希望你喜欢！💕
          </p>
        </div>
        
        <button @click="showGiftBox = false" class="close-gift-btn">
          关闭
        </button>
      </div>
    </div>
    
    <!-- 音频元素 -->
    <audio ref="birthdayAudioRef" loop style="display: none;">
      <source src="/audio/happy-birthday.mp3" type="audio/mpeg">
      <source src="/audio/happy-birthday.ogg" type="audio/ogg">
    </audio>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { gsap } from 'gsap'

// Props
const props = defineProps({
  birthdayPerson: {
    type: String,
    default: '木头'
  },
  age: {
    type: Number,
    default: 22
  }
})

// 响应式状态
const showModal = ref(true)
const showGiftBox = ref(false)
const giftOpened = ref(false)
const isPlaying = ref(false)
const currentGreetingIndex = ref(0)
const currentWishIndex = ref(0)
const fireworksAnimation = ref(null)
const textAnimation = ref(null)

// 引用
const fireworksRef = ref(null)
const cakeRef = ref(null)
const birthdayAudioRef = ref(null)

// 生日祝福语
const greetings = [
  '木头破壳日快乐！',
  '生日快乐，木头！',
  '愿木头永远快乐！',
  '木头的特别日子！'
]

const subtitles = [
  '今天是属于你的特别日子',
  '愿你的每一天都充满阳光',
  '感谢你来到我的生命中',
  '让我们一起庆祝这美好的一天'
]

const wishes = [
  '愿你的笑容永远灿烂如花 🌸',
  '愿你的梦想都能成真 ✨',
  '愿你被世界温柔以待 💕',
  '愿你的人生充满惊喜 🎉',
  '愿你永远年轻，永远热泪盈眶 🥰',
  '愿你拥有最美好的一切 💝'
]

// 计算属性
const currentGreeting = computed(() => greetings[currentGreetingIndex.value])
const currentSubtitle = computed(() => subtitles[currentGreetingIndex.value])
const currentWish = computed(() => wishes[currentWishIndex.value])
const currentAge = computed(() => props.age)

// 生命周期
onMounted(() => {
  initBirthdayEffects()
  startTextCarousel()
  startFireworksAnimation()
})

onUnmounted(() => {
  cleanup()
})

// 方法
function initBirthdayEffects() {
  // 初始化动画
  gsap.fromTo('.birthday-title', 
    { opacity: 0, y: 50 },
    { opacity: 1, y: 0, duration: 1, ease: "power2.out" }
  )
  
  gsap.fromTo('.age-display', 
    { opacity: 0, scale: 0.5 },
    { opacity: 1, scale: 1, duration: 1, delay: 0.5, ease: "back.out(1.7)" }
  )
  
  gsap.fromTo('.wishes-carousel', 
    { opacity: 0, y: 30 },
    { opacity: 1, y: 0, duration: 1, delay: 1, ease: "power2.out" }
  )
  
  gsap.fromTo('.birthday-actions', 
    { opacity: 0, y: 30 },
    { opacity: 1, y: 0, duration: 1, delay: 1.5, ease: "power2.out" }
  )
}

function startTextCarousel() {
  // 祝福语轮播
  setInterval(() => {
    currentGreetingIndex.value = (currentGreetingIndex.value + 1) % greetings.length
  }, 4000)
  
  // 祝福轮播
  setInterval(() => {
    currentWishIndex.value = (currentWishIndex.value + 1) % wishes.length
  }, 3000)
}

function startFireworksAnimation() {
  if (!fireworksRef.value) return
  
  // 创建烟花粒子
  createFireworks()
  
  // 定期创建新的烟花
  fireworksAnimation.value = setInterval(() => {
    createFireworks()
  }, 2000)
}

function createFireworks() {
  const container = fireworksRef.value
  if (!container) {
    console.log('烟花容器不存在')
    return
  }
  
  console.log('正在创建烟花效果...')
  
  // 创建烟花爆炸点
  const firework = document.createElement('div')
  firework.className = 'firework'
  
  // 随机位置
  const x = Math.random() * window.innerWidth
  const y = Math.random() * window.innerHeight * 0.6 + 100
  
  firework.style.left = `${x}px`
  firework.style.top = `${y}px`
  
  container.appendChild(firework)
  
  // 创建中心光晕
  const glow = document.createElement('div')
  glow.className = 'firework-glow'
  glow.style.left = `${x}px`
  glow.style.top = `${y}px`
  container.appendChild(glow)
  
  // 光晕动画
  gsap.fromTo(glow, 
    { scale: 0, opacity: 1 },
    { scale: 3, opacity: 0, duration: 1.5, ease: "power2.out" }
  )
  
  // 创建粒子
  const colors = ['#FF6B6B', '#FFB6C1', '#E6E6FA', '#B76E79', '#FF69B4', '#FFD700', '#FFA500', '#FF4500', '#DA70D6', '#98FB98', '#00BFFF', '#FF1493', '#00FF00', '#FF8C00']
  const particleCount = 40
  
  console.log(`创建 ${particleCount} 个烟花粒子在位置 (${x}, ${y})`)
  
  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div')
    particle.className = 'firework-particle'
    
    const color = colors[Math.floor(Math.random() * colors.length)]
    particle.style.backgroundColor = color
    particle.style.boxShadow = `0 0 20px ${color}, 0 0 40px ${color}`
    
    const angle = (Math.PI * 2 * i) / particleCount
    const velocity = Math.random() * 200 + 100
    const gravity = Math.random() * 0.8 + 0.4
    
    const endX = Math.cos(angle) * velocity
    const endY = Math.sin(angle) * velocity + gravity * 150
    
    particle.style.left = `${x}px`
    particle.style.top = `${y}px`
    particle.style.zIndex = '9999'
    
    container.appendChild(particle)
    
    // 主粒子动画
    gsap.fromTo(particle, 
      { scale: 0.5, opacity: 1 },
      {
        x: endX,
        y: endY,
        opacity: 0,
        scale: 0.2,
        duration: 2.5 + Math.random(),
        ease: "power2.out",
        onComplete: () => {
          if (particle.parentNode) {
            particle.parentNode.removeChild(particle)
          }
        }
      }
    )
    
    // 创建拖尾粒子
    if (Math.random() < 0.5) {
      setTimeout(() => {
        const trail = document.createElement('div')
        trail.className = 'firework-trail'
        trail.style.backgroundColor = color
        trail.style.boxShadow = `0 0 10px ${color}`
        trail.style.left = `${x + endX * 0.6}px`
        trail.style.top = `${y + endY * 0.6}px`
        trail.style.zIndex = '9999'
        container.appendChild(trail)
        
        gsap.to(trail, {
          opacity: 0,
          scale: 0.3,
          duration: 0.8,
          onComplete: () => {
            if (trail.parentNode) {
              trail.parentNode.removeChild(trail)
            }
          }
        })
      }, 800)
    }
  }
  
  // 创建星星效果
  for (let i = 0; i < 8; i++) {
    const star = document.createElement('div')
    star.className = 'firework-star'
    const starEmojis = ['✨', '⭐', '💫', '🌟', '✨']
    star.innerHTML = starEmojis[Math.floor(Math.random() * starEmojis.length)]
    
    const starX = x + (Math.random() - 0.5) * 300
    const starY = y + (Math.random() - 0.5) * 300
    
    star.style.left = `${starX}px`
    star.style.top = `${starY}px`
    star.style.zIndex = '9999'
    
    container.appendChild(star)
    
    gsap.fromTo(star, 
      { scale: 0, opacity: 1, rotation: 0 },
      { scale: 2, opacity: 0, rotation: 720, duration: 3, ease: "power2.out", onComplete: () => {
        if (star.parentNode) {
          star.parentNode.removeChild(star)
        }
      }}
    )
  }
  
  // 清理烟花元素
  setTimeout(() => {
    if (firework.parentNode) {
      firework.parentNode.removeChild(firework)
    }
    if (glow.parentNode) {
      glow.parentNode.removeChild(glow)
    }
  }, 3000)
}

function triggerFireworks() {
  console.log('点击了烟花按钮！')
  
  // 播放烟花音效
  playFireworkSound()
  
  // 创建迪士尼风格的壮观烟花秀
  createDisneyStyleFireworks()
}

function createDisneyStyleFireworks() {
  console.log('创建迪士尼风格烟花秀')
  
  // 第一波：大面积覆盖整个屏幕的烟花
  const screenPositions = [
    { x: window.innerWidth * 0.2, y: window.innerHeight * 0.3 },
    { x: window.innerWidth * 0.8, y: window.innerHeight * 0.3 },
    { x: window.innerWidth * 0.1, y: window.innerHeight * 0.5 },
    { x: window.innerWidth * 0.5, y: window.innerHeight * 0.2 },
    { x: window.innerWidth * 0.9, y: window.innerHeight * 0.5 },
    { x: window.innerWidth * 0.3, y: window.innerHeight * 0.6 },
    { x: window.innerWidth * 0.7, y: window.innerHeight * 0.6 },
    { x: window.innerWidth * 0.5, y: window.innerHeight * 0.7 },
  ]
  
  // 第一波同时爆炸
  screenPositions.forEach((pos, index) => {
    setTimeout(() => {
      createMassiveFirework(pos.x, pos.y)
      playFireworkSound()
    }, index * 100)
  })
  
  // 第二波：更密集的烟花
  setTimeout(() => {
    for (let i = 0; i < 15; i++) {
      setTimeout(() => {
        const x = Math.random() * window.innerWidth
        const y = Math.random() * window.innerHeight * 0.8 + 50
        createMassiveFirework(x, y)
        
        if (Math.random() < 0.3) {
          playFireworkSound()
        }
      }, i * 150)
    }
  }, 1000)
  
  // 第三波：最终高潮
  setTimeout(() => {
    for (let i = 0; i < 20; i++) {
      setTimeout(() => {
        const x = Math.random() * window.innerWidth
        const y = Math.random() * window.innerHeight * 0.7 + 50
        createMassiveFirework(x, y)
        createMassiveFirework(x + (Math.random() - 0.5) * 200, y + (Math.random() - 0.5) * 200)
        
        if (Math.random() < 0.4) {
          playFireworkSound()
        }
      }, i * 100)
    }
  }, 3000)
}

function createMassiveFirework(x, y) {
  const container = fireworksRef.value
  if (!container) return
  
  console.log(`创建大型烟花在位置 (${x}, ${y})`)
  
  // 创建中心爆炸点
  const center = document.createElement('div')
  center.className = 'massive-firework-center'
  center.style.left = `${x}px`
  center.style.top = `${y}px`
  container.appendChild(center)
  
  // 中心爆炸效果
  gsap.fromTo(center, 
    { scale: 0.2, opacity: 1 },
    { scale: 4, opacity: 0, duration: 1.5, ease: "power2.out" }
  )
  
  // 创建大量粒子
  const colors = ['#FF6B6B', '#FFD700', '#FF69B4', '#00BFFF', '#98FB98', '#FF4500', '#DA70D6', '#FFA500', '#FF1493', '#00FF00', '#FF8C00', '#E6E6FA']
  const particleCount = 80 // 大幅增加粒子数量
  
  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div')
    particle.className = 'massive-firework-particle'
    
    const color = colors[Math.floor(Math.random() * colors.length)]
    particle.style.backgroundColor = color
    particle.style.boxShadow = `0 0 30px ${color}, 0 0 60px ${color}`
    
    const angle = (Math.PI * 2 * i) / particleCount
    const velocity = Math.random() * 400 + 200 // 大幅增加速度
    const gravity = Math.random() * 1.2 + 0.8
    
    const endX = Math.cos(angle) * velocity
    const endY = Math.sin(angle) * velocity + gravity * 300
    
    particle.style.left = `${x}px`
    particle.style.top = `${y}px`
    particle.style.zIndex = '9999'
    
    container.appendChild(particle)
    
    // 粒子动画
    gsap.fromTo(particle, 
      { scale: 0.8, opacity: 1 },
      {
        x: endX,
        y: endY,
        opacity: 0,
        scale: 0.1,
        duration: 3 + Math.random() * 2,
        ease: "power2.out",
        onComplete: () => {
          if (particle.parentNode) {
            particle.parentNode.removeChild(particle)
          }
        }
      }
    )
  }
  
  // 创建环形扩散效果
  for (let ring = 0; ring < 3; ring++) {
    setTimeout(() => {
      const ringElement = document.createElement('div')
      ringElement.className = 'firework-ring'
      ringElement.style.left = `${x}px`
      ringElement.style.top = `${y}px`
      container.appendChild(ringElement)
      
      gsap.fromTo(ringElement, 
        { scale: 0, opacity: 0.8 },
        { scale: 5 + ring * 2, opacity: 0, duration: 2, ease: "power2.out", onComplete: () => {
          if (ringElement.parentNode) {
            ringElement.parentNode.removeChild(ringElement)
          }
        }}
      )
    }, ring * 200)
  }
  
  // 创建星星爆炸效果
  for (let i = 0; i < 15; i++) {
    const star = document.createElement('div')
    star.className = 'massive-firework-star'
    const starEmojis = ['✨', '⭐', '💫', '🌟', '✨']
    star.innerHTML = starEmojis[Math.floor(Math.random() * starEmojis.length)]
    
    const starX = x + (Math.random() - 0.5) * 600
    const starY = y + (Math.random() - 0.5) * 600
    
    star.style.left = `${starX}px`
    star.style.top = `${starY}px`
    star.style.zIndex = '9999'
    
    container.appendChild(star)
    
    gsap.fromTo(star, 
      { scale: 0, opacity: 1, rotation: 0 },
      { scale: 3, opacity: 0, rotation: 1440, duration: 4, ease: "power2.out", onComplete: () => {
        if (star.parentNode) {
          star.parentNode.removeChild(star)
        }
      }}
    )
  }
  
  // 清理中心元素
  setTimeout(() => {
    if (center.parentNode) {
      center.parentNode.removeChild(center)
    }
  }, 2000)
}

function playFireworkSound() {
  // 使用Web Audio API创建简单的爆炸音效
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    
    // 创建白噪声
    const bufferSize = audioContext.sampleRate * 0.1 // 0.1秒的音频
    const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate)
    const output = buffer.getChannelData(0)
    
    // 生成白噪声数据
    for (let i = 0; i < bufferSize; i++) {
      output[i] = (Math.random() * 2 - 1) * 0.1
    }
    
    // 创建音频源
    const source = audioContext.createBufferSource()
    source.buffer = buffer
    
    // 创建增益节点用于音量控制
    const gainNode = audioContext.createGain()
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime)
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1)
    
    // 连接音频节点
    source.connect(gainNode)
    gainNode.connect(audioContext.destination)
    
    // 播放音效
    source.start()
    source.stop(audioContext.currentTime + 0.1)
  } catch (error) {
    console.log('音效播放失败:', error)
  }
}

function playBirthdayMusic() {
  if (!birthdayAudioRef.value) return
  
  if (isPlaying.value) {
    birthdayAudioRef.value.pause()
    isPlaying.value = false
  } else {
    birthdayAudioRef.value.play()
      .then(() => {
        isPlaying.value = true
      })
      .catch(error => {
        console.warn('播放生日歌失败:', error)
      })
  }
}

function openGift() {
  giftOpened.value = true
  
  // 礼物打开动画
  gsap.fromTo('.gift-surprise', 
    { opacity: 0, scale: 0.8 },
    { opacity: 1, scale: 1, duration: 0.8, ease: "back.out(1.7)" }
  )
}

function closeModal() {
  // 关闭动画
  gsap.to('.birthday-modal', {
    opacity: 0,
    duration: 0.5,
    onComplete: () => {
      showModal.value = false
    }
  })
}

function cleanup() {
  if (fireworksAnimation.value) {
    clearInterval(fireworksAnimation.value)
  }
  
  if (textAnimation.value) {
    clearInterval(textAnimation.value)
  }
  
  if (birthdayAudioRef.value) {
    birthdayAudioRef.value.pause()
  }
}
</script>

<style scoped lang="scss">
.birthday-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, 
    rgba(255, 107, 107, 0.95) 0%, 
    rgba(255, 182, 193, 0.95) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  backdrop-filter: blur(10px);
}

.fireworks-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 9999;
}

.firework {
  position: absolute;
  width: 8px;
  height: 8px;
  background: radial-gradient(circle, #fff 0%, #FFD700 100%);
  border-radius: 50%;
  animation: firework-flash 0.5s ease-in-out;
  box-shadow: 0 0 20px #FFD700;
  z-index: 9999;
}

@keyframes firework-flash {
  0% { opacity: 1; transform: scale(1); }
  25% { opacity: 0.8; transform: scale(1.3); }
  50% { opacity: 0.3; transform: scale(1.8); }
  75% { opacity: 0.6; transform: scale(1.2); }
  100% { opacity: 1; transform: scale(1); }
}

.firework-particle {
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  pointer-events: none;
  animation: particle-sparkle 0.5s ease-in-out infinite alternate;
  z-index: 9999;
  box-shadow: 0 0 15px currentColor;
}

@keyframes particle-sparkle {
  0% { transform: scale(1); filter: brightness(1); }
  50% { transform: scale(1.5); filter: brightness(1.5); }
  100% { transform: scale(1); filter: brightness(1); }
}

.firework-glow {
  position: absolute;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(255,215,0,0.6) 30%, rgba(255,107,107,0.3) 60%, transparent 100%);
  pointer-events: none;
  transform: translate(-50%, -50%);
  z-index: 9998;
  box-shadow: 0 0 50px rgba(255,255,255,0.8);
}

.firework-trail {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  pointer-events: none;
  animation: trail-fade 1s ease-out;
  z-index: 9999;
}

@keyframes trail-fade {
  0% { opacity: 0.9; transform: scale(1.5); filter: brightness(1.2); }
  50% { opacity: 0.5; transform: scale(1); filter: brightness(1.5); }
  100% { opacity: 0; transform: scale(0.3); filter: brightness(0.8); }
}

.firework-star {
  position: absolute;
  font-size: 24px;
  pointer-events: none;
  text-shadow: 0 0 20px rgba(255,255,255,0.9), 0 0 40px rgba(255,215,0,0.6);
  transform: translate(-50%, -50%);
  z-index: 9999;
}

// 大型烟花效果样式
.massive-firework-center {
  position: absolute;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: radial-gradient(circle, #fff 0%, #FFD700 30%, #FF69B4 60%, transparent 100%);
  transform: translate(-50%, -50%);
  z-index: 9999;
  box-shadow: 0 0 60px #FFD700, 0 0 120px #FF69B4;
  animation: massive-center-pulse 0.5s ease-in-out;
}

@keyframes massive-center-pulse {
  0% { box-shadow: 0 0 60px #FFD700, 0 0 120px #FF69B4; }
  50% { box-shadow: 0 0 120px #FFD700, 0 0 240px #FF69B4; }
  100% { box-shadow: 0 0 60px #FFD700, 0 0 120px #FF69B4; }
}

.massive-firework-particle {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  pointer-events: none;
  z-index: 9999;
  animation: massive-particle-sparkle 0.3s ease-in-out infinite alternate;
}

@keyframes massive-particle-sparkle {
  0% { transform: scale(1); filter: brightness(1); }
  100% { transform: scale(1.3); filter: brightness(1.8); }
}

.firework-ring {
  position: absolute;
  width: 4px;
  height: 4px;
  border: 2px solid rgba(255,255,255,0.6);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  z-index: 9998;
  box-shadow: 0 0 20px rgba(255,255,255,0.4);
}

.massive-firework-star {
  position: absolute;
  font-size: 32px;
  pointer-events: none;
  text-shadow: 0 0 30px rgba(255,255,255,1), 0 0 60px rgba(255,215,0,0.8);
  transform: translate(-50%, -50%);
  z-index: 9999;
  animation: massive-star-twinkle 0.5s ease-in-out infinite alternate;
}

@keyframes massive-star-twinkle {
  0% { filter: brightness(1) drop-shadow(0 0 10px rgba(255,255,255,0.8)); }
  100% { filter: brightness(1.5) drop-shadow(0 0 20px rgba(255,255,255,1)); }
}

.cake-container {
  position: absolute;
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
  width: 200px;
  height: 200px;
  background: url('/images/birthday-cake.png') center/contain no-repeat;
  animation: cake-bounce 3s ease-in-out infinite;
}

@keyframes cake-bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(-10px); }
}

.birthday-content {
  text-align: center;
  color: white;
  max-width: 600px;
  padding: 40px;
  position: relative;
  z-index: 2;
}

.birthday-title {
  margin-bottom: 40px;
  
  .main-greeting {
    font-family: var(--font-heading);
    font-size: clamp(2rem, 6vw, 4rem);
    font-weight: 700;
    margin: 0 0 16px 0;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    background: linear-gradient(45deg, #FFE5E5, #FFFFFF);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
  }
  
  .subtitle {
    font-size: clamp(1rem, 2.5vw, 1.5rem);
    opacity: 0.9;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
}

.age-display {
  margin-bottom: 40px;
  
  .age-number {
    font-family: var(--font-display);
    font-size: clamp(4rem, 12vw, 8rem);
    font-weight: bold;
    margin-bottom: 8px;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    animation: age-glow 3s ease-in-out infinite;
  }
  
  .age-label {
    font-size: clamp(1.2rem, 3vw, 2rem);
    font-weight: 600;
  }
}

@keyframes age-glow {
  0%, 100% { 
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  }
  50% { 
    text-shadow: 0 4px 20px rgba(255, 255, 255, 0.5);
  }
}

.wishes-carousel {
  margin-bottom: 40px;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .wish-text {
    font-size: clamp(1.1rem, 2.5vw, 1.5rem);
    font-weight: 500;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    opacity: 0.95;
    animation: wish-fade 3s ease-in-out infinite;
  }
}

@keyframes wish-fade {
  0%, 100% { opacity: 0.95; transform: translateY(0); }
  50% { opacity: 1; transform: translateY(-5px); }
}

.birthday-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

.action-btn {
  padding: 12px 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--duration-normal) var(--ease-in-out);
  backdrop-filter: blur(10px);
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  }
  
  &.fireworks-btn {
    background: linear-gradient(45deg, rgba(255, 107, 107, 0.3), rgba(255, 182, 193, 0.3));
    border: 2px solid rgba(255, 107, 107, 0.5);
    animation: fireworks-btn-glow 2s ease-in-out infinite;
    
    &:hover {
      border-color: rgba(255, 107, 107, 0.8);
      background: linear-gradient(45deg, rgba(255, 107, 107, 0.5), rgba(255, 182, 193, 0.5));
      box-shadow: 0 0 20px rgba(255, 107, 107, 0.4);
      animation: fireworks-btn-pulse 0.5s ease-in-out;
    }
  }

@keyframes fireworks-btn-glow {
  0%, 100% { box-shadow: 0 0 10px rgba(255, 107, 107, 0.3); }
  50% { box-shadow: 0 0 20px rgba(255, 107, 107, 0.5); }
}

@keyframes fireworks-btn-pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}
  
  &.music-btn:hover {
    border-color: rgba(255, 182, 193, 0.7);
  }
  
  &.gift-btn:hover {
    border-color: rgba(255, 215, 0, 0.7);
  }
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 1.2rem;
  border-radius: 50%;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
  
  &:hover {
    background: rgba(0, 0, 0, 0.7);
    transform: scale(1.1);
  }
}

// 礼物模态框
.gift-modal {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
}

.gift-content {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  max-width: 500px;
  width: 90%;
  color: white;
}

.gift-box {
  margin-bottom: 30px;
  cursor: pointer;
  transition: transform var(--duration-fast) var(--ease-in-out);
  
  &:hover {
    transform: scale(1.05);
  }
  
  .gift-emoji {
    font-size: 4rem;
    margin-bottom: 16px;
    animation: gift-shake 2s ease-in-out infinite;
  }
  
  .gift-text {
    font-size: 1.2rem;
    font-weight: 500;
  }
}

@keyframes gift-shake {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-5deg); }
  75% { transform: rotate(5deg); }
}

.gift-surprise {
  margin-bottom: 30px;
  
  .surprise-emoji {
    font-size: 3rem;
    margin-bottom: 16px;
  }
  
  .surprise-title {
    font-size: 1.5rem;
    margin: 0 0 16px 0;
    font-weight: 600;
  }
  
  .surprise-message {
    font-size: 1rem;
    line-height: 1.6;
    opacity: 0.9;
    margin: 0;
  }
}

.close-gift-btn {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-in-out);
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
  }
}

// 响应式设计
@media (max-width: 768px) {
  .birthday-content {
    padding: 20px;
  }
  
  .birthday-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .action-btn {
    width: 100%;
    max-width: 200px;
  }
  
  .gift-content {
    padding: 30px 20px;
  }
  
  .cake-container {
    width: 150px;
    height: 150px;
  }
}

@media (max-width: 480px) {
  .birthday-content {
    padding: 16px;
  }
  
  .gift-content {
    padding: 20px 16px;
  }
}
</style>