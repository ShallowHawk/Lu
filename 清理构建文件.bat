@echo off
echo ===============================================
echo          清理构建文件脚本
echo ===============================================
echo.

echo 正在清理前端构建文件...
cd birthday-website

if exist .output (
    echo 删除 .output 文件夹...
    rd /s /q .output
    echo ✅ .output 文件夹已删除
) else (
    echo ⚠️  .output 文件夹不存在
)

if exist .nuxt (
    echo 删除 .nuxt 文件夹...
    rd /s /q .nuxt
    echo ✅ .nuxt 文件夹已删除
) else (
    echo ⚠️  .nuxt 文件夹不存在
)

if exist node_modules\.cache (
    echo 删除 node_modules 缓存...
    rd /s /q node_modules\.cache
    echo ✅ node_modules 缓存已删除
) else (
    echo ⚠️  node_modules 缓存不存在
)

cd ..

echo.
echo 正在清理部署文件...
if exist deployment (
    echo 删除 deployment 文件夹...
    rd /s /q deployment
    echo ✅ deployment 文件夹已删除
) else (
    echo ⚠️  deployment 文件夹不存在
)

echo.
echo ===============================================
echo             清理完成！
echo ===============================================
echo.
echo 🎉 所有构建文件已清理完成！
echo.
echo 💡 下一步：
echo 1. 运行 npm run generate 重新构建
echo 2. 或者运行 部署脚本.bat 自动构建和打包
echo.
pause 