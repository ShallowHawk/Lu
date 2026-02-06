// API配置文件
export const useApi = () => {
  // 生产环境 API 地址
  const baseURL = 'https://wildmutou.art/api'
  
  // 本地开发时，如果需要调试本地后端，可以临时改为 'http://localhost:5000'
  // 但目前需求是直接连线上，所以保持不变
  
  const headers = {
    'Content-Type': 'application/json',
  }

  const api = {
    // 通用 GET 请求
    async get(endpoint) {
      try {
        // endpoint 如果自带 /api 前缀则去除，避免重复
        const cleanEndpoint = endpoint.startsWith('/api') ? endpoint.replace('/api', '') : endpoint
        const response = await $fetch(`${baseURL}${cleanEndpoint}`)
        return response
      } catch (error) {
        console.error(`GET ${endpoint} 失败:`, error)
        throw error
      }
    },

    // 通用 POST 请求
    async post(endpoint, data) {
      try {
        const cleanEndpoint = endpoint.startsWith('/api') ? endpoint.replace('/api', '') : endpoint
        const response = await $fetch(`${baseURL}${cleanEndpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })
        return response
      } catch (error) {
        console.error(`POST ${endpoint} 失败:`, error)
        throw error
      }
    },

    // 获取当前状态
    async getStatus() {
      try {
        const response = await $fetch(`${baseURL}/status`)
        return response
      } catch (error) {
        console.error('获取状态失败:', error)
        return null
      }
    },

    // 获取历史记录
    async getHistory() {
      try {
        const response = await $fetch(`${baseURL}/history`)
        return response
      } catch (error) {
        console.error('获取历史记录失败:', error)
        return []
      }
    },

    // 更新状态（如果需要手动更新）
    async updateStatus(status) {
      try {
        const response = await $fetch(`${baseURL}/update_status`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ status })
        })
        return response
      } catch (error) {
        console.error('更新状态失败:', error)
        return null
      }
    },

    // 获取留言板消息
    async getMessages() {
      try {
        const response = await this.get('/messages') // 复用 this.get 自动处理 baseURL
        return response.messages || []
      } catch (error) {
        console.error('获取留言失败:', error)
        return []
      }
    },

    // 发送留言
    async sendMessage(content, user = '访客') {
      try {
        const response = await this.post('/messages/send', {
          message: content,
          user: user
        })
        return response
      } catch (error) {
        console.error('发送留言失败:', error)
        return null
      }
    },

    // 更新留言
    async updateMessage(messageId, content) {
      try {
        const response = await this.post('/messages/update', {
          message_id: messageId,
          message: content,
          secret: 'birthday2024' // 添加密钥
        })
        return response
      } catch (error) {
        console.error('更新留言失败:', error)
        return null
      }
    },

    // 删除留言
    async deleteMessage(messageId) {
      try {
        const response = await this.post('/messages/delete', {
          message_id: messageId,
          secret: 'birthday2024' // 添加密钥
        })
        return response
      } catch (error) {
        console.error('删除留言失败:', error)
        return null
      }
    }
  }

  return {
    api: {
      ...api,
      baseURL  // 将baseURL添加到api对象中
    },
    baseURL
  }
} 