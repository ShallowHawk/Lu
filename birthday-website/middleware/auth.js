export default defineNuxtRouteMiddleware((to, from) => {
  // 在服务端无法访问 localStorage，所以只能在客户端执行检查
  if (process.client) {
    const userRole = localStorage.getItem('user_role')
    
    // 如果没有登录信息，强制跳转到登录页
    // 注意：登录页路径是 '/' (index.vue)，主页路径是 '/home'
    if (!userRole && to.path !== '/') {
      return navigateTo('/')
    }
    
    // 如果已经登录了，访问登录页时跳转到主页
    if (userRole && to.path === '/') {
      return navigateTo('/home')
    }
  } else {
    // 服务端渲染时，如果访问的不是根路径，可以考虑是否需要重定向
    // 但因为无法判断用户状态，通常不做强制处理，交给客户端接管后处理
    // 或者，如果你希望所有直接访问 /home 的请求都先跳回 / 让客户端判断：
    // if (to.path !== '/') return navigateTo('/')
  }
})