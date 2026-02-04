@echo off
echo ===============================================
echo          生日网站自动部署脚本
echo ===============================================
echo.

:: 设置变量
set FRONTEND_DIR=birthday-website
set BACKEND_DIR=sleepy-status
set DIST_DIR=deployment
set TIMESTAMP=%date:~0,4%-%date:~5,2%-%date:~8,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%

echo [1/6] 检查环境...
:: 检查 Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装或不在PATH中
    echo 请先安装 Node.js 18+ 版本
    pause
    exit /b 1
)

:: 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装或不在PATH中
    echo 请先安装 Python 3.8+ 版本
    pause
    exit /b 1
)

echo ✅ 环境检查通过
echo.

echo [2/6] 准备部署目录...
if exist %DIST_DIR% (
    echo 删除旧的部署目录...
    rd /s /q %DIST_DIR%
)
mkdir %DIST_DIR%
mkdir %DIST_DIR%\frontend
mkdir %DIST_DIR%\backend
echo ✅ 部署目录准备完成
echo.

echo [3/6] 构建前端项目...
cd %FRONTEND_DIR%

:: 安装依赖
echo 安装前端依赖...
npm install
if %errorlevel% neq 0 (
    echo ❌ 前端依赖安装失败
    cd ..
    pause
    exit /b 1
)

:: 生成静态文件
echo 生成静态文件...
npm run generate
if %errorlevel% neq 0 (
    echo ❌ 静态文件生成失败
    cd ..
    pause
    exit /b 1
)

:: 复制构建文件
echo 复制前端构建文件...
xcopy /E /I /Y .output\public ..\%DIST_DIR%\frontend\
if %errorlevel% neq 0 (
    echo ❌ 前端文件复制失败
    cd ..
    pause
    exit /b 1
)

cd ..
echo ✅ 前端构建完成
echo.

echo [4/6] 准备后端文件...
echo 复制后端文件...
xcopy /E /I /Y %BACKEND_DIR% %DIST_DIR%\backend\
if %errorlevel% neq 0 (
    echo ❌ 后端文件复制失败
    pause
    exit /b 1
)

:: 移除本地监控文件（不需要在服务器上运行）
if exist %DIST_DIR%\backend\auto_monitor.py (
    del %DIST_DIR%\backend\auto_monitor.py
)
if exist %DIST_DIR%\backend\start_monitor.bat (
    del %DIST_DIR%\backend\start_monitor.bat
)

echo ✅ 后端文件准备完成
echo.

echo [5/6] 创建部署说明文件...
echo 创建部署说明文件 > %DIST_DIR%\部署说明.txt
echo ==================== >> %DIST_DIR%\部署说明.txt
echo 生成时间: %TIMESTAMP% >> %DIST_DIR%\部署说明.txt
echo. >> %DIST_DIR%\部署说明.txt
echo 目录结构: >> %DIST_DIR%\部署说明.txt
echo - frontend/   前端静态文件，上传到网站根目录 >> %DIST_DIR%\部署说明.txt
echo - backend/    后端API文件，上传到服务器API目录 >> %DIST_DIR%\部署说明.txt
echo. >> %DIST_DIR%\部署说明.txt
echo 部署步骤: >> %DIST_DIR%\部署说明.txt
echo 1. 将 frontend/ 文件夹内容上传到服务器网站根目录 >> %DIST_DIR%\部署说明.txt
echo 2. 将 backend/ 文件夹内容上传到服务器API目录 >> %DIST_DIR%\部署说明.txt
echo 3. 在服务器上运行: pip install -r requirements.txt >> %DIST_DIR%\部署说明.txt
echo 4. 启动后端服务: python app.py >> %DIST_DIR%\部署说明.txt
echo 5. 配置Nginx反向代理 >> %DIST_DIR%\部署说明.txt
echo. >> %DIST_DIR%\部署说明.txt
echo 详细步骤请参考: 宝塔面板部署指南.md >> %DIST_DIR%\部署说明.txt

echo ✅ 部署说明文件创建完成
echo.

echo [6/6] 创建部署包...
cd %DIST_DIR%
powershell -Command "Compress-Archive -Path * -DestinationPath ..\部署包_%TIMESTAMP%.zip -Force"
if %errorlevel% neq 0 (
    echo ❌ 部署包创建失败
    cd ..
    pause
    exit /b 1
)
cd ..

echo ✅ 部署包创建完成
echo.

echo ===============================================
echo             部署准备完成！
echo ===============================================
echo 📦 部署包位置: 部署包_%TIMESTAMP%.zip
echo 📁 部署文件夹: %DIST_DIR%\
echo.
echo 接下来的步骤：
echo 1. 上传部署包到服务器
echo 2. 按照 宝塔面板部署指南.md 进行部署
echo 3. 在本地运行 auto_monitor.py 进行状态监控
echo.
echo 💡 提示：
echo - 记得在 useApi.js 中修改您的域名
echo - 确保服务器安装了 Python 3.8+ 和相关依赖
echo - 配置好 Nginx 反向代理
echo.
pause 