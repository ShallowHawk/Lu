#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
状态监控程序 - GUI版本
提供图形界面的状态监控程序，方便用户使用
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import requests
import json
import os
from datetime import datetime, timedelta
import psutil
import sys

# Windows特有的库
try:
    import win32gui
    import win32process
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False

# 导入原有的StatusMonitor类
from auto_monitor import StatusMonitor

class StatusMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("状态监控程序 v1.0")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 设置窗口图标（如果存在）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # 监控器实例
        self.monitor = None
        self.monitor_thread = None
        self.is_running = False
        
        # 创建界面
        self.create_widgets()
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """创建GUI组件"""
        # 主标题
        title_label = tk.Label(self.root, text="🌟 状态监控程序", 
                              font=("Arial", 16, "bold"), fg="blue")
        title_label.pack(pady=10)
        
        # 用户选择框架
        user_frame = tk.LabelFrame(self.root, text="选择用户", font=("Arial", 12))
        user_frame.pack(pady=10, padx=20, fill="x")
        
        self.user_var = tk.StringVar(value="木头")
        user_radio1 = tk.Radiobutton(user_frame, text="🐰 木头", variable=self.user_var, 
                                    value="木头", font=("Arial", 10))
        user_radio1.pack(anchor="w", padx=10, pady=5)
        
        user_radio2 = tk.Radiobutton(user_frame, text="🌧️ 乾雨", variable=self.user_var, 
                                    value="乾雨", font=("Arial", 10))
        user_radio2.pack(anchor="w", padx=10, pady=5)
        
        # 服务器配置框架
        config_frame = tk.LabelFrame(self.root, text="服务器配置", font=("Arial", 12))
        config_frame.pack(pady=10, padx=20, fill="x")
        
        # 服务器地址
        tk.Label(config_frame, text="服务器地址:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.server_entry = tk.Entry(config_frame, width=40, font=("Arial", 9))
        self.server_entry.insert(0, "http://101.43.113.154:5000")
        self.server_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # 密钥
        tk.Label(config_frame, text="密钥:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.secret_entry = tk.Entry(config_frame, width=40, font=("Arial", 9), show="*")
        self.secret_entry.insert(0, "birthday2024")
        self.secret_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # 控制按钮
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(button_frame, text="🚀 开始监控", 
                                     command=self.start_monitoring, 
                                     font=("Arial", 12, "bold"), 
                                     bg="green", fg="white", width=12)
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = tk.Button(button_frame, text="⏹️ 停止监控", 
                                    command=self.stop_monitoring, 
                                    font=("Arial", 12, "bold"), 
                                    bg="red", fg="white", width=12, state="disabled")
        self.stop_button.pack(side="left", padx=10)
        
        # 状态显示
        status_frame = tk.LabelFrame(self.root, text="运行状态", font=("Arial", 12))
        status_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # 状态文本框
        self.status_text = tk.Text(status_frame, height=10, width=60, font=("Arial", 9))
        scrollbar = tk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 添加初始信息
        self.log_message("欢迎使用状态监控程序！")
        self.log_message("请选择用户并点击'开始监控'")
    
    def log_message(self, message):
        """添加日志信息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.status_text.insert(tk.END, log_entry)
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_monitoring(self):
        """开始监控"""
        if self.is_running:
            return
        
        # 验证配置
        server_url = self.server_entry.get().strip()
        secret = self.secret_entry.get().strip()
        user = self.user_var.get()
        
        if not server_url or not secret:
            messagebox.showerror("配置错误", "请填写完整的服务器地址和密钥")
            return
        
        # 测试连接
        self.log_message("正在测试服务器连接...")
        try:
            test_url = f"{server_url}/status"
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                self.log_message("✅ 服务器连接成功")
            else:
                self.log_message(f"⚠️ 服务器响应异常: {response.status_code}")
        except Exception as e:
            self.log_message(f"❌ 服务器连接失败: {e}")
            messagebox.showerror("连接错误", f"无法连接到服务器: {e}")
            return
        
        # 创建监控器实例
        self.monitor = StatusMonitor(server_url, secret, user)
        
        # 重写监控器的打印方法，让它输出到GUI
        original_print = print
        def gui_print(*args, **kwargs):
            message = " ".join(str(arg) for arg in args)
            self.log_message(message)
        
        # 替换print函数
        import builtins
        builtins.print = gui_print
        
        # 启动监控线程
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self.monitor_worker, daemon=True)
        self.monitor_thread.start()
        
        # 更新按钮状态
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        self.log_message(f"🚀 开始监控用户: {user}")
    
    def monitor_worker(self):
        """监控工作线程"""
        if not self.monitor:
            self.log_message("❌ 监控器未初始化")
            return
            
        try:
            self.log_message("🚀 自动状态监控已启动...")
            self.log_message(f"👤 监控用户: {self.monitor.user}")
            self.log_message(f"📡 服务器地址: {self.monitor.server_url}")
            self.log_message(f"⏱️  检查间隔: {self.monitor.check_interval}秒")
            self.log_message(f"😴 睡觉判断: {self.monitor.sleep_timeout}分钟无活动")
            self.log_message("="*50)
            
            while self.is_running and self.monitor:
                try:
                    # 获取当前状态
                    current_status = self.monitor.get_current_status()
                    
                    # 如果状态有变化，更新服务器
                    if current_status != self.monitor.last_status:
                        process_name, window_title = self.monitor.get_active_window_info()
                        
                        # 特殊处理睡觉状态的日志
                        if current_status == '1':
                            time_since_activity = datetime.now() - self.monitor.last_activity_time
                            self.log_message(f"😴 检测到睡觉状态:")
                            self.log_message(f"   最后活动时间: {self.monitor.last_activity_time.strftime('%H:%M:%S')}")
                            self.log_message(f"   无活动时长: {int(time_since_activity.total_seconds() // 60)}分钟")
                        else:
                            self.log_message(f"🔍 检测到状态变化:")
                            self.log_message(f"   应用: {process_name or '未知'}")
                            self.log_message(f"   标题: {window_title or '未知'}")
                            self.log_message(f"   状态: {current_status}")
                            
                            # 显示应用识别信息
                            if process_name and process_name in self.monitor.app_status_map:
                                status_or_func = self.monitor.app_status_map[process_name]
                                if callable(status_or_func):
                                    self.log_message(f"   识别: 浏览器活动检测")
                                else:
                                    self.log_message(f"   识别: 已知应用程序")
                            elif current_status == '9':
                                self.log_message(f"   识别: 未知应用程序")
                            else:
                                self.log_message(f"   识别: 按时间段判断")
                        
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
                        
                        if self.monitor.update_status(current_status, app_name):
                            self.monitor.last_status = current_status
                    
                    # 等待下一次检查
                    time.sleep(self.monitor.check_interval)
                    
                except Exception as e:
                    self.log_message(f"⚠️  监控过程中出错: {e}")
                    time.sleep(5)  # 出错后等待5秒再继续
                    
        except Exception as e:
            self.log_message(f"❌ 监控过程中出错: {e}")
        finally:
            self.is_running = False
            # 恢复按钮状态
            self.root.after(0, self.restore_buttons)
    
    def stop_monitoring(self):
        """停止监控"""
        if not self.is_running:
            return
        
        self.is_running = False
        self.log_message("🛑 正在停止监控...")
        
        # 恢复按钮状态
        self.restore_buttons()
        
        self.log_message("✅ 监控已停止")
    
    def restore_buttons(self):
        """恢复按钮状态"""
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
    
    def on_closing(self):
        """窗口关闭时的处理"""
        if self.is_running:
            result = messagebox.askyesno("确认退出", "监控正在运行，确定要退出吗？")
            if result:
                self.stop_monitoring()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """主函数"""
    # 检查Windows环境
    if not WINDOWS_AVAILABLE:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("系统不支持", "此程序仅支持Windows系统")
        return
    
    # 创建GUI
    root = tk.Tk()
    app = StatusMonitorGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("程序已退出")

if __name__ == "__main__":
    main() 