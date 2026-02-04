@echo off
echo ===============================================
echo          部署前环境检查脚本
echo ===============================================
echo.

echo [1/5] 检查 Node.js 环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装或不在PATH中
    echo 请先安装 Node.js 18+ 版本
    goto :error
) else (
    echo ✅ Node.js 已安装
    node --version
)
echo.

echo [2/5] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装或不在PATH中
    echo 请先安装 Python 3.8+ 版本
    goto :error
) else (
    echo ✅ Python 已安装
    python --version
)
echo.

echo [3/5] 检查项目文件结构...
if not exist "birthday-website" (
    echo ❌ 找不到 birthday-website 文件夹
    goto :error
)
if not exist "sleepy-status" (
    echo ❌ 找不到 sleepy-status 文件夹
    goto :error
)
if not exist "birthday-website\package.json" (
    echo ❌ 找不到前端 package.json 文件
    goto :error
)
if not exist "sleepy-status\app.py" (
    echo ❌ 找不到后端 app.py 文件
    goto :error
)
if not exist "sleepy-status\requirements.txt" (
    echo ❌ 找不到后端 requirements.txt 文件
    goto :error
)
echo ✅ 项目文件结构正确
echo.

echo [4/5] 检查前端依赖...
cd birthday-website
if not exist "node_modules" (
    echo ⚠️  前端依赖未安装，正在安装...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ 前端依赖安装失败
        cd ..
        goto :error
    )
) else (
    echo ✅ 前端依赖已安装
)
cd ..
echo.

echo [5/5] 检查后端依赖...
cd sleepy-status
echo 检查 Python 依赖...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  后端依赖未安装，正在安装...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ 后端依赖安装失败
        cd ..
        goto :error
    )
) else (
    echo ✅ 后端依赖已安装
)
cd ..
echo.

echo ===============================================
echo             环境检查完成！
echo ===============================================
echo.
echo 📋 检查结果：
echo ✅ Node.js 环境正常
echo ✅ Python 环境正常
echo ✅ 项目文件结构正确
echo ✅ 前端依赖已安装
echo ✅ 后端依赖已安装
echo.
echo 🎉 所有检查通过！您可以开始部署了。
echo.
echo 💡 下一步：
echo 1. 运行 部署脚本.bat 来构建部署包
echo 2. 按照 宝塔面板部署指南.md 进行部署
echo 3. 记得修改 useApi.js 中的域名配置
echo.
goto :end

:error
echo.
echo ===============================================
echo             检查失败！
echo ===============================================
echo.
echo ❌ 部署前检查未通过，请解决上述问题后重试。
echo.
echo 🔧 可能的解决方案：
echo - 安装 Node.js 18+ 版本
echo - 安装 Python 3.8+ 版本
echo - 确保项目文件完整
echo - 检查网络连接
echo.

:end
pause 