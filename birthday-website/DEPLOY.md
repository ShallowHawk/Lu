# 部署指南

本指南将帮助你将网站部署到 Linux 服务器 (Ubuntu/Debian)。

## 准备工作

1.  **服务器**: 一台拥有公网 IP 的 Linux 服务器 (如腾讯云/阿里云)。
2.  **域名**: (可选) 解析到服务器 IP。
3.  **环境**: 确保服务器已安装 `git`, `python3`, `npm` (脚本会自动处理大部分)。

## 自动化部署 (推荐)

我已为你编写了 `auto_deploy.py` 脚本，可以一键完成部署。

### 1. 修改配置
打开 `auto_deploy.py`，确认服务器信息：
```python
HOST = '101.43.113.154'  # 你的服务器IP
USER = 'root'            # 用户名
PASSWORD = '...'         # 密码
```

### 2. 运行脚本
在本地项目根目录下运行：
```bash
python auto_deploy.py
```
*注意：如果遇到 SSH 连接失败，可能是服务器禁用了密码登录。请尝试使用 SSH Key 或手动部署。*

## 手动部署 (如果自动部署失败)

### 1. 连接服务器
```bash
ssh root@101.43.113.154
```

### 2. 安装依赖
```bash
# 更新源
apt-get update

# 安装基础软件
apt-get install -y python3-pip python3-venv nginx mysql-server zip unzip

# 安装 Node.js (v18)
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# 安装 PM2 (进程管理)
npm install -g pm2
```

### 3. 配置 MySQL
```bash
service mysql start
mysql -u root -p
# 在 MySQL 命令行中：
CREATE DATABASE birthday_db;
exit;
```

### 4. 上传代码
你可以使用 SFTP 或 Git 将代码上传到 `/var/www/birthday-website`。

### 5. 启动后端
```bash
cd /var/www/birthday-website/sleepy-status
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# 启动 (使用环境变量连接 MySQL)
export USE_MYSQL=1
export DB_PASSWORD='你的数据库密码'
pm2 start app.py --name flask-api --interpreter ./venv/bin/python
```

### 6. 启动前端
```bash
cd /var/www/birthday-website
npm install
npm run build
pm2 start .output/server/index.mjs --name nuxt-app
```

### 7. 配置 Nginx 反向代理
编辑 `/etc/nginx/sites-available/birthday`：
```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:3000;
        # ... 其他 proxy_set_header 配置
    }

    location /api {
        proxy_pass http://localhost:5000;
        # ... 其他 proxy_set_header 配置
    }
}
```
启用并重启 Nginx：
```bash
ln -s /etc/nginx/sites-available/birthday /etc/nginx/sites-enabled/
nginx -t
service nginx restart
```

## 常见问题

*   **数据库连接失败**: 检查 `DB_PASSWORD` 环境变量是否正确。
*   **端口被占用**: 检查 3000 和 5000 端口。
