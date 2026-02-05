// API配置文件
export const useApi = () => {
  // 根据环境自动切换API地址
  const baseURL = process.env.NODE_ENV === 'production' 
    ? 'http://localhost:5000'  // 生产环境
    : 'http://localhost:5000'  // 开发环境

  const api = {
    // 通用 GET 请求
    async get(endpoint) {
      try {
        const response = await $fetch(`${baseURL}${endpoint}`)
        return response
      } catch (error) {
        console.error(`GET ${endpoint} 失败:`, error)
        throw error
      }
    },

    // 通用 POST 请求
    async post(endpoint, data) {
      try {
        const response = await $fetch(`${baseURL}${endpoint}`, {
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
        const response = await $fetch(`${baseURL}/api/messages`)
        return response.messages || []
      } catch (error) {
        console.error('获取留言失败:', error)
        return []
      }
    },

    // 发送留言
    async sendMessage(content) {
      try {
        const response = await $fetch(`${baseURL}/api/messages/send`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            message: content,
            user: '木头' // 默认用户，可以根据需要修改
          })
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
        const response = await $fetch(`${baseURL}/api/messages/update`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            message_id: messageId,
            message: content,
            secret: 'birthday2024' // 添加密钥
          })
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
        const response = await $fetch(`${baseURL}/api/messages/delete`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            message_id: messageId,
            secret: 'birthday2024' // 添加密钥
          })
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