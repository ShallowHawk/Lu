# Birthday Website & Sleepy Status

这是一个为女朋友定制的生日纪念网站，包含二次元风格的前端界面和基于 Flask 的后端服务。

## 功能特性

*   **前端 (Nuxt 3 + Vue 3)**:
    *   **日式和风/动漫风格**: 樱花飘落、手写字体、御守卡片。
    *   **多Tab设计**: 首页(倒计时)、动态(时间轴+照片墙)、留言板。
    *   **特色组件**: 
        *   `LoveTimer`: 夏目友人帐风格的恋爱计时器。
        *   `StatusCard`: 实时状态御守卡片，支持查看对方状态。
        *   `Omikuji`: 全功能抽签系统，集成真实天气和星座运势。
    *   **权限系统**: 暗号登录 (木头专属) vs 访客模式 (仅查看留言)。

*   **后端 (Flask)**:
    *   **API 服务**: 提供状态更新、抽签逻辑、历史记录查询。
    *   **外部集成**: 对接天气和星座 API。
    *   **数据库**: MySQL (生产环境) / SQLite (开发环境)。

*   **本地监控**:
    *   提供 `monitor.py` 脚本，在本地电脑运行即可向服务器推送当前状态。

## 目录结构

*   `pages/`: 前端页面
*   `components/`: Vue 组件
*   `sleepy-status/`: 后端 Flask 应用
*   `local_client/`: 本地状态上报脚本
*   `auto_deploy.py`: 自动化部署脚本

## 快速开始

### 开发环境

1.  **前端**:
    ```bash
    npm install
    npm run dev
    ```

2.  **后端**:
    ```bash
    cd sleepy-status
    pip install -r requirements.txt
    python app.py
    ```

### 部署

详见 [DEPLOY.md](DEPLOY.md)

## 本地状态同步

想要让网页上的御守显示你的实时状态？

1.  **电脑端**: 运行 `local_client/monitor.py`。
2.  **手机端 (iOS/Android)**: 
    *   访问 `/admin/dashboard` 页面。
    *   或者使用 iOS 快捷指令 / Android HTTP Shortcuts。
    *   详见 [MOBILE_GUIDE.md](MOBILE_GUIDE.md)。
