<template>
  <div class="timeline-container">
    <div class="notebook-wrapper">
      <!-- 笔记本封面装饰 -->
      <div class="notebook-spiral"></div>
      
      <!-- 笔记本内容 -->
      <div class="notebook-paper">
        <h3 class="notebook-title text-handwriting">
          <span class="icon">📖</span> 我们的故事
        </h3>
        
        <div class="timeline-content">
          <div 
            v-for="(event, index) in events" 
            :key="index"
            class="timeline-item"
            :class="{ 'left': index % 2 === 0, 'right': index % 2 !== 0 }"
          >
            <div class="timeline-marker"></div>
            <div class="timeline-date text-heading">{{ event.date }}</div>
            <div class="timeline-card">
              <div class="event-title text-heading">{{ event.title }}</div>
              <div class="event-desc text-handwriting">{{ event.description }}</div>
              <div v-if="event.image" class="event-image">
                <img :src="event.image" :alt="event.title" loading="lazy" />
                <div class="tape-decoration"></div>
              </div>
            </div>
          </div>
          
          <!-- 未完待续 -->
          <div class="timeline-end text-handwriting">
            ... 未完待续 ...
          </div>
        </div>

        <!-- 照片墙部分 -->
        <div class="photo-gallery-section">
          <h3 class="gallery-title text-heading">
            <span class="icon">📸</span> 甜蜜瞬间
          </h3>
          <div class="waterfall-gallery">
            <div 
              v-for="(photo, index) in photoList" 
              :key="index"
              class="photo-card"
              :style="{ transform: `rotate(${Math.random() * 6 - 3}deg)` }"
            >
              <div class="photo-frame">
                <img :src="photo.src" loading="lazy" />
              </div>
              <div class="photo-date text-handwriting">{{ photo.date }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePhotoGallery } from '~/composables/usePhotoGallery'

// 模拟时间线数据
const events = ref([
  {
    date: '2022.11.02',
    title: '故事的开始',
    description: '那是我们第一次相遇的日子，虽然很普通，但因为有你而变得闪闪发光。',
    image: null
  },
  {
    date: '2023.02.14',
    title: '第一个情人节',
    description: '即使相隔两地，心也是连在一起的。那天晚上的月亮很美。',
    image: null
  },
  {
    date: '2023.07.16',
    title: '木头的生日',
    description: '祝全世界最好的木头生日快乐！希望你的每一天都充满阳光。',
    image: null
  },
  {
    date: '2024.01.01',
    title: '新年快乐',
    description: '新的一年，也要请多指教哦。一起去看了烟花，真的很开心。',
    image: null
  }
])

const { photos, loadPhotos } = usePhotoGallery()
const photoList = ref([])

onMounted(async () => {
  await loadPhotos()
  
  if (photos.value.length > 0) {
    photoList.value = photos.value.map(photo => ({
      src: photo.url,
      date: '美好瞬间'
    }))
  } else {
    // Fallback if no photos loaded
    const demoPhotos = [
      '/images/IMG_0545.jpg',
      '/images/IMG_0923.jpg',
      '/images/IMG_1129.jpg',
      '/images/IMG_1159.jpg',
      '/images/IMG_1291.jpg',
      '/images/IMG_3084.jpg'
    ]
    photoList.value = demoPhotos.map(src => ({
      src,
      date: '2023.xx.xx'
    }))
  }
})
</script>

