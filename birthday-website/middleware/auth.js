export default defineNuxtRouteMiddleware((to, from) => {
  // 使用 useCookie 获取状态，这在服务端和客户端都能工作
  const roleCookie = useCookie('user_role')
  const userRole = roleCookie.value
  
  // 如果没有登录信息，强制跳转到登录页
  // 注意：登录页路径是 '/' (index.vue)，主页路径是 '/home'
  if (!userRole && to.path !== '/') {
    return navigateTo('/')
  }
  
  // 如果已经登录了，访问登录页时跳转到主页
  if (userRole && to.path === '/') {
    return navigateTo('/home')
  }
})