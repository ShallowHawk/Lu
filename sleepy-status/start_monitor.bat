@echo off
chcp 65001 >nul
echo.
echo ==========================================
echo    🚀 林璐状态监控系统启动器
echo ==========================================
echo.

:: 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未检测到Python，请先安装Python
    pause
    exit /b 1
)

:: 检查依赖是否已安装
echo 📦 检查依赖...
pip show psutil >nul 2>&1
if errorlevel 1 (
    echo 📥 安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

echo ✅ 依赖检查完成
echo.

:: 启动选择菜单
:menu
echo 请选择启动模式:
echo [1] 只启动API服务器 (手动控制)
echo [2] 只启动自动监控 (需要API服务器运行)
echo [3] 同时启动API服务器和自动监控 (推荐)
echo [4] 退出
echo.
set /p choice=请输入选择 (1-4): 

if "%choice%"=="1" goto start_server
if "%choice%"=="2" goto start_monitor
if "%choice%"=="3" goto start_both
if "%choice%"=="4" exit /b 0
echo ❌ 无效选择，请重新输入
goto menu

:start_server
echo.
echo 🌐 启动API服务器...
echo 📱 手机控制面板: http://127.0.0.1:5000/mobile
echo 🖥️  状态展示页面: http://127.0.0.1:5000/status_page
echo.
python app.py
pause
exit /b 0

:start_monitor
echo.
echo 🤖 启动自动监控...
echo ⚠️  请确保API服务器已经在运行 (端口5000)
echo.
python auto_monitor.py
pause
exit /b 0

:start_both
echo.
echo 🚀 启动完整系统...
echo 📱 手机控制面板: http://127.0.0.1:5000/mobile
echo 🖥️  状态展示页面: http://127.0.0.1:5000/status_page
echo.
echo 正在启动API服务器...
start /min cmd /c "python app.py"

:: 等待API服务器启动
timeout /t 3 /nobreak >nul

echo 正在启动自动监控...
python auto_monitor.py

echo.
echo 🛑 自动监控已停止
pause
exit /b 0 