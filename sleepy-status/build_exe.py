#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建可执行文件脚本
使用PyInstaller将auto_monitor.py打包成Windows可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ PyInstaller安装失败")
        return False

def build_exe(version="console"):
    """构建可执行文件"""
    if not check_pyinstaller():
        if not install_pyinstaller():
            return False
    
    # 清理之前的构建
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    print(f"开始构建可执行文件 ({version}版本)...")
    
    # 根据版本选择不同的配置
    if version == "gui":
        # GUI版本
        cmd = [
            "pyinstaller",
            "--onefile",  # 打包成单个文件
            "--windowed",  # 不显示控制台窗口
            "--name=状态监控程序_GUI",  # 可执行文件名称
            "--add-data=requirements.txt;.",  # 包含requirements.txt
            "--icon=icon.ico",  # 图标文件（如果存在）
            "start_gui.py"
        ]
    else:
        # 控制台版本
        cmd = [
            "pyinstaller",
            "--onefile",  # 打包成单个文件
            "--console",  # 显示控制台窗口
            "--name=状态监控程序_控制台",  # 可执行文件名称
            "--add-data=requirements.txt;.",  # 包含requirements.txt
            "--icon=icon.ico",  # 图标文件（如果存在）
            "auto_monitor.py"
        ]
    
    # 如果没有图标文件，移除图标参数
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 构建成功！")
        exe_name = "状态监控程序_GUI.exe" if version == "gui" else "状态监控程序_控制台.exe"
        print(f"可执行文件位置: {os.path.abspath(f'dist/{exe_name}')}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        if e.stdout:
            print("标准输出:", e.stdout)
        if e.stderr:
            print("错误输出:", e.stderr)
        return False

def create_portable_package():
    """创建便携包"""
    gui_exe = "dist/状态监控程序_GUI.exe"
    console_exe = "dist/状态监控程序_控制台.exe"
    
    if not os.path.exists(gui_exe) and not os.path.exists(console_exe):
        print("❌ 找不到可执行文件，请先构建")
        return False
    
    # 创建便携包目录
    package_dir = "状态监控程序_便携版"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    # 复制可执行文件
    if os.path.exists(gui_exe):
        shutil.copy2(gui_exe, package_dir)
    if os.path.exists(console_exe):
        shutil.copy2(console_exe, package_dir)
    
    # 创建使用说明
    readme_content = """# 状态监控程序使用说明

## 程序版本
- **状态监控程序_GUI.exe**: 图形界面版本，推荐使用
- **状态监控程序_控制台.exe**: 控制台版本，适合高级用户

## 快速开始
### GUI版本（推荐）
1. 双击 `状态监控程序_GUI.exe` 启动程序
2. 在界面中选择要监控的用户（木头 或 乾雨）
3. 确认服务器配置（通常无需修改）
4. 点击"开始监控"按钮
5. 程序将自动监控您的应用程序使用情况并上传状态

### 控制台版本
1. 双击 `状态监控程序_控制台.exe` 启动程序
2. 按照提示选择要监控的用户（1-2）
3. 程序将自动监控您的应用程序使用情况并上传状态

## 功能说明
- 自动检测当前使用的应用程序
- 根据应用程序类型自动判断状态（工作、学习、游戏、看视频等）
- 检测用户活动，长时间无活动时自动切换为睡觉状态
- 实时上传状态到服务器

## 支持的应用程序
- **工作**: VS Code, PyCharm, Cursor, 微信, QQ, 钉钉等
- **学习**: Anki, Obsidian, Notion, Typora等
- **游戏**: Steam, 原神, 英雄联盟等
- **视频**: B站桌面版, PotPlayer, VLC等
- **音乐**: 网易云音乐, Spotify, QQ音乐等
- **浏览器**: 自动识别网站类型（B站、学习网站等）

## 注意事项
- 首次运行可能需要管理员权限
- 程序会在系统托盘中运行
- 如需停止程序，请按Ctrl+C或关闭窗口
- 程序需要网络连接才能上传状态

## 问题排查
如果程序无法正常运行，请检查：
1. 网络连接是否正常
2. 防火墙是否阻止了程序
3. 杀毒软件是否误报

## 联系支持
如有问题请联系开发者。
"""
    
    with open(os.path.join(package_dir, "使用说明.txt"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ 便携包创建成功: {package_dir}")
    return True

def main():
    """主函数"""
    print("🔧 状态监控程序构建工具")
    print("=" * 50)
    
    print("选择操作:")
    print("[1] 构建GUI版本")
    print("[2] 构建控制台版本")
    print("[3] 构建全部版本")
    print("[4] 创建便携包")
    print("[5] 全部执行")
    
    while True:
        choice = input("请输入选择 (1-5): ").strip()
        if choice == "1":
            if build_exe("gui"):
                print("✅ GUI版本构建完成")
            break
        elif choice == "2":
            if build_exe("console"):
                print("✅ 控制台版本构建完成")
            break
        elif choice == "3":
            gui_success = build_exe("gui")
            console_success = build_exe("console")
            if gui_success and console_success:
                print("✅ 全部版本构建完成")
            elif gui_success:
                print("✅ GUI版本构建完成，控制台版本构建失败")
            elif console_success:
                print("✅ 控制台版本构建完成，GUI版本构建失败")
            else:
                print("❌ 所有版本构建失败")
            break
        elif choice == "4":
            if create_portable_package():
                print("✅ 便携包创建完成")
            break
        elif choice == "5":
            gui_success = build_exe("gui")
            console_success = build_exe("console")
            if gui_success or console_success:
                print("✅ 构建完成")
                if create_portable_package():
                    print("✅ 便携包创建完成")
                print("🎉 全部操作完成")
            else:
                print("❌ 构建失败，无法创建便携包")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main() 