# PowerShell 配置 claude 别名
# 运行此脚本来设置 claude 别名

# 获取 PowerShell profile 路径
$profilePath = $PROFILE

# 检查 profile 文件是否存在，如果不存在则创建
if (!(Test-Path $profilePath)) {
    New-Item -ItemType File -Path $profilePath -Force
    Write-Host "已创建 PowerShell profile: $profilePath"
}

# 添加 claude 别名到 profile
$aliasCommand = 'function claude { npx win-claude-code@latest $args }'

# 检查是否已经存在 claude 别名
$content = Get-Content $profilePath -ErrorAction SilentlyContinue
if ($content -notcontains $aliasCommand) {
    Add-Content -Path $profilePath -Value $aliasCommand
    Write-Host "已添加 claude 别名到 PowerShell profile"
} else {
    Write-Host "claude 别名已存在于 PowerShell profile"
}

Write-Host "请重新启动 PowerShell 或运行 '. $PROFILE' 来使别名生效"