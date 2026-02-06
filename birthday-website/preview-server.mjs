import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 4714;

// 1. 静态文件服务 (.output/public 目录)
app.use(express.static(path.join(__dirname, '.output/public')));

// 2. API 代理配置
// 将本地 /api/... 的请求转发到 https://wildmutou.art/api/...
app.use('/api', createProxyMiddleware({
  target: 'https://wildmutou.art/api', 
  changeOrigin: true, // 必须设置为 true，否则 SSL 握手可能会失败，或者 Host 头不匹配
  pathRewrite: {
    '^/api': '', // 去掉路径中的 /api 前缀
  },
  onProxyRes: function (proxyRes, req, res) {
    // 解决 CORS 问题：强制覆盖后端返回的 Access-Control-Allow-Origin
    // 因为后端可能返回了 invalid 的 '*,*'，或者我们本地是 localhost 需要允许跨域
    proxyRes.headers['Access-Control-Allow-Origin'] = '*';
    proxyRes.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS';
    proxyRes.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization';
  }
}));

// 3. 处理 SPA 路由 (所有未匹配的请求都返回 index.html)
app.use((req, res) => {
  res.sendFile(path.join(__dirname, '.output/public/index.html'));
});

app.listen(PORT, () => {
  console.log('-----------------------------------------------------');
  console.log(`🚀 本地预览服务器已启动！`);
  console.log(`👉 访问地址: http://localhost:${PORT}`);
  console.log(`🔗 API 代理: /api -> https://wildmutou.art/api`);
  console.log('-----------------------------------------------------');
});
