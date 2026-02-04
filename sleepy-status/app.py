from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid
import random
import glob
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据文件路径
DATA_FILE = 'data.json'
HISTORY_FILE = 'history.json'
PHOTOS_DIR = 'public/images'
PHOTOS_INFO_FILE = 'photos.json'
MESSAGES_FILE = 'messages.json'

# 允许上传的图片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# 配置上传限制
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 默认配置
DEFAULT_CONFIG = {
    "secret": "birthday2024",
    "status_list": {
        "1": {"name": "睡觉中", "desc": "正在做美梦zzz...", "color": "#9B59B6"},
        "2": {"name": "工作中", "desc": "正在努力工作", "color": "#3498DB"},
        "3": {"name": "运动中", "desc": "正在运动💪", "color": "#E74C3C"},
        "4": {"name": "看B站", "desc": "正在刷B站", "color": "#FF69B4"},
        "5": {"name": "玩游戏", "desc": "在游戏世界里", "color": "#F39C12"},
        "6": {"name": "听音乐", "desc": "正在享受音乐", "color": "#1ABC9C"},
        "7": {"name": "学习中", "desc": "在认真学习", "color": "#8E44AD"},
        "8": {"name": "做饭中", "desc": "在准备美食", "color": "#E67E22"},
        "9": {"name": "未知状态", "desc": "正在使用未知应用", "color": "#95A5A6"}
    },
    "users": {
        "木头": {
            "display_name": "木头",
            "current_status": "2",
            "last_update": None,
            "emoji": "🐰"
        },
        "乾雨": {
            "display_name": "乾雨", 
            "current_status": "2",
            "last_update": None,
            "emoji": "🌧️"
        }
    }
}

def load_data():
    """加载配置数据"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_data(data):
    """保存配置数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_history():
    """加载状态历史"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return []

def save_history(history):
    """保存状态历史"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_to_history(user_id, status_id, app_name=None):
    """添加状态到历史记录"""
    history = load_history()
    timestamp = datetime.now().isoformat()
    
    # 添加新记录
    record = {
        "user": user_id,
        "status": status_id,
        "timestamp": timestamp
    }
    
    # 如果有应用名信息，添加到记录中
    if app_name:
        record["app_name"] = app_name
    
    history.append(record)
    
    # 只保留最近100条记录（支持两个用户）
    if len(history) > 100:
        history = history[-100:]
    
    save_history(history)

def load_photos_info():
    """加载照片信息"""
    if os.path.exists(PHOTOS_INFO_FILE):
        try:
            with open(PHOTOS_INFO_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return []

def save_photos_info(photos_info):
    """保存照片信息"""
    with open(PHOTOS_INFO_FILE, 'w', encoding='utf-8') as f:
        json.dump(photos_info, f, ensure_ascii=False, indent=2)

def load_messages():
    """加载留言信息"""
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return []

def save_messages(messages):
    """保存留言信息"""
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file_path):
    """获取文件大小（以MB为单位）"""
    size_bytes = os.path.getsize(file_path)
    return round(size_bytes / (1024 * 1024), 2)

# 静态文件服务
@app.route('/public/images/<filename>')
def uploaded_file(filename):
    """提供上传的图片文件"""
    return send_from_directory(PHOTOS_DIR, filename)

@app.route('/')
def index():
    """主页"""
    return jsonify({
        "message": "林璐的状态监控服务",
        "version": "1.0.0",
        "endpoints": {
            "/query": "获取当前状态",
            "/get/status_list": "获取状态列表",
            "/set": "设置状态 (需要secret参数)",
            "/history": "获取状态历史",
            "/photos": "照片墙页面",
            "/api/photos": "获取照片列表",
            "/api/photos/upload": "上传照片",
            "/api/photos/delete": "删除照片",
            "/api/messages": "获取留言列表",
            "/api/messages/send": "发送留言",
            "/api/messages/delete": "删除留言"
        }
    })

@app.route('/query')
def query_status():
    """查询当前状态（支持单用户和多用户）"""
    user = request.args.get('user')  # 可选用户参数
    data = load_data()
    
    if user and user in data.get('users', {}):
        # 查询指定用户状态
        user_data = data['users'][user]
        current_status = user_data.get('current_status', '1')
        status_info = data['status_list'].get(current_status, {})
        
        return jsonify({
            "user": user,
            "display_name": user_data.get('display_name', user),
            "emoji": user_data.get('emoji', '👤'),
            "status": current_status,
            "name": status_info.get('name', '未知状态'),
            "description": status_info.get('desc', '暂无描述'),
            "color": status_info.get('color', '#000000'),
            "last_update": user_data.get('last_update'),
            "timestamp": datetime.now().isoformat()
        })
    else:
        # 返回所有用户状态
        users_status = {}
        for user_id, user_data in data.get('users', {}).items():
            current_status = user_data.get('current_status', '1')
            status_info = data['status_list'].get(current_status, {})
            
            users_status[user_id] = {
                "display_name": user_data.get('display_name', user_id),
                "emoji": user_data.get('emoji', '👤'),
                "status": current_status,
                "name": status_info.get('name', '未知状态'),
                "description": status_info.get('desc', '暂无描述'),
                "color": status_info.get('color', '#000000'),
                "last_update": user_data.get('last_update')
            }
        
        return jsonify({
            "users": users_status,
            "timestamp": datetime.now().isoformat()
        })

@app.route('/get/status_list')
def get_status_list():
    """获取所有状态列表"""
    data = load_data()
    return jsonify({
        "status_list": data['status_list'],
        "current": data.get('current_status', '1')
    })

