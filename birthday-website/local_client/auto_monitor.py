import time
import requests
import psutil
import win32gui
import win32process
import win32api
import os

# --- 配置区域 ---
SERVER_URL = "https://wildmutou.art/api/status/update" # 替换为你的服务器IP/域名
SECRET = "my_love_secret_2024"
USER_KEY = "mutou"

# 状态映射配置 (进程名关键词 -> 状态)
APP_RULES = {
    "code": ("勤勉", "正在写代码改变世界..."),
    "idea": ("勤勉", "Java 是世界上最好的语言"),
    "pycharm": ("勤勉", "Python 使得"),
    "webstorm": ("勤勉", "正在写前端"),
    "cursor": ("勤勉", "AI 辅助编程中"),
    "chrome": ("摸鱼", "网上冲浪中..."),
    "firefox": ("摸鱼", "网上冲浪中..."),
    "edge": ("摸鱼", "网上冲浪中..."),
    "cloudmusic": ("听歌", "网易云音乐"),
    "qqmusic": ("听歌", "QQ音乐"),
    "spotify": ("听歌", "Spotify"),
    "potplayer": ("看剧", "正在看视频"),
    "vlc": ("看剧", "正在看视频"),
    "steam": ("游戏", "Steam启动！"),
    "league of legends": ("游戏", "LOL中，回复不及时"),
    "genshin": ("游戏", "原神，启动！"),
    "wechat": ("聊天", "微信摸鱼中"),
    "dingtalk": ("搬砖", "为了我们以后更好的生活"),
    "feishu": ("搬砖", "为了我们以后更好的生活"),
}

# 闲置判定时间 (秒)
IDLE_THRESHOLD = 300 # 5分钟无操作视为发呆/休息

# --- 核心逻辑 ---

def get_active_window_process():
    try:
        # 获取当前活动窗口句柄
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd: return None
        
        # 获取窗口标题
        window_title = win32gui.GetWindowText(hwnd)
        
        # 获取进程ID
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        try:
            process = psutil.Process(pid)
            process_name = process.name().lower()
            return process_name, window_title
        except psutil.NoSuchProcess:
            return None, window_title
    except Exception as e:
        # print(f"Error getting window: {e}")
        return None, None

def get_idle_duration():
    try:
        # 获取系统最后一次输入时间
        last_input_info = win32api.GetLastInputInfo()
        # 系统启动以来的毫秒数
        tick_count = win32api.GetTickCount()
        
        idle_ms = tick_count - last_input_info
        return idle_ms / 1000.0 # 转换为秒
    except Exception:
        return 0

def update_status(name, description):
    try:
        # 简单防抖：如果状态没变就不发送请求 (这里简化处理，实际可以加本地缓存对比)
        # 为了演示，我们每次打印，实际请求可以加判断
        
        data = {
            "secret": SECRET,
            "user_key": USER_KEY,
            "name": name,
            "description": description,
            "is_online": True
        }
        res = requests.post(SERVER_URL, json=data, timeout=5)
        if res.status_code == 200:
            print(f"[{time.strftime('%H:%M:%S')}] 同步成功: {name} - {description}")
        else:
            print(f"同步失败: {res.text}")
    except Exception as e:
        print(f"网络异常: {e}")

def main():
    print("🚀 自动状态监控已启动...")
    print(f"目标服务器: {SERVER_URL}")
    print("正在监听活动窗口和键盘鼠标操作...")
    
    last_status_key = None
    
    while True:
        try:
            # 1. 检测闲置
            idle_seconds = get_idle_duration()
            if idle_seconds > IDLE_THRESHOLD:
                # 闲置超过阈值，不发送任何状态，让服务器自动判定超时进入 "想你" 状态
                # 或者发送一个 "Idle" 状态 (如果需要显示离开多久)
                # 根据需求：用户希望超时后自动变为"想你"
                # 所以这里我们停止发送更新即可，或者发送心跳但标记为idle?
                # 简单做法：停止发送，让服务器timeout
                if last_status_key != "idle_silent":
                    print(f"[{time.strftime('%H:%M:%S')}] 进入闲置模式，停止推送状态...")
                    last_status_key = "idle_silent"
                
                time.sleep(60) # 闲置时大幅降低检测频率
                continue

            # 2. 检测活动窗口
            proc_name, win_title = get_active_window_process()
            
            current_status = None
            
            if proc_name:
                # 遍历规则匹配
                for key, (name, desc) in APP_RULES.items():
                    if key in proc_name:
                        # 特殊处理：浏览器看视频检测 (通过标题)
                        if key in ['chrome', 'edge', 'firefox']:
                            title_lower = win_title.lower()
                            if 'bilibili' in title_lower or 'youtube' in title_lower:
                                current_status = ("看B站", f"正在看: {win_title[:15]}...")
                            else:
                                current_status = (name, desc)
                        else:
                            current_status = (name, desc)
                        break
            
            # 默认状态
            if not current_status:
                current_status = ("在线", "正在电脑前发呆")
            
            # 3. 状态变更时推送
            # 构造一个简单的key用于对比是否变化 (name + desc)
            status_key = f"{current_status[0]}_{current_status[1]}"
            
            if status_key != last_status_key:
                update_status(current_status[0], current_status[1])
                last_status_key = status_key
            
            time.sleep(5) # 每5秒检测一次
            
        except KeyboardInterrupt:
            print("\n监控已停止")
            break
        except Exception as e:
            print(f"运行出错: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
