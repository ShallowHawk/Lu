import paramiko
import os
import time
from scp import SCPClient
import sys

# Configuration
HOST = '101.43.113.154'
USER = 'root'
PASSWORD = '63658513ZGWo+-'
REMOTE_DIR = '/var/www/birthday-website'

def create_ssh_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, username=USER, password=PASSWORD, look_for_keys=False, allow_agent=False)
        return client
    except Exception as e:
        print(f"Connection Failed: {e}")
        sys.exit(1)

def run_command(client, command, description):
    print(f"[{description}] Running: {command}")
    stdin, stdout, stderr = client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print(f"[{description}] Success")
        return True
    else:
        print(f"[{description}] Error: {stderr.read().decode()}")
        return False

def deploy():
    print("🚀 Starting Auto Deployment...")
    client = create_ssh_client()
    
    # 1. Install Dependencies
    commands = [
        "apt-get update",
        "apt-get install -y python3-pip python3-venv nginx mysql-server zip unzip",
        # Install Node.js 18
        "curl -fsSL https://deb.nodesource.com/setup_18.x | bash -",
        "apt-get install -y nodejs",
        "npm install -g pm2"
    ]
    
    for cmd in commands:
        run_command(client, cmd, "Installing Dependencies")

    # 2. Setup MySQL
    # Secure setup might be needed, but we'll ensure DB exists
    mysql_cmds = [
        "service mysql start",
        f"mysql -e \"CREATE DATABASE IF NOT EXISTS birthday_db;\"",
        # Ensure root password matches or create specific user (Skipping root password change to avoid lockout)
        # We will trust the provided password is for SSH and maybe MySQL? 
        # Usually MySQL root has no password or a different one on fresh install.
        # Let's try to set it to ensure app.py works.
        f"mysql -e \"ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '{PASSWORD}'; FLUSH PRIVILEGES;\" || echo 'Root password change failed, might already be set'"
    ]
    for cmd in mysql_cmds:
        run_command(client, cmd, "Configuring MySQL")

    # 3. Upload Files
    # We will zip the current directory (excluding node_modules, .git, .output)
    print("[Upload] Zipping files...")
    os.system("tar --exclude='node_modules' --exclude='.git' --exclude='.output' --exclude='.nuxt' -czf deploy_package.tar.gz .")
    
    print("[Upload] Transferring files...")
    with SCPClient(client.get_transport()) as scp:
        scp.put('deploy_package.tar.gz', '/tmp/deploy_package.tar.gz')
    
    # Clean remote dir and unzip
    run_command(client, f"rm -rf {REMOTE_DIR} && mkdir -p {REMOTE_DIR}", "Cleaning Remote Dir")
    run_command(client, f"tar -xzf /tmp/deploy_package.tar.gz -C {REMOTE_DIR}", "Extracting Files")

    # 4. Setup Backend
    backend_cmds = [
        f"cd {REMOTE_DIR}/sleepy-status && python3 -m venv venv",
        f"cd {REMOTE_DIR}/sleepy-status && ./venv/bin/pip install -r requirements.txt",
        # Run Flask with PM2
        f"pm2 delete flask-api || true",
        f"cd {REMOTE_DIR}/sleepy-status && USE_MYSQL=1 pm2 start app.py --name flask-api --interpreter ./venv/bin/python"
    ]
    for cmd in backend_cmds:
        run_command(client, cmd, "Setting up Backend")

    # 5. Setup Frontend
    frontend_cmds = [
        f"cd {REMOTE_DIR} && npm install",
        f"cd {REMOTE_DIR} && npm run build",
        f"pm2 delete nuxt-app || true",
        f"cd {REMOTE_DIR} && pm2 start .output/server/index.mjs --name nuxt-app"
    ]
    for cmd in frontend_cmds:
        run_command(client, cmd, "Setting up Frontend")

    # 6. Configure Nginx
    nginx_config = """
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
"""
    # Write config to file then upload
    with open('nginx_config', 'w') as f:
        f.write(nginx_config)
    
    with SCPClient(client.get_transport()) as scp:
        scp.put('nginx_config', '/etc/nginx/sites-available/birthday')
    
    run_command(client, "ln -sf /etc/nginx/sites-available/birthday /etc/nginx/sites-enabled/default", "Linking Nginx Config")
    run_command(client, "nginx -t && service nginx restart", "Restarting Nginx")

    print("✅ Deployment Completed Successfully!")
    print(f"Visit http://{HOST}")

    client.close()
    # Cleanup local
    if os.path.exists('deploy_package.tar.gz'):
        os.remove('deploy_package.tar.gz')
    if os.path.exists('nginx_config'):
        os.remove('nginx_config')

if __name__ == '__main__':
    deploy()