@app.route('/set')
def set_status():
    """设置状态（支持多用户）"""
    secret = request.args.get('secret')
    status = request.args.get('status')
    user = request.args.get('user', '木头')  # 默认用户为木头
    app_name = request.args.get('app_name')  # 应用名（用于未知状态）
    
    if not secret or not status:
        return jsonify({
            "error": "缺少必要参数",
            "required": ["secret", "status"],
            "optional": ["user", "app_name"]
        }), 400
    
    data = load_data()
    
    # 验证密钥
    if secret != data.get('secret', 'birthday2024'):
        return jsonify({"error": "密钥错误"}), 403
    
    # 验证状态ID
    if status not in data['status_list']:
        return jsonify({
            "error": "无效的状态ID",
            "valid_status": list(data['status_list'].keys())
        }), 400
    
    # 验证用户ID
    if user not in data.get('users', {}):
        return jsonify({
            "error": "无效的用户ID",
            "valid_users": list(data.get('users', {}).keys())
        }), 400
    
    # 更新用户状态
    user_data = data['users'][user]
    old_status = user_data.get('current_status')
    user_data['current_status'] = status
    user_data['last_update'] = datetime.now().isoformat()
    
    save_data(data)
    
    # 添加到历史记录（仅当状态真正改变时）
    if old_status != status:
        add_to_history(user, status, app_name)
    
    status_info = data['status_list'][status]
    
    # 如果是未知状态且有应用名，添加应用名到描述中
    status_name = status_info['name']
    status_desc = status_info['desc']
    if status == '9' and app_name:
        status_name = f"{status_info['name']} ({app_name})"
        status_desc = f"{status_info['desc']} ({app_name})"
    
    return jsonify({
        "success": True,
        "message": "状态更新成功",
        "user": user,
        "display_name": user_data.get('display_name', user),
        "emoji": user_data.get('emoji', '👤'),
        "status": {
            "id": status,
            "name": status_name,
            "description": status_desc,
            "color": status_info['color']
        },
        "timestamp": user_data['last_update']
    })

@app.route('/history')
def get_history():
    """获取状态历史（支持多用户）"""
    user = request.args.get('user')  # 可选用户过滤
    history = load_history()
    data = load_data()
    
    # 过滤用户历史（如果指定了用户）
    if user:
        history = [item for item in history if item.get('user') == user]
    
    # 丰富历史数据
    enriched_history = []
    for item in history:
        status_info = data['status_list'].get(item['status'], {})
        user_id = item.get('user', '未知用户')
        user_data = data.get('users', {}).get(user_id, {})
        
        # 处理应用名信息
        status_name = status_info.get('name', '未知状态')
        status_desc = status_info.get('desc', '')
        app_name = item.get('app_name')
        
        if item['status'] == '9' and app_name:
            status_name = f"{status_name} ({app_name})"
            status_desc = f"{status_desc} ({app_name})"
        
        enriched_history.append({
            "user": user_id,
            "display_name": user_data.get('display_name', user_id),
            "emoji": user_data.get('emoji', '👤'),
            "status_id": item['status'],
            "name": status_name,
            "description": status_desc,
            "color": status_info.get('color', '#000000'),
            "timestamp": item['timestamp'],
            "app_name": app_name if app_name else None
        })
    
    return jsonify({
        "history": enriched_history[-30:],  # 返回最近30条
        "total": len(enriched_history),
        "filtered_user": user if user else "all"
    })

@app.route('/api/photos')
def get_photos():
    """获取照片列表"""
    photos_info = load_photos_info()
    config_data = load_data()
    
    # 检查文件是否真实存在，如果不存在则从列表中移除
    valid_photos = []
    for photo in photos_info:
        file_path = os.path.join(PHOTOS_DIR, photo['filename'])
        if os.path.exists(file_path):
            # 添加用户信息
            user_info = config_data.get('users', {}).get(photo['user'], {})
            photo_with_user_info = photo.copy()
            photo_with_user_info['user_info'] = user_info
            valid_photos.append(photo_with_user_info)
    
    # 如果有无效照片，更新照片信息文件
    if len(valid_photos) != len(photos_info):
        save_photos_info([p for p in photos_info if os.path.exists(os.path.join(PHOTOS_DIR, p['filename']))])
    
    # 按上传时间倒序排列
    valid_photos.sort(key=lambda x: x['upload_time'], reverse=True)
    
    return jsonify({
        "success": True,
        "photos": valid_photos,
        "total": len(valid_photos)
    })

