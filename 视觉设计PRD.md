# 木头的破壳日网站 - 视觉体验设计PRD

## 项目概述

**项目名称**: 木头的破壳日数字艺术纪念网站  
**项目愿景**: 打造一个融合美学与科技的浪漫数字空间，让每一次访问都成为一场视觉盛宴  
**开发周期**: 3周（目标7月16日前完成核心功能）  
**技术栈**: Vue.js 3 + Nuxt 3 + Python Flask + Socket.io + Three.js + GSAP  

## 设计理念

### 🎨 设计系统

#### 色彩体系
```scss
// 主题色板
$primary-gradient: linear-gradient(135deg, #FF6B6B 0%, #FFB6C1 100%); // 珊瑚粉到樱花粉
$secondary: #E6E6FA; // 薰衣草紫
$accent: #B76E79; // 玫瑰金
$background-light: #FFFDD0; // 奶油白
$background-dark: #2C1F3D; // 暮光紫（暗色模式）

// 功能色
$status-colors: (
  'sleeping': #9B59B6,  // 梦幻紫
  'working': #3498DB,   // 天空蓝
  'exercising': #E74C3C, // 活力红
  'gaming': #F39C12,    // 阳光橙
  'relaxing': #1ABC9C   // 薄荷绿
);
```

#### 字体系统
- **主标题**: 思源宋体 - 优雅古典
- **正文**: 苹方/思源黑体 - 清晰易读
- **数字**: Abril Fatface - 装饰性强
- **手写体**: 李旭科书法 - 温暖亲切

#### 动效原则
- **缓动函数**: cubic-bezier(0.4, 0.0, 0.2, 1)
- **动画时长**: 微交互200-400ms，页面切换600-800ms
- **性能优先**: 使用transform和opacity，避免重排

## 核心功能模块 2.0

### 1. 🌸 沉浸式Loading体验

#### 视觉设计
- **3D相册墙**: 
  - 使用Three.js创建空间感相册
  - 照片以螺旋上升方式排列
  - 鼠标悬停照片会放大并显示日期
  
- **粒子系统背景**:
  ```javascript
  // 樱花飘落效果
  particles: {
    count: 200,
    shape: 'sakura', // 自定义樱花形状
    physics: {
      gravity: 0.05,
      wind: 0.02,
      rotation: true
    }
  }
  ```

- **打字机文案效果**:
  - "正在收集我们的甜蜜瞬间..."
  - "每一张照片都是一个故事..."
  - "准备进入我们的专属世界..."

- **创意进度指示器**:
  - 两颗心从两端靠近，相遇时页面加载完成
  - 心跳频率随加载进度加快

### 2. 💕 恋爱时光机

#### 设计特色
- **液态数字显示**:
  - 数字切换使用SVG变形动画
  - 毫秒级更新，营造时间流逝感
  - 鼠标悬停时间会"凝固"

- **极光背景动画**:
  ```css
  .aurora-bg {
    background: linear-gradient(45deg, #FF6B6B, #FFB6C1, #E6E6FA);
    animation: aurora 10s ease-in-out infinite;
    filter: blur(80px);
  }
  ```

- **里程碑庆祝系统**:
  - 100天倍数：全屏烟花 + 定制祝福语
  - 特殊日期：漂浮气球动画
  - 支持自定义纪念日

- **时间胶囊功能**:
  - 悬浮卡片显示"此刻的我们"
  - 连接照片、音乐、天气等记忆元素

### 3. 🎂 生日庆典模式

#### 3D视觉盛宴
- **WebGL生日蛋糕**:
  ```javascript
  // Three.js 蛋糕模型
  const cake = new THREE.Group();
  cake.add(layers, candles, decorations);
  // 支持手势旋转查看
  controls = new OrbitControls(camera, renderer.domElement);
  ```

- **AR烟花体验**:
  - 集成WebXR API
  - 手机摄像头识别标记触发AR烟花
  - 支持录制分享

- **音乐可视化**:
  - Web Audio API分析音频
  - 音波化作彩色粒子环绕蛋糕
  - 节奏同步的灯光效果

- **祝福文字动画**:
  - 文字粒子先散开成星空
  - 重组为"生日快乐"
  - 支持自定义祝福语

### 4. 📱 智能状态展示系统

#### 玻璃拟态卡片设计
```scss
.status-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(255, 182, 193, 0.2),
    inset 0 2px 4px rgba(255, 255, 255, 0.3);
  
  // 呼吸灯边框
  &.active {
    animation: breathing-glow 2s ease-in-out infinite;
  }
}
```

#### 动态元素设计
- **Emoji动画库**:
  - 😴 睡觉：Z字漂浮上升
  - 💻 工作：键盘打字效果
  - 🏃 运动：小人跑步循环
  - 🎮 游戏：手柄按键闪烁

- **状态切换过渡**:
  - Morphing动画平滑过渡
  - 状态历史时间轴展示
  - 支持状态心情标注

### 5. 🏃‍♂️ 运动数据可视化

