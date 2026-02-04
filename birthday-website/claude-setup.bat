@echo off
REM Command Prompt 配置 claude 别名
REM 运行此批处理文件来设置 claude 别名

echo 正在为 Command Prompt 配置 claude 别名...

REM 创建一个批处理文件作为 claude 命令
echo @echo off > "%USERPROFILE%\claude.bat"
echo npx win-claude-code@latest %%* >> "%USERPROFILE%\claude.bat"

REM 添加用户目录到 PATH（如果尚未添加）
echo.
echo 请手动将以下路径添加到系统环境变量 PATH 中：
echo %USERPROFILE%
echo.
echo 或者运行以下命令（需要管理员权限）：
echo setx PATH "%%PATH%%;%USERPROFILE%%" /M
echo.
echo 配置完成！重新打开 Command Prompt 后即可使用 claude 命令

pause