@app.route('/api/photos/upload', methods=['POST'])
def upload_photo():
    """上传照片"""
    secret = request.form.get('secret')
    user = request.form.get('user', '木头')
    caption = request.form.get('caption', '')
    
    # 验证密钥
    data = load_data()
    if secret != data.get('secret', 'birthday2024'):
        return jsonify({"error": "密钥错误"}), 403
    
    # 检查用户是否存在
    if user not in data.get('users', {}):
        return jsonify({"error": "无效的用户"}), 400
    
    # 检查是否有文件
    if 'photo' not in request.files:
        return jsonify({"error": "没有选择文件"}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({"error": "没有选择文件"}), 400
    
    if file and allowed_file(file.filename):
        # 确保目录存在
        os.makedirs(PHOTOS_DIR, exist_ok=True)
        
        # 生成唯一文件名
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(PHOTOS_DIR, unique_filename)
        
        # 保存文件
        file.save(file_path)
        
        # 获取文件信息
        file_size = get_file_size(file_path)
        upload_time = datetime.now().isoformat()
        
        # 保存照片信息
        photos_info = load_photos_info()
        photo_info = {
            "id": str(uuid.uuid4()),
            "filename": unique_filename,
            "original_name": secure_filename(file.filename),
            "user": user,
            "caption": caption,
            "upload_time": upload_time,
            "file_size": file_size,
            "url": f"/public/images/{unique_filename}"
        }
        
        photos_info.append(photo_info)
        save_photos_info(photos_info)
        
        return jsonify({
            "success": True,
            "message": "照片上传成功",
            "photo": photo_info
        })
    else:
        return jsonify({"error": "不支持的文件格式"}), 400

@app.route('/api/photos/delete', methods=['POST'])
def delete_photo():
    """删除照片"""
    secret = request.form.get('secret') or request.json.get('secret')
    photo_id = request.form.get('photo_id') or request.json.get('photo_id')
    
    # 验证密钥
    data = load_data()
    if secret != data.get('secret', 'birthday2024'):
        return jsonify({"error": "密钥错误"}), 403
    
    if not photo_id:
        return jsonify({"error": "缺少照片ID"}), 400
    
    # 查找并删除照片
    photos_info = load_photos_info()
    photo_to_delete = None
    
    for i, photo in enumerate(photos_info):
        if photo['id'] == photo_id:
            photo_to_delete = photo
            photos_info.pop(i)
            break
    
    if not photo_to_delete:
        return jsonify({"error": "照片不存在"}), 404
    
    # 删除文件
    file_path = os.path.join(PHOTOS_DIR, photo_to_delete['filename'])
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # 保存更新后的照片信息
    save_photos_info(photos_info)
    
    return jsonify({
        "success": True,
        "message": "照片删除成功",
        "deleted_photo": photo_to_delete
    })

@app.route('/api/gallery')
def get_gallery():
    """获取public/images目录下的所有图片文件"""
    try:
        # 支持的图片格式
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.JPG', '*.JPEG', '*.PNG', '*.GIF', '*.WEBP']
        
        image_files = []
        for extension in image_extensions:
            pattern = os.path.join(PHOTOS_DIR, extension)
            image_files.extend(glob.glob(pattern))
        
        # 获取文件信息并随机排序
        gallery_images = []
        for file_path in image_files:
            filename = os.path.basename(file_path)
            file_size = round(os.path.getsize(file_path) / (1024 * 1024), 2)  # MB
            
            gallery_images.append({
                "filename": filename,
                "url": f"/public/images/{filename}",
                "size": file_size,
                "width": random.randint(200, 400),  # 随机宽度用于瀑布流
                "height": random.randint(200, 500)  # 随机高度用于瀑布流
            })
        
        # 随机打乱顺序
        random.shuffle(gallery_images)
        
        return jsonify({
            "success": True,
            "images": gallery_images,
            "total": len(gallery_images)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/messages')
def get_messages():
    """获取留言列表"""
    try:
        messages = load_messages()
        
        # 按时间倒序排列
        messages.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            "success": True,
            "messages": messages,
            "total": len(messages)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/messages/send', methods=['POST'])
def send_message():
    """发送留言"""
    try:
        # 支持JSON和表单数据
        if request.is_json:
            data = request.json
        else:
            data = request.form
        
        user = data.get('user', '匿名')
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"error": "留言内容不能为空"}), 400
        
        # 验证用户是否存在
        config_data = load_data()
        if user not in config_data.get('users', {}):
            return jsonify({"error": "无效的用户"}), 400
        
        # 创建留言记录
        message_record = {
            "id": str(uuid.uuid4()),
            "user": user,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "user_info": config_data['users'][user]
        }
        
        # 保存留言
        messages = load_messages()
        messages.append(message_record)
        
        # 只保留最近100条留言
        if len(messages) > 100:
            messages = messages[-100:]
        
        save_messages(messages)
        
        return jsonify({
            "success": True,
            "message": "留言发送成功",
            "data": message_record
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/messages/delete', methods=['POST'])
def delete_message():
    """删除留言"""
    try:
        # 支持JSON和表单数据
        if request.is_json:
            data = request.json
        else:
            data = request.form
        
        secret = data.get('secret')
        message_id = data.get('message_id')
        
        # 验证密钥
        config_data = load_data()
        if secret != config_data.get('secret', 'birthday2024'):
            return jsonify({"error": "密钥错误"}), 403
        
        if not message_id:
            return jsonify({"error": "缺少留言ID"}), 400
        
        # 查找并删除留言
        messages = load_messages()
        message_to_delete = None
        
        for i, message in enumerate(messages):
            if message['id'] == message_id:
                message_to_delete = message
                messages.pop(i)
                break
        
        if not message_to_delete:
            return jsonify({"error": "留言不存在"}), 404
        
        # 保存更新后的留言
        save_messages(messages)
        
        return jsonify({
            "success": True,
            "message": "留言删除成功",
            "deleted_message": message_to_delete
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/messages/update', methods=['POST'])
def update_message():
    """更新留言"""
    try:
        # 支持JSON和表单数据
        if request.is_json:
            data = request.json
        else:
            data = request.form
        
        secret = data.get('secret')
        message_id = data.get('message_id')
        new_message = data.get('message', '').strip()
        
        # 验证密钥
        config_data = load_data()
        if secret != config_data.get('secret', 'birthday2024'):
            return jsonify({"error": "密钥错误"}), 403
        
        if not message_id:
            return jsonify({"error": "缺少留言ID"}), 400
        
        if not new_message:
            return jsonify({"error": "留言内容不能为空"}), 400
        
        # 查找并更新留言
        messages = load_messages()
        message_to_update = None
        
        for i, message in enumerate(messages):
            if message['id'] == message_id:
                message_to_update = message
                messages[i]['message'] = new_message
                messages[i]['timestamp'] = datetime.now().isoformat()
                break
        
        if not message_to_update:
            return jsonify({"error": "留言不存在"}), 404
        
        # 保存更新后的留言
        save_messages(messages)
        
        return jsonify({
            "success": True,
            "message": "留言更新成功",
            "updated_message": messages[i]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/status_page')
def status_page():
    """双人状态展示页面"""
    data = load_data()
    users = data.get('users', {})
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>木头 & 乾雨 的状态</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                margin: 0; 
                padding: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            .header h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            .header p {
                font-size: 1.2rem;
                opacity: 0.8;
                margin: 0;
            }
            .status-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 30px;
                max-width: 1000px;
                margin: 0 auto;
                transition: opacity 0.5s ease;
            }
            .status-card {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 40px;
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }
            .status-card:hover {
                transform: translateY(-5px);
            }
            .user-info {
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
                gap: 10px;
            }
            .user-emoji {
                font-size: 2rem;
            }
            .user-name {
                font-size: 1.8rem;
                font-weight: 600;
            }
            .status-emoji { 
                font-size: 4rem; 
                margin-bottom: 20px; 
                animation: bounce 2s infinite;
            }
            .status-name { 
                font-size: 1.5rem; 
                margin-bottom: 10px; 
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }
            .status-desc { 
                font-size: 1rem; 
                opacity: 0.9; 
                margin-bottom: 20px; 
                line-height: 1.4;
            }
            .last-update { 
                font-size: 0.8rem; 
                opacity: 0.7; 
            }
            .indicator {
                width: 12px; 
                height: 12px; 
                border-radius: 50%;
                display: inline-block;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
                animation: pulse 2s infinite;
            }
            .offline {
                opacity: 0.6;
                filter: grayscale(50%);
            }
            .footer {
                text-align: center;
                margin-top: 40px;
                font-size: 0.9rem;
                opacity: 0.7;
            }
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                40% { transform: translateY(-10px); }
                60% { transform: translateY(-5px); }
            }
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7); }
                70% { box-shadow: 0 0 0 10px rgba(255, 255, 255, 0); }
                100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
            }
            @media (max-width: 768px) {
                .status-container {
                    grid-template-columns: 1fr;
                    gap: 20px;
                }
                .status-card {
                    padding: 30px 20px;
                }
                .header h1 {
                    font-size: 2rem;
                }
            }
        </style>
        <script>
            let galleryImages = [];
            let isLoading = false;
            
            // 获取图片库照片
            async function loadGallery() {
                try {
                    const response = await fetch('/api/gallery');
                    const data = await response.json();
                    if (data.success && data.images.length > 0) {
                        galleryImages = data.images;
                        return true;
                    }
                } catch (error) {
                    console.error('Load gallery error:', error);
                }
                return false;
            }
            
            // 显示瀑布流照片墙loading
            function showWaterfallLoading() {
                if (galleryImages.length === 0) return false;
                
                const container = document.querySelector('.status-container');
                isLoading = true;
                
                // 取前12张图片用于瀑布流
                const displayImages = galleryImages.slice(0, 12);
                
                container.innerHTML = `
                    <div style="text-align: center; margin-bottom: 30px;">
                        <div style="font-size: 1.8rem; margin-bottom: 10px; opacity: 0.9;">
                            🔄 正在加载状态信息...
                        </div>
                        <div style="font-size: 1rem; opacity: 0.7;">
                            ✨ 回忆时光 ✨
                        </div>
                    </div>
                    <div class="waterfall-container" style="columns: 3; column-gap: 20px; max-width: 900px; margin: 0 auto;">
                        ${displayImages.map((img, index) => `
                            <div class="waterfall-item" style="
                                break-inside: avoid;
                                margin-bottom: 20px;
                                background: rgba(255, 255, 255, 0.1);
                                backdrop-filter: blur(20px);
                                border-radius: 16px;
                                overflow: hidden;
                                border: 1px solid rgba(255, 255, 255, 0.2);
                                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                                opacity: 0;
                                animation: fadeInUp 0.6s ease forwards;
                                animation-delay: ${index * 0.1}s;
                            ">
                                <img src="${img.url}" alt="照片" 
                                     style="width: 100%; height: auto; display: block; transition: transform 0.3s ease;"
                                     onload="this.style.opacity='1'"
                                     onmouseover="this.style.transform='scale(1.05)'"
                                     onmouseout="this.style.transform='scale(1)'">
                            </div>
                        `).join('')}
                    </div>
                    <style>
                        @keyframes fadeInUp {
                            from {
                                opacity: 0;
                                transform: translateY(30px);
                            }
                            to {
                                opacity: 1;
                                transform: translateY(0);
                            }
                        }
                        
                        @media (max-width: 768px) {
                            .waterfall-container {
                                columns: 2 !important;
                                column-gap: 15px !important;
                            }
                        }
                        
                        @media (max-width: 480px) {
                            .waterfall-container {
                                columns: 1 !important;
                            }
                        }
                    </style>
                `;
                
                return true;
            }
            
            // 页面加载时先显示照片墙
            window.addEventListener('load', async () => {
                const hasImages = await loadGallery();
                
                if (hasImages) {
                    // 显示瀑布流照片墙loading
                    showWaterfallLoading();
                    
                    // 6秒后平滑过渡到正常内容
                    setTimeout(() => {
                        // 平滑过渡到正常内容
                        document.querySelector('.status-container').style.opacity = '0';
                        setTimeout(() => {
                            isLoading = false;
                            location.reload();
                        }, 500);
                    }, 6000);
                } else {
                    // 没有照片时直接显示正常内容
                    isLoading = false;
                }
            });
            
            // 每30秒刷新一次
            setTimeout(() => location.reload(), 30000);
        </script>
    </head>
    <body>
        <div class="header">
            <h1>🏠 状态监控中心</h1>
            <p>实时跟踪木头和乾雨的生活状态</p>
        </div>
        
        <div class="status-container">'''
    
    # 生成每个用户的状态卡片
    for user_id, user_data in users.items():
        current_status = user_data.get('current_status', '1')
        status_info = data['status_list'].get(current_status, {})
        last_update = user_data.get('last_update', '从未更新')
        
        # 判断是否在线（最近10分钟内有更新）
        is_online = True
        try:
            if last_update and last_update != '从未更新':
                from datetime import datetime, timedelta
                last_time = datetime.fromisoformat(last_update)
                if datetime.now() - last_time > timedelta(minutes=10):
                    is_online = False
        except:
            is_online = False
        
        offline_class = ' offline' if not is_online else ''
        
        html += f'''
            <div class="status-card{offline_class}">
                <div class="user-info">
                    <span class="user-emoji">{user_data.get('emoji', '👤')}</span>
                    <span class="user-name">{user_data.get('display_name', user_id)}</span>
                </div>
                <div class="status-emoji">
                    {get_emoji_by_status(current_status)}
                </div>
                <div class="status-name">
                    <span class="indicator" style="background: {status_info.get('color', '#000')};"></span>
                    {status_info.get('name', '未知状态')}
                </div>
                <div class="status-desc">
                    {status_info.get('desc', '暂无描述')}
                </div>
                <div class="last-update">
                    最后更新: {last_update if last_update != '从未更新' else '从未更新'}
                    {'🔴 离线' if not is_online else '🟢 在线'}
                </div>
            </div>'''
    
    html += '''
        </div>
        
        <div class="footer">
            <p>💡 页面每30秒自动刷新 | 🔄 数据实时同步</p>
            <p>🏠 <a href="/mobile" style="color: white; text-decoration: none;">移动端控制面板</a> | 📊 <a href="/history" style="color: white; text-decoration: none;">历史记录</a> | 📸 <a href="/photos" style="color: white; text-decoration: none;">照片墙</a></p>
        </div>
    </body>
    </html>
    '''
    return html

def get_emoji_by_status(status_id):
    """根据状态ID返回对应emoji"""
    emoji_map = {
        "1": "😴",
        "2": "💻", 
        "3": "🏃‍♀️",
        "4": "📱",
        "5": "🎮",
        "6": "🎵",
        "7": "📚",
        "8": "👩‍🍳",
        "9": "❓"
    }
    return emoji_map.get(status_id, "❓")

@app.route('/mobile')
def mobile_control():
    """手机端双人控制面板"""
    data = load_data()
    users = data.get('users', {})
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>木头 & 乾雨 状态控制中心</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: white;
                overflow-x: hidden;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px 0;
                transition: opacity 0.5s ease;
            }
            .header h1 {
                font-size: 1.8rem;
                font-weight: 600;
                margin-bottom: 20px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            .user-tabs {
                display: flex;
                justify-content: center;
                gap: 10px;
                margin-bottom: 30px;
            }
            .user-tab {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 25px;
                padding: 12px 24px;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 1rem;
            }
            .user-tab.active {
                background: rgba(255, 255, 255, 0.25);
                border: 2px solid rgba(255, 255, 255, 0.5);
                transform: scale(1.05);
            }
            .current-status {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 20px;
                margin-bottom: 30px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                text-align: center;
            }
            .current-emoji { font-size: 3rem; margin-bottom: 10px; }
            .current-name { font-size: 1.2rem; margin-bottom: 5px; font-weight: 500; }
            .current-desc { font-size: 0.9rem; opacity: 0.8; }
            .status-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-bottom: 30px;
            }
            .status-btn {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 20px 15px;
                text-align: center;
                color: white;
                text-decoration: none;
                transition: all 0.3s ease;
                cursor: pointer;
                min-height: 100px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }
            .status-btn:hover, .status-btn:active {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                background: rgba(255, 255, 255, 0.2);
            }
            .status-btn.active {
                background: rgba(255, 255, 255, 0.25);
                border: 2px solid rgba(255, 255, 255, 0.5);
                transform: scale(0.95);
            }
            .status-btn .emoji { font-size: 2rem; margin-bottom: 8px; }
            .status-btn .name { font-size: 0.9rem; font-weight: 500; margin-bottom: 3px; }
            .status-btn .desc { font-size: 0.7rem; opacity: 0.8; line-height: 1.2; }
            .secret-input {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 20px;
                text-align: center;
            }
            .secret-input input {
                background: transparent;
                border: none;
                color: white;
                font-size: 1rem;
                text-align: center;
                width: 100%;
                outline: none;
            }
            .secret-input input::placeholder { color: rgba(255,255,255,0.6); }
            .footer {
                text-align: center;
                margin-top: 30px;
                font-size: 0.8rem;
                opacity: 0.7;
            }
            .loading {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 20px;
                border-radius: 10px;
                display: none;
                z-index: 1000;
            }
            .toast {
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 15px 25px;
                border-radius: 25px;
                display: none;
                z-index: 1000;
                backdrop-filter: blur(20px);
            }
            @media (max-width: 480px) {
                .status-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
                .status-btn { padding: 15px 10px; min-height: 80px; }
                .status-btn .emoji { font-size: 1.5rem; }
                .status-btn .name { font-size: 0.8rem; }
                .status-btn .desc { font-size: 0.65rem; }
                .user-tabs { flex-direction: column; align-items: center; }
                .user-tab { margin-bottom: 10px; }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌟 状态控制中心</h1>
            
            <div class="user-tabs">'''
    
    # 生成用户选择标签
    first_user = True
    for user_id, user_data in users.items():
        active_class = ' active' if first_user else ''
        html += f'''
                <div class="user-tab{active_class}" onclick="selectUser('{user_id}')">
                    <span>{user_data.get('emoji', '👤')}</span>
                    <span>{user_data.get('display_name', user_id)}</span>
                </div>'''
        first_user = False
    
    html += '''
            </div>
            
            <div class="current-status">
                <div class="current-emoji" id="currentEmoji">💻</div>
                <div class="current-name" id="currentName">加载中...</div>
                <div class="current-desc" id="currentDesc">正在获取状态信息</div>
            </div>
        </div>

        <div class="secret-input">
            <input type="password" id="secretInput" placeholder="请输入密钥 (默认: birthday2024)" value="birthday2024">
        </div>

        <div class="status-grid">'''
    
    # 动态生成状态按钮
    for status_id, status_info in data['status_list'].items():
        html += f'''
            <div class="status-btn" onclick="setStatus('{status_id}')">
                <div class="emoji">{get_emoji_by_status(status_id)}</div>
                <div class="name">{status_info['name']}</div>
                <div class="desc">{status_info['desc']}</div>
            </div>'''
    
    html += '''
        </div>

        <div class="footer">
            <p>💡 点击状态按钮即可更新</p>
            <p>🔄 页面会自动刷新显示最新状态</p>
            <p>
                <a href="/status_page" style="color: white; text-decoration: none;">📊 状态页面</a> |
                <a href="/photos" style="color: white; text-decoration: none;">📸 照片墙</a> |
                <a href="/history" style="color: white; text-decoration: none;">📜 历史记录</a>
            </p>
        </div>

        <div class="loading" id="loading">
            <div>⏳ 正在更新状态...</div>
        </div>

        <div class="toast" id="toast"></div>

        <script>
            let currentUser = Object.keys(''' + str(list(users.keys())).replace("'", '"') + ''')[0] || "木头";
            let currentStatus = {};
            let photos = [];
            let currentPhotoIndex = 0;
            let photoInterval;
            
            function showLoading() {
                document.getElementById('loading').style.display = 'block';
            }
            
            function hideLoading() {
                document.getElementById('loading').style.display = 'none';
            }
            
            function showToast(message, isError = false) {
                const toast = document.getElementById('toast');
                toast.textContent = message;
                toast.style.background = isError ? 'rgba(220, 53, 69, 0.9)' : 'rgba(40, 167, 69, 0.9)';
                toast.style.display = 'block';
                
                setTimeout(() => {
                    toast.style.display = 'none';
                }, 3000);
            }
            
            function selectUser(userId) {
                // 更新用户选择
                currentUser = userId;
                
                // 更新标签状态
                document.querySelectorAll('.user-tab').forEach(tab => {
                    tab.classList.remove('active');
                });
                event.target.closest('.user-tab').classList.add('active');
                
                // 刷新当前状态显示
                refreshStatus();
            }
            
            async function refreshStatus() {
                try {
                    const response = await fetch(`/query?user=${currentUser}`);
                    const data = await response.json();
                    
                    if (data.user) {
                        currentStatus[currentUser] = data.status;
                        updateCurrentStatus(data.status, data);
                        updateActiveButton(data.status);
                    }
                } catch (error) {
                    console.error('Refresh status error:', error);
                }
            }
            
            async function setStatus(statusId) {
                if (statusId === currentStatus[currentUser]) {
                    showToast(`🤔 ${currentUser}当前已经是这个状态了`);
                    return;
                }
                
                const secret = document.getElementById('secretInput').value || 'birthday2024';
                
                showLoading();
                
                try {
                    const response = await fetch(`/set?secret=${encodeURIComponent(secret)}&status=${statusId}&user=${currentUser}`);
                    const data = await response.json();
                    
                    hideLoading();
                    
                    if (data.success) {
                        showToast(`✅ ${data.display_name}: ${data.status.name}`);
                        
                        // 更新UI
                        currentStatus[currentUser] = statusId;
                        updateCurrentStatus(statusId, data.status);
                        updateActiveButton(statusId);
                        
                        // 添加触觉反馈（iOS）
                        if (window.navigator && window.navigator.vibrate) {
                            window.navigator.vibrate(50);
                        }
                    } else {
                        showToast(`❌ ${data.error}`, true);
                    }
                } catch (error) {
                    hideLoading();
                    showToast('❌ 网络错误', true);
                    console.error('Error:', error);
                }
            }
            
            function updateCurrentStatus(statusId, statusInfo) {
                const emojiMap = {
                    "1": "😴", "2": "💻", "3": "🏃‍♀️", "4": "📱",
                    "5": "🎮", "6": "🎵", "7": "📚", "8": "👩‍🍳", "9": "❓"
                };
                
                document.getElementById('currentEmoji').textContent = emojiMap[statusId] || '❓';
                document.getElementById('currentName').textContent = statusInfo.name || statusInfo.status?.name || '未知状态';
                document.getElementById('currentDesc').textContent = statusInfo.description || statusInfo.status?.description || '暂无描述';
            }
            
            function updateActiveButton(statusId) {
                // 移除所有active类
                document.querySelectorAll('.status-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                
                // 为新按钮添加active类
                const buttons = document.querySelectorAll('.status-btn');
                buttons[parseInt(statusId) - 1]?.classList.add('active');
            }
            
            // 获取照片列表
            async function loadPhotos() {
                try {
                    const response = await fetch('/api/photos');
                    const data = await response.json();
                    if (data.success && data.photos.length > 0) {
                        photos = data.photos;
                        return true;
                    }
                } catch (error) {
                    console.error('Load photos error:', error);
                }
                return false;
            }
            
            // 显示照片墙loading
            function showPhotoWallLoading() {
                if (photos.length === 0) return false;
                
                const photo = photos[currentPhotoIndex];
                
                // 隐藏其他内容
                document.querySelector('.user-tabs').style.display = 'none';
                document.querySelector('.current-status').style.display = 'none';
                document.querySelector('.secret-input').style.display = 'none';
                document.querySelector('.status-grid').style.display = 'none';
                
                // 显示照片墙loading
                const container = document.querySelector('.header');
                container.innerHTML = `
                    <h1>🌟 状态控制中心</h1>
                    <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.2); margin: 20px 0;">
                        <div style="font-size: 1.2rem; margin-bottom: 15px; opacity: 0.9;">
                            🔄 正在加载控制面板...
                        </div>
                        <div style="position: relative; margin-bottom: 15px;">
                            <img src="${photo.url}" alt="${photo.caption || '照片'}" 
                                 style="width: 100%; max-width: 300px; height: 200px; object-fit: cover; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.3);">
                            <div style="position: absolute; bottom: 8px; left: 8px; right: 8px; background: rgba(0,0,0,0.7); color: white; padding: 8px; border-radius: 6px; font-size: 0.8rem;">
                                <div style="font-weight: 500; margin-bottom: 3px;">${getUserEmoji(photo.user)} ${getUserDisplayName(photo.user)}</div>
                                <div style="opacity: 0.8;">${photo.caption || '无描述'}</div>
                            </div>
                        </div>
                        <div style="font-size: 0.8rem; opacity: 0.7;">
                            照片 ${currentPhotoIndex + 1} / ${photos.length} · ${formatDate(photo.upload_time)}
                        </div>
                    </div>
                `;
                
                // 每2秒切换到下一张照片
                currentPhotoIndex = (currentPhotoIndex + 1) % photos.length;
                
                return true;
            }
            
            // 工具函数
            function getUserEmoji(userId) {
                const userMap = {"木头": "🐰", "乾雨": "🌧️"};
                return userMap[userId] || '👤';
            }
            
            function getUserDisplayName(userId) {
                const userMap = {"木头": "木头", "乾雨": "乾雨"};
                return userMap[userId] || userId;
            }
            
            function formatDate(dateString) {
                const date = new Date(dateString);
                return date.toLocaleString('zh-CN', {
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                });
            }
            
            // 页面加载完成后初始化
            window.addEventListener('load', async () => {
                const hasPhotos = await loadPhotos();
                
                if (hasPhotos) {
                    // 显示照片墙loading
                    showPhotoWallLoading();
                    
                    // 每2秒切换照片
                    photoInterval = setInterval(() => {
                        showPhotoWallLoading();
                    }, 2000);
                    
                    // 6秒后平滑过渡到正常内容
                    setTimeout(() => {
                        clearInterval(photoInterval);
                        // 平滑过渡到正常内容
                        document.querySelector('.header').style.opacity = '0';
                        setTimeout(() => {
                            location.reload();
                        }, 500);
                    }, 6000); // 显示3张照片后加载正常内容
                } else {
                    // 没有照片时直接显示正常内容
                    refreshStatus();
                }
                
                // PWA支持
                if ('serviceWorker' in navigator) {
                    navigator.serviceWorker.register('/static/sw.js').catch(() => {});
                }
            });
            
            // 每30秒自动刷新状态
            setInterval(refreshStatus, 30000);
        </script>
    </body>
    </html>
    '''
    return html

@app.route('/photos')
def photos_page():
    """照片墙页面"""
    data = load_data()
    users = data.get('users', {})
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>📸 照片墙</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: white;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px 0;
            }
            .header h1 {
                font-size: 2.2rem;
                font-weight: 600;
                margin-bottom: 10px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            .header p {
                font-size: 1rem;
                opacity: 0.8;
                margin-bottom: 20px;
            }
            .upload-section {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 25px;
                margin-bottom: 30px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
            .upload-form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            .form-group {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .form-group label {
                font-size: 0.9rem;
                font-weight: 500;
                opacity: 0.9;
            }
            .form-group input, .form-group select, .form-group textarea {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 12px 15px;
                color: white;
                font-size: 1rem;
                outline: none;
                transition: all 0.3s ease;
            }
            .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
                border-color: rgba(255, 255, 255, 0.5);
                background: rgba(255, 255, 255, 0.15);
            }
            .form-group input::placeholder, .form-group textarea::placeholder {
                color: rgba(255, 255, 255, 0.6);
            }
            .form-group input[type="file"] {
                padding: 8px;
                cursor: pointer;
            }
            .upload-btn {
                background: linear-gradient(45deg, #667eea, #764ba2);
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                color: white;
                font-size: 1rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }
            .upload-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            }
            .upload-btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            .photos-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .photo-card {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 16px;
                overflow: hidden;
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: all 0.3s ease;
                cursor: pointer;
                position: relative;
            }
            .photo-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
            }
            .photo-img {
                width: 100%;
                height: 200px;
                object-fit: cover;
                transition: transform 0.3s ease;
            }
            .photo-card:hover .photo-img {
                transform: scale(1.05);
            }
            .photo-info {
                padding: 15px;
            }
            .photo-user {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 10px;
                font-size: 0.9rem;
                opacity: 0.9;
            }
            .photo-caption {
                font-size: 0.95rem;
                line-height: 1.4;
                margin-bottom: 10px;
                min-height: 20px;
            }
            .photo-meta {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.8rem;
                opacity: 0.7;
            }
            .photo-time {
                font-size: 0.8rem;
                opacity: 0.7;
            }
            .delete-btn {
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(220, 53, 69, 0.8);
                border: none;
                border-radius: 50%;
                width: 32px;
                height: 32px;
                color: white;
                font-size: 1.2rem;
                cursor: pointer;
                display: none;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }
            .photo-card:hover .delete-btn {
                display: flex;
            }
            .delete-btn:hover {
                background: rgba(220, 53, 69, 1);
                transform: scale(1.1);
            }
            .modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.9);
                backdrop-filter: blur(10px);
            }
            .modal-content {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                max-width: 90%;
                max-height: 90%;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .modal-img {
                width: 100%;
                height: auto;
                max-height: 70vh;
                object-fit: contain;
                border-radius: 12px;
                margin-bottom: 15px;
            }
            .modal-info {
                text-align: center;
                color: white;
            }
            .modal-close {
                position: absolute;
                top: 15px;
                right: 20px;
                background: none;
                border: none;
                color: white;
                font-size: 2rem;
                cursor: pointer;
                padding: 5px;
                line-height: 1;
            }
            .empty-state {
                text-align: center;
                padding: 60px 20px;
                opacity: 0.8;
            }
            .empty-state .emoji {
                font-size: 4rem;
                margin-bottom: 20px;
            }
            .empty-state h3 {
                font-size: 1.5rem;
                margin-bottom: 10px;
            }
            .empty-state p {
                font-size: 1rem;
                opacity: 0.7;
            }
            .loading {
                text-align: center;
                padding: 40px;
                font-size: 1.2rem;
                opacity: 0.8;
            }
            .toast {
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 15px 25px;
                border-radius: 25px;
                display: none;
                z-index: 1000;
                backdrop-filter: blur(20px);
            }
            .footer {
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                font-size: 0.9rem;
                opacity: 0.7;
            }
            .footer a {
                color: white;
                text-decoration: none;
                margin: 0 10px;
            }
            .footer a:hover {
                text-decoration: underline;
            }
            @media (max-width: 768px) {
                .photos-grid {
                    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                    gap: 15px;
                }
                .upload-section {
                    margin-bottom: 20px;
                    padding: 20px;
                }
                .header h1 {
                    font-size: 1.8rem;
                }
                .modal-content {
                    padding: 15px;
                }
            }
            @media (max-width: 480px) {
                .photos-grid {
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                    gap: 12px;
                }
                .upload-section {
                    padding: 15px;
                }
                .header h1 {
                    font-size: 1.6rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📸 照片墙</h1>
            <p>记录美好时光的地方</p>
        </div>

        <div class="upload-section">
            <form class="upload-form" id="uploadForm" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="userSelect">上传用户</label>
                    <select id="userSelect" name="user" required>'''
    
    # 添加用户选项
    for user_id, user_data in users.items():
        html += f'''
                        <option value="{user_id}">{user_data.get('emoji', '👤')} {user_data.get('display_name', user_id)}</option>'''
    
    html += '''
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="photoFile">选择照片</label>
                    <input type="file" id="photoFile" name="photo" accept="image/*" required>
                </div>
                
                <div class="form-group">
                    <label for="caption">照片描述 (可选)</label>
                    <textarea id="caption" name="caption" placeholder="说点什么..." rows="3"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="secret">密钥</label>
                    <input type="password" id="secret" name="secret" placeholder="请输入密钥" value="birthday2024" required>
                </div>
                
                <button type="submit" class="upload-btn" id="uploadBtn">
                    📤 上传照片
                </button>
            </form>
        </div>

        <div id="photosContainer">
            <div class="loading">
                🔄 正在加载照片...
            </div>
        </div>

        <div class="modal" id="photoModal">
            <div class="modal-content">
                <button class="modal-close" onclick="closeModal()">&times;</button>
                <img class="modal-img" id="modalImg" src="" alt="">
                <div class="modal-info">
                    <div id="modalCaption"></div>
                    <div id="modalUser"></div>
                    <div id="modalTime"></div>
                </div>
            </div>
        </div>

        <div class="toast" id="toast"></div>

        <div class="footer">
            <p>💡 点击照片可以放大查看</p>
            <p>
                <a href="/status_page">📊 状态页面</a>
                <a href="/mobile">📱 控制面板</a>
                <a href="/history">📜 历史记录</a>
            </p>
        </div>

        <script>
            let photos = [];
            let currentUser = Object.keys(''' + str(list(users.keys())).replace("'", '"') + ''')[0] || "木头";
            
            function showToast(message, isError = false) {
                const toast = document.getElementById('toast');
                toast.textContent = message;
                toast.style.background = isError ? 'rgba(220, 53, 69, 0.9)' : 'rgba(40, 167, 69, 0.9)';
                toast.style.display = 'block';
                
                setTimeout(() => {
                    toast.style.display = 'none';
                }, 3000);
            }
            
            function formatDate(dateString) {
                const date = new Date(dateString);
                return date.toLocaleString('zh-CN', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                });
            }
            
            function getUserEmoji(userId) {
                const userMap = ''' + str(dict((k, v.get('emoji', '👤')) for k, v in users.items())).replace("'", '"') + ''';
                return userMap[userId] || '👤';
            }
            
            function getUserDisplayName(userId) {
                const userMap = ''' + str(dict((k, v.get('display_name', k)) for k, v in users.items())).replace("'", '"') + ''';
                return userMap[userId] || userId;
            }
            
            async function loadPhotos() {
                try {
                    const response = await fetch('/api/photos');
                    const data = await response.json();
                    
                    if (data.success) {
                        photos = data.photos;
                        renderPhotos();
                    } else {
                        showToast('加载照片失败', true);
                    }
                } catch (error) {
                    console.error('Load photos error:', error);
                    showToast('网络错误', true);
                }
            }
            
            function renderPhotos() {
                const container = document.getElementById('photosContainer');
                
                if (photos.length === 0) {
                    container.innerHTML = `
                        <div class="empty-state">
                            <div class="emoji">📷</div>
                            <h3>还没有照片</h3>
                            <p>上传第一张照片来开始记录美好时光吧！</p>
                        </div>
                    `;
                    return;
                }
                
                let html = '<div class="photos-grid">';
                
                photos.forEach(photo => {
                    html += `
                        <div class="photo-card" onclick="openModal('${photo.id}')">
                            <button class="delete-btn" onclick="deletePhoto('${photo.id}', event)" title="删除照片">🗑️</button>
                            <img class="photo-img" src="${photo.url}" alt="${photo.caption || '照片'}" loading="lazy">
                            <div class="photo-info">
                                <div class="photo-user">
                                    <span>${getUserEmoji(photo.user)}</span>
                                    <span>${getUserDisplayName(photo.user)}</span>
                                </div>
                                <div class="photo-caption">${photo.caption || ''}</div>
                                <div class="photo-meta">
                                    <span class="photo-time">${formatDate(photo.upload_time)}</span>
                                    <span>${photo.file_size}MB</span>
                                </div>
                            </div>
                        </div>
                    `;
                });
                
                html += '</div>';
                container.innerHTML = html;
            }
            
            function openModal(photoId) {
                const photo = photos.find(p => p.id === photoId);
                if (!photo) return;
                
                const modal = document.getElementById('photoModal');
                const modalImg = document.getElementById('modalImg');
                const modalCaption = document.getElementById('modalCaption');
                const modalUser = document.getElementById('modalUser');
                const modalTime = document.getElementById('modalTime');
                
                modalImg.src = photo.url;
                modalCaption.textContent = photo.caption || '无描述';
                modalUser.textContent = `${getUserEmoji(photo.user)} ${getUserDisplayName(photo.user)}`;
                modalTime.textContent = formatDate(photo.upload_time);
                
                modal.style.display = 'block';
                
                // 阻止背景滚动
                document.body.style.overflow = 'hidden';
            }
            
            function closeModal() {
                const modal = document.getElementById('photoModal');
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
            
            async function deletePhoto(photoId, event) {
                event.stopPropagation();
                
                if (!confirm('确定要删除这张照片吗？')) {
                    return;
                }
                
                const secret = document.getElementById('secret').value;
                
                try {
                    const response = await fetch('/api/photos/delete', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            photo_id: photoId,
                            secret: secret
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        showToast('照片删除成功');
                        // 从本地数组中移除
                        photos = photos.filter(p => p.id !== photoId);
                        renderPhotos();
                    } else {
                        showToast(`删除失败: ${data.error}`, true);
                    }
                } catch (error) {
                    console.error('Delete photo error:', error);
                    showToast('网络错误', true);
                }
            }
            
            // 表单提交处理
            document.getElementById('uploadForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const uploadBtn = document.getElementById('uploadBtn');
                const originalText = uploadBtn.textContent;
                
                uploadBtn.disabled = true;
                uploadBtn.textContent = '📤 上传中...';
                
                const formData = new FormData(this);
                
                try {
                    const response = await fetch('/api/photos/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        showToast('照片上传成功！');
                        
                        // 添加到本地数组开头
                        photos.unshift(data.photo);
                        renderPhotos();
                        
                        // 清空表单
                        document.getElementById('photoFile').value = '';
                        document.getElementById('caption').value = '';
                    } else {
                        showToast(`上传失败: ${data.error}`, true);
                    }
                } catch (error) {
                    console.error('Upload error:', error);
                    showToast('网络错误', true);
                } finally {
                    uploadBtn.disabled = false;
                    uploadBtn.textContent = originalText;
                }
            });
            
            // 点击模态框背景关闭
            document.getElementById('photoModal').addEventListener('click', function(e) {
                if (e.target === this) {
                    closeModal();
                }
            });
            
            // ESC键关闭模态框
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeModal();
                }
            });
            
            // 页面加载完成后加载照片
            window.addEventListener('load', () => {
                loadPhotos();
            });
        </script>
    </body>
    </html>
    '''
    return html

if __name__ == '__main__':
    # 确保数据文件存在
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_CONFIG)
    
    print("🚀 林璐的状态监控服务启动中...")
    print("📍 访问地址: http://127.0.0.1:5000")
    print("📊 状态页面: http://127.0.0.1:5000/status_page")
    print("📱 控制面板: http://127.0.0.1:5000/mobile")
    print("📸 照片墙: http://127.0.0.1:5000/photos")
    print("🔗 API文档: http://127.0.0.1:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)