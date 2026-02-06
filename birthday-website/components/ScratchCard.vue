<template>
  <div class="scratch-card-container" ref="container">
    <div class="content-layer">
      <slot></slot>
    </div>
    <canvas ref="canvas" class="scratch-canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'

const container = ref(null)
const canvas = ref(null)
let ctx = null
let isDrawing = false

const props = defineProps({
  width: {
    type: Number,
    default: 300
  },
  height: {
    type: Number,
    default: 100
  },
  coverColor: {
    type: String,
    default: '#cccccc'
  },
  brushSize: {
    type: Number,
    default: 20
  },
  revealThreshold: {
    type: Number,
    default: 0.4 // 40%
  }
})

const emit = defineEmits(['reveal'])

let isRevealed = false
let checkCounter = 0

onMounted(() => {
  // Use nextTick to ensure container has dimensions
  nextTick(() => {
    initCanvas()
  })
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

function initCanvas() {
  if (!canvas.value || !container.value) return

  // Ensure we have dimensions
  const w = props.width || container.value.offsetWidth
  const h = props.height || container.value.offsetHeight
  
  if (w === 0 || h === 0) {
      // Retry if dimensions are not yet available
      setTimeout(initCanvas, 100)
      return
  }

  canvas.value.width = w
  canvas.value.height = h
  
  ctx = canvas.value.getContext('2d')
  
  // Fill with cover color
  ctx.fillStyle = props.coverColor
  ctx.fillRect(0, 0, w, h)
  
  // Add some text or pattern on top of the cover (optional)
  ctx.font = '16px Arial'
  ctx.fillStyle = '#999'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillText('刮开查看提示', w / 2, h / 2)

  // Setup event listeners
  const c = canvas.value
  
  // Mouse
  c.addEventListener('mousedown', startDrawing)
  c.addEventListener('mousemove', draw)
  c.addEventListener('mouseup', stopDrawing)
  c.addEventListener('mouseleave', stopDrawing)
  
  // Touch
  c.addEventListener('touchstart', handleTouchStart, { passive: false })
  c.addEventListener('touchmove', handleTouchMove, { passive: false })
  c.addEventListener('touchend', stopDrawing)
}

function handleResize() {
  // Optional: Reset canvas on resize or scale it
  // For simplicity, we might just leave it or re-init
  // initCanvas() 
}

function getPos(e) {
  const rect = canvas.value.getBoundingClientRect()
  let clientX, clientY
  
  if (e.changedTouches) {
    clientX = e.changedTouches[0].clientX
    clientY = e.changedTouches[0].clientY
  } else {
    clientX = e.clientX
    clientY = e.clientY
  }
  
  return {
    x: clientX - rect.left,
    y: clientY - rect.top
  }
}

function startDrawing(e) {
  isDrawing = true
  draw(e)
}

function handleTouchStart(e) {
  e.preventDefault() // Prevent scrolling
  startDrawing(e)
}

function handleTouchMove(e) {
  e.preventDefault()
  draw(e)
}

function draw(e) {
  if (!isDrawing || isRevealed) return
  
  const pos = getPos(e)
  
  ctx.globalCompositeOperation = 'destination-out'
  ctx.beginPath()
  ctx.arc(pos.x, pos.y, props.brushSize, 0, Math.PI * 2)
  ctx.fill()
  
  // Check every 10 draw calls to improve performance
  checkCounter++
  if (checkCounter % 10 === 0) {
      checkReveal()
  }
}

function stopDrawing() {
  isDrawing = false
}

function checkReveal() {
  if (isRevealed) return

  const w = canvas.value.width
  const h = canvas.value.height
  
  // Get all pixel data
  const imageData = ctx.getImageData(0, 0, w, h)
  const pixels = imageData.data
  const totalPixels = pixels.length / 4
  let transparentPixels = 0
  
  // Check alpha channel of each pixel
  // Optimize by checking every 4th pixel (stride) to speed up
  for (let i = 3; i < pixels.length; i += 16) {
    if (pixels[i] < 128) {
      transparentPixels++
    }
  }
  
  // Since we skipped pixels, we need to adjust total count for ratio
  // We checked 1 pixel out of 4 (stride of 16 bytes = 4 pixels)
  const checkedPixels = totalPixels / 4
  const ratio = transparentPixels / checkedPixels
  
  if (ratio > props.revealThreshold) {
    // Reveal all
    ctx.clearRect(0, 0, w, h)
    isRevealed = true
    canvas.value.style.pointerEvents = 'none' // Disable further interaction
    emit('reveal')
  }
}

</script>

<style scoped>
.scratch-card-container {
  position: relative;
  width: 100%;
  height: 100%;
  user-select: none;
  overflow: hidden;
}

.content-layer {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.scratch-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
  z-index: 2;
}
</style>