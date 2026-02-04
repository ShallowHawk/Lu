// composables/usePhotoGallery.js
import { ref, computed } from 'vue'

export function usePhotoGallery() {
  const photos = ref([])
  const loading = ref(false)
  const error = ref(null)

  // 获取所有图片文件
  async function loadPhotos() {
    loading.value = true
    error.value = null
    
    try {
      // 直接使用本地images目录的图片列表
      const localImages = [
        'IMG_0923.jpg', '8c701324617fd359fc5ee78a05f02361.JPG', 
        '180ec0db96657633daeb182fe7683ede.JPG', 'b0581c23cb2f9eee4ff7da722e134e7c.JPG',
        '0fb5830d-3188-4e07-8a56-22b181d34910.jpg', 'IMG_1293.jpg',
        'IMG_1291.jpg', 'DSC08835.JPG', 'IMG_0928.jpg', 'IMG_0670.JPG',
        'IMG_5895.jpg', 'IMG_3329.jpg', 'IMG_3276.jpg', 'IMG_3097.jpg',
        'IMG_3084.jpg', 'IMG_2342.PNG', 'IMG_1727.jpg', 'IMG_1713.jpg',
        'IMG_1163.jpg', 'IMG_1159.jpg', 'IMG_1129.jpg', 'IMG_0545.jpg',
        'IMG_0510.jpg'
      ]
      
      photos.value = localImages.map(filename => ({
        id: Math.random().toString(36).substr(2, 9),
        filename,
        url: `/images/${filename}`, // 使用本地images目录
        width: Math.floor(Math.random() * 100) + 150, // 150-250px
        height: Math.floor(Math.random() * 150) + 200, // 200-350px
        delay: Math.random() * 2 // 动画延迟
      }))
      
      // 随机打乱照片顺序
      photos.value = shuffleArray(photos.value)
      console.log(`成功加载 ${photos.value.length} 张本地照片`)
      
    } catch (err) {
      console.error('加载照片失败:', err)
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  // 随机打乱数组
  function shuffleArray(array) {
    const shuffled = [...array]
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
    }
    return shuffled
  }

  // 获取随机照片子集
  const getRandomPhotos = (count = 12) => {
    return computed(() => {
      if (photos.value.length === 0) return []
      
      const shuffled = shuffleArray(photos.value)
      return shuffled.slice(0, Math.min(count, shuffled.length))
    })
  }

  // 检查是否有照片
  const hasPhotos = computed(() => photos.value.length > 0)

  return {
    photos,
    loading,
    error,
    hasPhotos,
    loadPhotos,
    getRandomPhotos,
    shuffleArray
  }
}