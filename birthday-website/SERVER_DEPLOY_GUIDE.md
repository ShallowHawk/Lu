# 🚀 服务器端 AI 部署操作指南

**致服务器端的 AI 助手：**
你好！请严格按照以下步骤协助用户完成网站的更新部署。我们需要更新前端代码、后端接口以及数据库结构。

---

## 📋 步骤清单

### 第一步：拉取最新代码
请进入项目的根目录（通常是 `birthday-website`），执行 Git 拉取操作。

```bash
# 1. 进入项目目录 (请根据实际路径调整)
cd /path/to/birthday-website

# 2. 拉取最新代码
git pull origin main
```

> **检查点**：确保输出显示 "Already up to date." 或拉取了若干文件（特别是 `app.py`, `home.vue`, `DynamicTimeline.vue` 等）。如果遇到冲突，请优先保留远程仓库的版本（`git reset --hard origin/main`）。

---

### 第二步：更新并重启后端 (Python/Flask)
后端新增了 `Status` 模型和 `Message` 接口，必须重启才能生效。

```bash
# 1. 进入后端目录
cd sleepy-status

# 2. 安装可能缺失的依赖 (可选，防止报错)
pip install -r requirements.txt
# 或者如果没有 requirements.txt，确保安装了 flask-cors, requests
pip install flask-cors requests

# 3. 查找并杀死旧的 Python 进程
# 注意：这会杀死所有名为 app.py 的 python 进程，请谨慎操作
pkill -f "python app.py" 
# 或者手动查找 PID: ps aux | grep app.py

# 4. 后台启动新服务
# 建议使用 nohup 或 systemctl (如果有配置)
nohup python app.py > app.log 2>&1 &

# 5. 验证后端是否启动成功
curl -I http://localhost:5000/api/status/latest
```

> **检查点**：`curl` 命令应该返回 `HTTP/1.1 200 OK`。如果返回 Connection refused，请检查 `app.log` 看是否有报错。

---

### 第三步：更新并构建前端 (Nuxt)
前端新增了“卷轴公告”、“刮刮卡”和“防未登录跳转”功能，必须重新构建。

```bash
# 1. 回到项目根目录
cd ..

# 2. 安装新依赖 (如果有)
npm install

# 3. 执行构建
npm run build

# 4. 重启前端服务
# 如果是使用 PM2 管理 (推荐):
pm2 restart all
# 或者根据实际服务名: pm2 restart birthday-web

# 如果没有 PM2，是直接运行的:
# pkill -f "nuxt"
# nohup npm run start > nuxt.log 2>&1 &
```

> **检查点**：访问 `http://localhost:3000` (或你的服务器域名)，应该能看到最新的页面。如果未登录直接访问 `/home`，应该会被强制弹回登录页。

---

## 🛠️ 故障排查 (Troubleshooting)

1.  **留言板无法发送 / 报错 404**：
    *   **原因**：后端 `app.py` 没有重启，还在运行旧代码。
    *   **解决**：请务必执行 **第二步** 中的重启操作。

2.  **图片不显示 / 卷轴没出来**：
    *   **原因**：`git pull` 没有拉下来新图片，或者前端没有重新 `npm run build`。
    *   **解决**：检查 `public/images` 目录下是否有 `2023_02_14...` 开头的图片。如果没有，重新 git pull。

3.  **状态一直显示“未知”**：
    *   **原因**：数据库可能需要重新初始化。
    *   **解决**：重启后端时，代码里的 `init_db()` 会自动运行。如果还不行，尝试删除 `birthday.db` (如果是 SQLite) 让它重建。

---

**任务完成！请通知用户尝试访问网站测试。**
