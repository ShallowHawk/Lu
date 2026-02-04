<template>
  <div class="audio-manager">
    <!-- 音频控制器 -->
    <div class="audio-controls" :class="{ 'expanded': showControls }">
      <button 
        class="audio-toggle"
        @click="toggleAudio"
        :title="isPlaying ? '暂停音乐' : '播放音乐'"
      >
        <span v-if="isPlaying">🔊</span>
        <span v-else>🔇</span>
      </button>
      
      <div class="volume-control" v-if="showControls">
        <input 
          type="range" 
          v-model="volume" 
          min="0" 
          max="100" 
          class="volume-slider"
          @input="updateVolume"
        />
      </div>
      
      <button 
        class="controls-toggle"
        @click="showControls = !showControls"
        title="音频设置"
      >
        ⚙️
      </button>
    </div>
    
    <!-- 音频元素 -->
    <audio 
      ref="bgmRef"
      loop
      preload="none"
      @loadeddata="onAudioLoaded"
      @error="onAudioError"
    >
      <!-- 暂时注释掉音频源，等音频文件准备好后再启用 -->
      <!-- <source src="/audio/background.mp3" type="audio/mpeg">
      <source src="/audio/background.ogg" type="audio/ogg"> -->
    </audio>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// 响应式状态
const isPlaying = ref(false)
const volume = ref(30) // 默认音量30%
const showControls = ref(false)
const bgmRef = ref(null)
const isLoaded = ref(false)

// 生命周期
onMounted(() => {
  initAudio()
  loadUserPreferences()
})

onUnmounted(() => {
  saveUserPreferences()
})

// 方法
function initAudio() {
  if (bgmRef.value) {
    bgmRef.value.volume = volume.value / 100
    
    // 自动播放（需要用户交互）
    document.addEventListener('click', startAudioOnFirstInteraction, { once: true })
  }
}

function startAudioOnFirstInteraction() {
  if (isLoaded.value && !isPlaying.value) {
    playAudio()
  }
}

function toggleAudio() {
  if (isPlaying.value) {
    pauseAudio()
  } else {
    playAudio()
  }
}

function playAudio() {
  if (bgmRef.value && isLoaded.value) {
    bgmRef.value.play()
      .then(() => {
        isPlaying.value = true
      })
      .catch(error => {
        console.warn('音频播放失败:', error)
      })
  }
}

function pauseAudio() {
  if (bgmRef.value) {
    bgmRef.value.pause()
    isPlaying.value = false
  }
}

function updateVolume() {
  if (bgmRef.value) {
    bgmRef.value.volume = volume.value / 100
  }
  saveUserPreferences()
}

function onAudioLoaded() {
  isLoaded.value = true
  console.log('背景音乐加载完成')
}

function onAudioError(error) {
  console.warn('音频加载失败:', error)
}

function loadUserPreferences() {
  try {
    const saved = localStorage.getItem('audioPreferences')
    if (saved) {
      const prefs = JSON.parse(saved)
      volume.value = prefs.volume || 30
      
      if (bgmRef.value) {
        bgmRef.value.volume = volume.value / 100
      }
    }
  } catch (error) {
    console.warn('加载音频偏好失败:', error)
  }
}

function saveUserPreferences() {
  try {
    const prefs = {
      volume: volume.value,
      lastSaved: Date.now()
    }
    localStorage.setItem('audioPreferences', JSON.stringify(prefs))
  } catch (error) {
    console.warn('保存音频偏好失败:', error)
  }
}

// 音效播放函数（供其他组件调用）
function playSound(soundName) {
  // 创建临时音频元素播放音效
  const audio = new Audio(`/audio/sounds/${soundName}.mp3`)
  audio.volume = (volume.value / 100) * 0.5 // 音效音量相对较小
  audio.play().catch(error => {
    console.warn(`音效 ${soundName} 播放失败:`, error)
  })
}

// 导出给其他组件使用
defineExpose({
  playSound,
  toggleAudio,
  updateVolume
})
</script>

<style scoped lang="scss">
.audio-manager {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.audio-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 25px;
  padding: 8px 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all var(--duration-normal) var(--ease-in-out);
  
  &.expanded {
    padding: 8px 16px;
  }
}

.audio-toggle,
.controls-toggle {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  transition: transform var(--duration-fast) var(--ease-in-out);
  
  &:hover {
    transform: scale(1.1);
  }
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.volume-slider {
  width: 80px;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
  
  &::-webkit-slider-thumb {
    appearance: none;
    width: 16px;
    height: 16px;
    background: white;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
  
  &::-moz-range-thumb {
    width: 16px;
    height: 16px;
    background: white;
    border-radius: 50%;
    cursor: pointer;
    border: none;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
}

// 响应式设计
@media (max-width: 768px) {
  .audio-manager {
    bottom: 16px;
    right: 16px;
  }
  
  .audio-controls {
    padding: 6px 10px;
    
    &.expanded {
      padding: 6px 12px;
    }
  }
  
  .audio-toggle,
  .controls-toggle {
    font-size: 1rem;
  }
  
  .volume-slider {
    width: 60px;
  }
}
</style>