#### 赛博朋克仪表盘
- **心率监测器**:
  ```javascript
  // 模拟心电图效果
  const heartbeat = new Chart(ctx, {
    type: 'line',
    options: {
      animation: {
        onComplete: drawPulse
      }
    }
  });
  ```

- **3D跑步轨迹**:
  - Mapbox GL集成
  - 热力图显示运动强度
  - 支持回放功能

- **成就系统**:
  - 3D徽章模型展示
  - 解锁动画带音效
  - 成就墙Gallery视图

### 6. 💌 互动社交空间

#### 便利贴留言板
- **物理引擎**:
  - Matter.js实现真实物理效果
  - 便利贴可拖拽、旋转
  - 碰撞检测防止重叠

- **手写效果**:
  - 集成手写字体
  - 支持涂鸦绘画
  - 多种信纸模板

#### 情侣小游戏
- **记忆翻牌**:
  - 卡片翻转3D效果
  - 渐进难度系统
  - 最高分记录

- **默契测试**:
  - 实时对战模式
  - 答案一致度分析
  - 生成默契度报告

### 7. 📊 动态时间线

#### 视觉设计
- **时空隧道效果**:
  - 3D透视滚动
  - 重要事件高亮发光
  - 平滑视差滚动

- **卡片设计系统**:
  - 根据内容类型自适应布局
  - 悬停展开详情
  - 支持多媒体内容

## 🎵 声音设计系统

### 背景音乐
- **智能播放列表**:
  - 根据页面情绪切换BGM
  - 淡入淡出过渡
  - 用户可上传定制

### 交互音效
```javascript
const sounds = {
  click: new Howl({ src: ['click.mp3'], volume: 0.3 }),
  hover: new Howl({ src: ['hover.mp3'], volume: 0.2 }),
  success: new Howl({ src: ['success.mp3'], volume: 0.5 }),
  notification: new Howl({ src: ['notify.mp3'], volume: 0.4 })
};
```

## 🌈 氛围系统

### 智能主题切换
- **时间感知**:
  - 6:00-18:00 明亮模式
  - 18:00-6:00 暗色模式
  - 过渡时长30分钟

- **天气同步**:
  ```javascript
  // 获取实时天气
  weather.on('rain', () => {
    particles.add('raindrops');
    audio.play('rain-ambience');
  });
  ```

- **节日皮肤**:
  - 情人节：玫瑰花瓣飘落
  - 圣诞节：雪花 + 铃铛音效
  - 春节：红包雨 + 烟花

## 📱 响应式体验

### 移动端优化
- **手势交互**:
  - 左右滑动切换模块
  - 双指缩放照片
  - 长按保存图片

- **触觉反馈**:
  ```javascript
  // Haptic Feedback API
  navigator.vibrate([200, 100, 200]); // 重要操作
  navigator.vibrate(50); // 轻触反馈
  ```

- **性能优化**:
  - 图片WebP格式 + 懒加载
  - Virtual Scroll虚拟滚动
  - Service Worker离线缓存

## 🎁 个性化系统

### 主题编辑器
- **可视化配置**:
  - 实时预览主题效果
  - 颜色选择器
  - 字体大小调节

### 布局定制
- **拖拽式编辑器**:
  - Grid布局系统
  - 模块显示/隐藏
  - 保存多套布局

### 内容管理
- **素材上传**:
  - 批量照片上传
  - 自定义表情包
  - 背景音乐管理

## 🚀 技术架构升级

### 前端技术栈
```json
{
  "framework": "Nuxt 3 + Vue 3",
  "ui": "Naive UI + 自定义组件库",
  "animation": "GSAP + Three.js + Lottie",
  "charts": "ECharts + D3.js",
  "audio": "Howler.js + Web Audio API",
  "pwa": "Workbox + Web App Manifest"
}
```

### 性能指标
- 首屏加载 < 2秒
- 交互响应 < 100ms
- 动画保持 60FPS
- Lighthouse评分 > 95

## 📅 开发计划

### 第一阶段：核心体验（第1周）
- [ ] 设计系统搭建
- [ ] 3D Loading页面
- [ ] 恋爱计时器高级版
- [ ] 状态卡片玻璃拟态

### 第二阶段：视觉升级（第2周）
- [ ] 生日3D蛋糕
- [ ] 运动数据可视化
- [ ] 粒子系统集成
- [ ] 声音系统实现

### 第三阶段：交互完善（第3周）
- [ ] 手势交互系统
- [ ] 个性化配置
- [ ] 性能优化
- [ ] 部署上线

## ✨ 创新亮点

1. **沉浸式体验**: 每个页面都是一个小世界
2. **情感化设计**: 细节处处体现爱意
3. **技术与艺术**: 前沿技术打造艺术品
4. **持续惊喜**: 不断解锁新功能
5. **共同成长**: 记录两人一起的时光

---

**这份PRD将技术与美学完美融合，相信木头看到成品一定会惊喜到哭的！** 🎁✨