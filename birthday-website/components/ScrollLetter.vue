<template>
  <Transition name="fade">
    <div v-if="visible" class="scroll-letter-overlay" @click="handleOverlayClick">
      <div class="scroll-container" @click.stop :class="{ 'open': isOpen }">
        <!-- 卷轴轴杆 (左/上) -->
        <div class="scroll-rod rod-top">
          <div class="rod-knob left"></div>
          <div class="rod-knob right"></div>
        </div>
        
        <!-- 卷轴内容区域 -->
        <div class="scroll-content-wrapper">
          <div class="scroll-paper">
            <div class="paper-texture"></div>
            
            <div class="letter-content text-handwriting">
              <h3 class="letter-title">Hi，木头：</h3>
              
              <div class="letter-body">
                <p>当你看到这张纸条并打开这个网站时，距离它的第一个版本（2025年6月你的生日）已经过去了快八个月。</p>
                <p>还记得吗？最初它只是一串冰冷难记的 IP 地址，像是一个还没正式安家的临时站点。而今天，我给它注册了一个永久的域名：<span class="highlight">wildmutou.art</span>。</p>
                <p>“野生的木头”——这是我能想到最像你的词。你有你的倔强，有你对世界独特的感知，虽然偶尔像木头一样不善言辞，但在我心里，你从来都是那个蓬勃、自由、无可替代的野生存在。</p>
                <p>时间过得真的很快，快到让我们有些措手不及。1月28号那天，我们还在为了那些遥远的以后争吵、内耗；可一转眼，生活就给了我们最沉重的一击。这几天，看着你在医院走廊里守着外婆，看着你面对那些不乐观的检查结果时的无力感，我真的很心疼。</p>
                <p>我知道，现在的你可能觉得世界正在崩塌。面对生老病死，我们都显得那么渺小，但这正是我想把这个网站“升级”的初衷。</p>
                <p>以前的我，可能表现得太“人机”了——习惯用逻辑去拆解问题，习惯用理智去分析利弊，却忽略了你最需要的其实是一个能感知你体温的怀抱。</p>
                
                <div class="update-log">
                  <h4 class="update-title">🛠️ 2.0 版本更新日志：</h4>
                  <div class="update-item">
                    <p>1. 关于“人机”的修复：</p>
                    <div class="progress-bar-container">
                      <div class="progress-label">逻辑模块占比 ⬇️ 20%</div>
                      <div class="progress-track"><div class="progress-fill logic" style="width: 20%"></div></div>
                    </div>
                    <div class="progress-bar-container">
                      <div class="progress-label">情感支持模块 ⬆️ 80%</div>
                      <div class="progress-track"><div class="progress-fill emotion" style="width: 80%"></div></div>
                    </div>
                    <p class="status-text">状态：正在全力陪伴木头度过难关...</p>
                  </div>
                  <div class="update-item">
                     <p>2. 关于“域名”的解析：</p>
                     <p>从此以后，无论我们未来在哪个城市，无论面对什么样的风雨，wildmutou 都有一个确定的指向——那就是我。我会一直陪着你，做你最稳定的服务器。</p>
                  </div>
                </div>

                <p>木头，别怕。虽然我不能替你分担外婆的病痛，但我会一直守在你的信号覆盖范围内。</p>
                <p><span class="highlight">wildmutou.art</span> 已经永久上线。</p>
                <p>无论何时你觉得累了，回头看，乾雨一直都在。</p>
              </div>
              
              <div class="letter-footer">
                <p>爱你的 乾雨</p>
                <p>2026.02</p>
                <div class="footer-note">
                  * IP是会变的，但域名是唯一的。
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 卷轴轴杆 (右/下) -->
        <div class="scroll-rod rod-bottom">
          <div class="rod-knob left"></div>
          <div class="rod-knob right"></div>
          
          <!-- 打开按钮 (未打开时显示) -->
          <div v-if="!isOpen" class="open-seal" @click="openScroll">
            <span class="seal-text">亲启</span>
          </div>
        </div>
        
        <!-- 关闭按钮 -->
        <button v-if="isOpen" class="close-btn" @click="close">
          朕已阅
        </button>
        
        <!-- 调试用的临时关闭按钮 (仅关闭弹窗，不标记已读) -->
        <div v-if="isOpen" class="debug-close" @click="tempClose" title="调试用：仅关闭，下次刷新还会显示">
          ×
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'close'])

const visible = ref(false)
const isOpen = ref(false)

onMounted(() => {
  if (props.modelValue) {
    visible.value = true
  }
})

function openScroll() {
  isOpen.value = true
}

function close() {
  visible.value = false
  emit('update:modelValue', false)
  emit('close', true) // true 表示正式阅后即焚
}

function tempClose() {
  visible.value = false
  emit('update:modelValue', false)
  emit('close', false) // false 表示仅临时关闭
}

function handleOverlayClick() {
  // Optional: click outside to close only if already open?
  // strict mode: must click button
}

// Watch prop change to show
import { watch } from 'vue'
watch(() => props.modelValue, (val) => {
  visible.value = val
  if (val) {
    // Reset state
    isOpen.value = false
  }
})

</script>

