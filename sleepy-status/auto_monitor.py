#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动状态监控脚本
监控桌面应用程序并自动更新状态
"""

import time
import requests
import json
import os
from datetime import datetime, timedelta
import psutil

# Windows特有的库
try:
    import win32gui
    import win32process
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False
    print("警告: 无法导入Windows相关库，某些功能可能不可用")

class StatusMonitor:
    def __init__(self, server_url="http://101.43.113.154:5000", secret="birthday2024", user="木头"):
        self.server_url = server_url
        self.secret = secret
        self.user = user
        self.last_status = None
        self.check_interval = 30  # 30秒检查一次
        
        # 活动检测相关
        self.last_activity_time = datetime.now()
        self.last_active_window = None
        self.last_mouse_pos = None
        self.sleep_timeout = 60  # 60分钟（1小时）无活动判断为睡觉
        
        # 应用程序到状态的映射
        self.app_status_map = {
            # 工作相关
            'code.exe': '2',  # VS Code -> 工作中
            'devenv.exe': '2',  # Visual Studio -> 工作中
            'pycharm64.exe': '2',  # PyCharm -> 工作中
            'idea64.exe': '2',  # IntelliJ IDEA -> 工作中
            'notepad++.exe': '2',  # Notepad++ -> 工作中
            'cursor.exe': '2',  # Cursor -> 工作中
            
            # 通信相关（默认为工作中）
            'wechatappex.exe': '2',  # 微信 -> 工作中
            'wechat.exe': '2',  # 微信 -> 工作中
            'qq.exe': '2',  # QQ -> 工作中
            'dingtalk.exe': '2',  # 钉钉 -> 工作中
            'tencent.exe': '2',  # 腾讯会议 -> 工作中
            'zoom.exe': '2',  # Zoom -> 工作中
            'teams.exe': '2',  # Microsoft Teams -> 工作中
            'slack.exe': '2',  # Slack -> 工作中
            'discord.exe': '2',  # Discord -> 工作中
            
            # 游戏相关
            'steam.exe': '5',  # Steam -> 玩游戏
            'genshinimpact.exe': '5',  # 原神 -> 玩游戏
            'leagueoflegends.exe': '5',  # 英雄联盟 -> 玩游戏
            'wow.exe': '5',  # 魔兽世界 -> 玩游戏
            'minecraft.exe': '5',  # 我的世界 -> 玩游戏
            
            # 音乐相关
            'cloudmusic.exe': '6',  # 网易云音乐 -> 听音乐
            'spotify.exe': '6',  # Spotify -> 听音乐
            'qqmusic.exe': '6',  # QQ音乐 -> 听音乐
            
            # 视频相关
            'bilibilidesktop.exe': '4',  # B站桌面版 -> 看B站
            'potplayer.exe': '4',  # PotPlayer -> 看B站/视频
            'vlc.exe': '4',  # VLC -> 看视频
            
            # 学习相关
            'anki.exe': '7',  # Anki -> 学习中
            'obsidian.exe': '7',  # Obsidian -> 学习中
            'notion.exe': '7',  # Notion -> 学习中
            'typora.exe': '7',  # Typora -> 学习中
            
            # 浏览器特殊处理（需要检查标题）
            'chrome.exe': self._check_browser_activity,
            'firefox.exe': self._check_browser_activity,
            'edge.exe': self._check_browser_activity,
            'brave.exe': self._check_browser_activity,
        }
        
        # 工作时间段（用于默认状态判断）
        self.work_hours = (9, 18)  # 9-18点工作时间
    
    def get_mouse_position(self):
        """获取鼠标位置"""
        if not WINDOWS_AVAILABLE:
            return None
            
        try:
            import win32gui
            return win32gui.GetCursorPos()
        except Exception:
            return None
    
    def check_user_activity(self):
        """检查用户活动"""
        current_time = datetime.now()
        has_activity = False
        
        # 检查窗口变化
        process_name, window_title = self.get_active_window_info()
        current_window = f"{process_name}:{window_title}" if process_name else None
        
        if current_window != self.last_active_window:
            has_activity = True
            self.last_active_window = current_window
        
        # 检查鼠标位置变化
        current_mouse_pos = self.get_mouse_position()
        if current_mouse_pos and current_mouse_pos != self.last_mouse_pos:
            has_activity = True
            self.last_mouse_pos = current_mouse_pos
        
        # 检查系统资源使用情况 - 如果CPU或内存使用率较高，认为系统活跃
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_percent = psutil.virtual_memory().percent
            
            # 如果CPU使用率超过30%或内存使用率超过70%，认为系统活跃
            if cpu_percent > 30 or memory_percent > 70:
                has_activity = True
        except Exception:
            pass
        
        # 检查网络活动
        try:
            net_io = psutil.net_io_counters()
            if hasattr(self, 'last_net_io'):
                # 如果有网络传输，认为系统活跃
                if (net_io.bytes_sent != self.last_net_io.bytes_sent or 
                    net_io.bytes_recv != self.last_net_io.bytes_recv):
                    has_activity = True
            self.last_net_io = net_io
        except Exception:
            pass
        
        # 特殊处理：如果当前正在进行明确的活动（如看视频、游戏等），延长活动时间
        if process_name and process_name in self.app_status_map:
            status_or_func = self.app_status_map[process_name]
            
            if callable(status_or_func):
                # 浏览器检查
                detected_status = status_or_func(window_title or '')
                if detected_status in ['4', '5', '6', '7']:  # 看B站、游戏、音乐、学习
                    has_activity = True
            elif status_or_func in ['4', '5', '6', '7']:  # 看B站、游戏、音乐、学习
                has_activity = True
        
        # 如果有活动，更新最后活动时间
        if has_activity:
            self.last_activity_time = current_time
            
        return has_activity
    
    def is_sleeping(self):
        """判断是否应该标记为睡觉"""
        current_time = datetime.now()
        time_since_last_activity = current_time - self.last_activity_time
        
        # 基本时间检查：必须超过1小时无活动
        if time_since_last_activity <= timedelta(minutes=self.sleep_timeout):
            return False
        
        # 检查当前是否有明确的活动应用
        process_name, window_title = self.get_active_window_info()
        if process_name:
            # 如果有明确的活动应用，不判断为睡觉
            if process_name in self.app_status_map:
                status_or_func = self.app_status_map[process_name]
                
                if callable(status_or_func):
                    # 浏览器检查
                    detected_status = status_or_func(window_title or '')
                    if detected_status in ['2', '4', '5', '6', '7', '8']:  # 任何非睡觉状态
                        return False
                else:
                    # 直接状态映射，且不是睡觉状态
                    if status_or_func != '1':
                        return False
        
        # 额外检查：如果系统仍然活跃，不判断为睡觉
        try:
            # 检查是否有媒体播放相关进程
            media_processes = ['vlc.exe', 'potplayer.exe', 'wmplayer.exe', 'spotify.exe', 'cloudmusic.exe']
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() in media_processes:
                    return False
            
            # 检查浏览器是否在播放媒体
            browser_processes = ['chrome.exe', 'firefox.exe', 'edge.exe', 'brave.exe']
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() in browser_processes:
                    # 如果浏览器进程的CPU使用率较高，可能在播放视频
                    try:
                        cpu_percent = proc.cpu_percent()
                        if cpu_percent > 10:  # 浏览器CPU使用率超过10%
                            return False
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            
            # 检查其他可能的活动应用
            activity_processes = ['wechatappex.exe', 'wechat.exe', 'qq.exe', 'dingtalk.exe']
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() in activity_processes:
                    return False
                        
        except Exception:
            pass
        
        # 只有在以下情况下才判断为睡觉：
        # 1. 超过1小时无活动
        # 2. 没有明确的活动应用
        # 3. 没有媒体播放或高CPU使用的浏览器
        # 4. 没有通信应用在运行
        return True
    
    def get_active_window_info(self):
        """获取当前活跃窗口信息"""
        if not WINDOWS_AVAILABLE:
            return None, None
            
        try:
            # 获取前台窗口
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return None, None
                
            # 获取窗口标题
            window_title = win32gui.GetWindowText(hwnd)
            
            # 获取进程ID
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            # 获取进程名
            try:
                process = psutil.Process(pid)
                process_name = process.name().lower()
                return process_name, window_title
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return None, None
                
        except Exception as e:
            print(f"获取窗口信息时出错: {e}")
            return None, None

    def _check_browser_activity(self, window_title):
        """检查浏览器活动并推断状态"""
        title_lower = window_title.lower()
        
        # B站相关 - 增加更多识别方式
        if any(keyword in title_lower for keyword in [
            'bilibili', 'b站', 'bili', 
            '游戏热门视频', '生活热门视频', '影视热门视频',
            'www.bilibili.com', 'space.bilibili.com',
            '哔哩哔哩', 'up主', '弹幕',
            '投币', '收藏', '分享'
        ]):
            return '4'  # 看B站
        
        # 学习相关
        if any(keyword in title_lower for keyword in ['coursera', 'udemy', '慕课', '学堂在线', 'edx']):
            return '7'  # 学习中
        
        # 工作相关
        if any(keyword in title_lower for keyword in ['github', 'stackoverflow', 'developer', 'documentation']):
            return '2'  # 工作中
        
        # 音乐相关
        if any(keyword in title_lower for keyword in ['music', '音乐', 'spotify', 'youtube music']):
            return '6'  # 听音乐
        
        # 默认返回工作中
        return '2'

    def _get_status_by_time(self):
        """根据时间段推断默认状态"""
        current_hour = datetime.now().hour
        
        # 工作时间默认为工作中
        if self.work_hours[0] <= current_hour < self.work_hours[1]:
            return '2'  # 工作中
        
        # 其他时间默认为工作中（由活动检测决定是否睡觉）
        return '2'
    
    def get_current_status(self):
        """获取当前应该的状态"""
        # 首先检查用户活动
        self.check_user_activity()
        
        # 获取当前活跃应用
        process_name, window_title = self.get_active_window_info()
        
        if process_name:
            # 检查应用映射
            if process_name in self.app_status_map:
                status_or_func = self.app_status_map[process_name]
                
                if callable(status_or_func):
                    # 如果是函数（如浏览器检查），调用函数
                    detected_status = status_or_func(window_title or '')
                    # 如果检测到明确的活动状态，直接返回
                    if detected_status in ['2', '4', '5', '6', '7', '8']:  # 工作、B站、游戏、音乐、学习、做饭
                        return detected_status
                else:
                    # 如果是直接的状态ID，且不是睡觉状态，直接返回
                    if status_or_func != '1':
                        return status_or_func
            else:
                # 未知应用，返回未知状态
                return '9'
        
        # 如果没有检测到明确的活动，最后检查是否应该睡觉
        if self.is_sleeping():
            return '1'  # 睡觉中
        
        # 如果没有活动的应用程序，返回未知状态而不是按时间段判断
        return '9'
    
    def update_status(self, status_id, app_name=None):
        """更新服务器状态"""
        try:
            url = f"{self.server_url}/set"
            params = {
                'secret': self.secret,
                'status': status_id,
                'user': self.user
            }
            
            # 如果是未知状态，添加应用名信息
            if status_id == '9' and app_name:
                params['app_name'] = app_name
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    status_name = data['status']['name']
                    if status_id == '9' and app_name:
                        print(f"✓ 状态已更新为: {status_name} - 当前应用: {app_name}")
                    else:
                        print(f"✓ 状态已更新为: {status_name}")
                    return True
                else:
                    print(f"✗ 更新失败: {data.get('error', '未知错误')}")
            else:
                print(f"✗ HTTP错误: {response.status_code}")
                
        except requests.RequestException as e:
            print(f"✗ 网络错误: {e}")
        except Exception as e:
            print(f"✗ 未知错误: {e}")
            
        return False
    
    def run(self):
        """主监控循环"""
        print("🚀 自动状态监控已启动...")
        print(f"👤 监控用户: {self.user}")
        print(f"📡 服务器地址: {self.server_url}")
        print(f"⏱️  检查间隔: {self.check_interval}秒")
        print(f"😴 睡觉判断: {self.sleep_timeout}分钟无活动")
        print("="*50)
        
        while True:
            try:
                # 获取当前状态
                current_status = self.get_current_status()
                
                # 如果状态有变化，更新服务器
                if current_status != self.last_status:
                    process_name, window_title = self.get_active_window_info()
                    
                    # 特殊处理睡觉状态的日志
                    if current_status == '1':
                        time_since_activity = datetime.now() - self.last_activity_time
                        print(f"😴 检测到睡觉状态:")
                        print(f"   最后活动时间: {self.last_activity_time.strftime('%H:%M:%S')}")
                        print(f"   无活动时长: {int(time_since_activity.total_seconds() // 60)}分钟")
                    else:
                        print(f"🔍 检测到状态变化:")
                        print(f"   应用: {process_name or '未知'}")
                        print(f"   标题: {window_title or '未知'}")
                        print(f"   状态: {current_status}")
                        
                        # 显示应用识别信息
                        if process_name and process_name in self.app_status_map:
                            status_or_func = self.app_status_map[process_name]
                            if callable(status_or_func):
                                print(f"   识别: 浏览器活动检测")
                            else:
                                print(f"   识别: 已知应用程序")
                        elif current_status == '9':
                            print(f"   识别: 未知应用程序")
                        else:
                            print(f"   识别: 按时间段判断")
                    
                    # 更新状态，如果是未知状态则传递应用名和窗口标题
                    app_name = None
                    if current_status == '9':
                        # 对于未知状态，组合应用名和窗口标题以提供更多信息
                        if process_name and window_title:
                            app_name = f"{process_name} - {window_title}"
                        elif process_name:
                            app_name = process_name
                        else:
                            app_name = "未知应用"
                    
                    if self.update_status(current_status, app_name):
                        self.last_status = current_status
                
                # 等待下一次检查
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("\n👋 监控已停止")
                break
            except Exception as e:
                print(f"⚠️  监控过程中出错: {e}")
                time.sleep(5)  # 出错后等待5秒再继续

def main():
    """主函数"""
    print("🌟 欢迎使用状态监控系统")
    print("请选择要监控的用户：")
    print("[1] 🐰 木头")
    print("[2] 🌧️ 乾雨")
    
    while True:
        choice = input("请输入选择 (1-2): ").strip()
        if choice == "1":
            user = "木头"
            break
        elif choice == "2":
            user = "乾雨"
            break
        else:
            print("❌ 无效选择，请重新输入")
    
    print(f"✅ 已选择监控用户: {user}")
    print()
    
    # 可以通过命令行参数或配置文件自定义设置
    monitor = StatusMonitor(
        server_url="http://101.43.113.154:5000",
        secret="birthday2024",
        user=user
    )
    
    monitor.run()

if __name__ == "__main__":
    main() 