<style scoped lang="scss">
.timeline-container {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.notebook-wrapper {
  position: relative;
  width: 100%;
  max-width: 700px;
  margin-left: 15px; // 给线圈留位置
}

.notebook-paper {
  background: #fff;
  padding: 40px 30px;
  box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
  min-height: 500px;
  border-radius: 4px 16px 16px 4px;
  
  // 格子纸纹理
  background-image: 
    linear-gradient(#e1f5fe 1px, transparent 1px),
    linear-gradient(90deg, #e1f5fe 1px, transparent 1px);
  background-size: 20px 20px;
  background-position: 0 0;
  
  // 红色边距线
  border-left: 2px solid #ffcdd2;
  padding-left: 40px;
}

.notebook-spiral {
  position: absolute;
  left: -15px;
  top: 20px;
  bottom: 20px;
  width: 30px;
  background: repeating-linear-gradient(
    0deg,
    transparent 0px,
    transparent 20px,
    #555 20px,
    #555 24px,
    transparent 24px,
    transparent 40px
  );
  z-index: 10;
  
  &::after {
    content: '';
    position: absolute;
    top: 0;
    bottom: 0;
    left: 12px;
    width: 6px;
    background: #fff;
    border-radius: 3px;
  }
}

.notebook-title, .gallery-title {
  text-align: center;
  font-size: 2rem;
  color: var(--text-ink);
  margin-bottom: 40px;
  padding-bottom: 10px;
  border-bottom: 2px dashed var(--primary-pink);
  
  .icon {
    font-size: 1.8rem;
    vertical-align: middle;
  }
}

.timeline-content {
  position: relative;
  margin-bottom: 60px;
  
  &::before {
    content: '';
    position: absolute;
    left: 20px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--primary-pink);
    opacity: 0.5;
  }
}

.timeline-item {
  position: relative;
  margin-bottom: 40px;
  padding-left: 50px;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.timeline-marker {
  position: absolute;
  left: 15px;
  top: 5px;
  width: 12px;
  height: 12px;
  background: var(--primary-pink);
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 0 0 2px var(--primary-pink);
  z-index: 2;
}

.timeline-date {
  font-size: 1.2rem;
  color: var(--primary-pink);
  margin-bottom: 8px;
  font-weight: bold;
}

.timeline-card {
  background: rgba(255, 255, 255, 0.9);
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  border: 1px solid rgba(0,0,0,0.05);
  transform: rotate(-1deg);
  transition: transform 0.3s ease;
  
  &:hover {
    transform: rotate(0) scale(1.02);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }
}

.event-title {
  font-size: 1.3rem;
  color: var(--text-ink);
  margin-bottom: 8px;
}

.event-desc {
  font-size: 1rem;
  color: var(--text-light);
  line-height: 1.6;
}

.event-image {
  margin-top: 15px;
  position: relative;
  
  img {
    width: 100%;
    border-radius: 4px;
    border: 4px solid #fff;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .tape-decoration {
    position: absolute;
    top: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 20px;
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid rgba(0,0,0,0.1);
    transform: translateX(-50%) rotate(2deg);
  }
}

.timeline-end {
  text-align: center;
  margin-top: 40px;
  color: var(--text-light);
  opacity: 0.6;
  letter-spacing: 2px;
}

// 照片墙样式
.photo-gallery-section {
  margin-top: 50px;
  padding-top: 30px;
  border-top: 2px dashed #ddd;
}

.waterfall-gallery {
  column-count: 2;
  column-gap: 15px;
  
  @media (min-width: 600px) {
    column-count: 3;
  }
}

.photo-card {
  break-inside: avoid;
  margin-bottom: 20px;
  background: white;
  padding: 10px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
  
  &:hover {
    transform: scale(1.05) rotate(0deg) !important;
    z-index: 10;
  }
}

.photo-frame {
  width: 100%;
  overflow: hidden;
  margin-bottom: 8px;
  
  img {
    width: 100%;
    height: auto;
    display: block;
    filter: sepia(0.2); // 复古感
  }
}

.photo-date {
  text-align: right;
  font-size: 0.9rem;
  color: #888;
}

// 移动端适配
@media (max-width: 480px) {
  .notebook-paper {
    padding: 30px 15px;
    padding-left: 25px; // 减少左边距
  }
  
  .notebook-wrapper {
    margin-left: 10px;
  }
  
  .timeline-item {
    padding-left: 30px;
  }
  
  .timeline-content::before {
    left: 10px;
  }
  
  .timeline-marker {
    left: 5px;
  }
}
</style>