<style scoped lang="scss">
.scroll-letter-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(5px);
}

.scroll-container {
  position: relative;
  width: 90%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  
  // 初始折叠状态高度
  height: 120px; 
  
  &.open {
    height: 80vh; // 展开高度
    
    .scroll-content-wrapper {
      opacity: 1;
      pointer-events: auto;
    }
  }
}

.scroll-rod {
  width: 100%;
  height: 40px;
  background: #8B4513;
  border-radius: 20px;
  position: relative;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  z-index: 10;
  display: flex;
  justify-content: center;
  align-items: center;
  
  // 木纹
  background-image: repeating-linear-gradient(90deg, rgba(255,255,255,0.1) 0px, rgba(255,255,255,0.1) 1px, transparent 1px, transparent 10px);
  
  .rod-knob {
    position: absolute;
    width: 20px;
    height: 50px;
    background: #5D4037;
    top: -5px;
    border-radius: 4px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    border: 1px solid #3E2723;
    
    &.left { left: -10px; }
    &.right { right: -10px; }
  }
}

.scroll-content-wrapper {
  flex: 1;
  width: 95%; // 比轴稍微窄一点
  background: #FDF5E6; // 羊皮纸色
  overflow: hidden;
  position: relative;
  transition: opacity 0.5s ease;
  opacity: 0; // 初始隐藏
  pointer-events: none;
  
  // 纸张阴影
  box-shadow: inset 0 0 30px rgba(139, 69, 19, 0.2);
  margin: -15px 0; // 塞进轴里
  z-index: 5;
}

.scroll-paper {
  width: 100%;
  height: 100%;
  padding: 40px 30px;
  overflow-y: auto;
  position: relative;
  
  // 卷轴展开动画
  mask-image: linear-gradient(to bottom, transparent, black 10%, black 90%, transparent);
}

.paper-texture {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.5' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
}

.letter-content {
  color: #5D4037;
  line-height: 1.8;
  font-size: 1.1rem;
}

.letter-title {
  text-align: center;
  font-size: 1.5rem;
  margin-bottom: 30px;
  color: #3E2723;
  font-weight: bold;
  border-bottom: 2px solid rgba(139, 69, 19, 0.3);
  padding-bottom: 10px;
  display: inline-block;
  width: 100%;
}

.letter-body {
  p {
    margin-bottom: 15px;
    text-indent: 2em;
  }
}

.highlight {
  color: #CB4042;
  font-weight: bold;
  background: rgba(203, 64, 66, 0.1);
  padding: 0 4px;
  border-radius: 4px;
}

.update-log {
  background: rgba(139, 69, 19, 0.05);
  padding: 15px;
  border-radius: 8px;
  margin: 20px 0;
  border: 1px dashed rgba(139, 69, 19, 0.3);
}

.update-title {
  font-weight: bold;
  margin-bottom: 15px;
  color: #3E2723;
}

.update-item {
  margin-bottom: 15px;
  
  p {
    text-indent: 0;
    margin-bottom: 8px;
    font-weight: bold;
  }
}

.progress-bar-container {
  margin-bottom: 10px;
  padding-left: 20px;
}

.progress-label {
  font-size: 0.9rem;
  margin-bottom: 4px;
  color: #5D4037;
}

.progress-track {
  width: 100%;
  height: 12px;
  background: #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 1s ease-out;
  
  &.logic { background: #90A4AE; }
  &.emotion { background: #FF9AA2; }
}

.status-text {
  font-size: 0.9rem;
  color: #CB4042;
  font-style: italic;
  margin-top: 5px;
  padding-left: 20px;
}

.footer-note {
  font-size: 0.8rem;
  color: #8D6E63;
  margin-top: 10px;
  font-style: italic;
  opacity: 0.8;
}

.letter-footer {
  text-align: right;
  margin-top: 40px;
  font-weight: bold;
}

.open-seal {
  width: 60px;
  height: 60px;
  background: #CB4042; // 印泥红
  border-radius: 50%;
  position: absolute;
  top: -30px; // 骑在轴上
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  cursor: pointer;
  border: 2px solid #fff;
  animation: pulse 2s infinite;
  z-index: 20;
  
  .seal-text {
    color: white;
    font-weight: bold;
    font-size: 1.2rem;
    writing-mode: vertical-rl;
    letter-spacing: 2px;
  }
}

.close-btn {
  margin-top: 20px;
  margin-bottom: 20px;
  padding: 10px 30px;
  background: #8B4513;
  color: white;
  border: none;
  border-radius: 20px;
  font-family: inherit;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  transition: all 0.3s;
  z-index: 20;
  
  &:hover {
    background: #5D4037;
    transform: translateY(-2px);
  }
}

.debug-close {
  position: absolute;
  top: -40px;
  right: 0;
  width: 30px;
  height: 30px;
  background: rgba(0,0,0,0.3);
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  font-size: 1.2rem;
  z-index: 100;
  
  &:hover {
    background: rgba(0,0,0,0.6);
  }
}

@keyframes pulse {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(203, 64, 66, 0.7); }
  70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(203, 64, 66, 0); }
  100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(203, 64, 66, 0); }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>