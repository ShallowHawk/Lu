@echo off
chcp 65001 >nul
title 状态监控程序构建工具

echo 🔧 状态监控程序构建工具
echo ==================================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python环境
    echo 请先安装Python 3.7或更高版本
    echo.
    pause
    exit /b 1
)

REM 检查依赖
echo 正在检查依赖...
pip install -r requirements.txt >nul 2>&1

REM 启动构建程序
echo 正在启动构建程序...
echo.
python build_exe.py

pause 