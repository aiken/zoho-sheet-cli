# Zoho Sheet CLI 本地测试脚本 (PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Zoho Sheet CLI 本地测试脚本" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
Write-Host "[1/6] 检查 Python 环境..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 未找到 Python，请先安装 Python 3.8+" -ForegroundColor Red
    exit 1
}
Write-Host "Python 版本: $pythonVersion"
Write-Host ""

# 创建虚拟环境
Write-Host "[2/6] 创建虚拟环境..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "虚拟环境创建完成" -ForegroundColor Green
} else {
    Write-Host "虚拟环境已存在" -ForegroundColor Gray
}
Write-Host ""

# 激活虚拟环境
Write-Host "[3/6] 激活虚拟环境..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "虚拟环境已激活" -ForegroundColor Green
Write-Host ""

# 安装依赖
Write-Host "[4/6] 安装依赖..." -ForegroundColor Yellow
$installOutput = pip install -e ".[dev]" -q 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 依赖安装失败" -ForegroundColor Red
    Write-Host $installOutput
    exit 1
}
Write-Host "依赖安装完成" -ForegroundColor Green
Write-Host ""

# 测试 CLI
Write-Host "[5/6] 测试 CLI 基础功能..." -ForegroundColor Yellow
Write-Host ""

Write-Host "5.1 测试版本..." -ForegroundColor Gray
$version = zsheet --version 2>&1
Write-Host "  版本: $version"
Write-Host ""

Write-Host "5.2 测试各命令帮助..." -ForegroundColor Gray

$commands = @(
    @{Name="auth"; Args="auth --help"},
    @{Name="workbook"; Args="workbook --help"},
    @{Name="worksheet"; Args="worksheet --help"},
    @{Name="cell"; Args="cell --help"},
    @{Name="file"; Args="file --help"}
)

foreach ($cmd in $commands) {
    $null = zsheet $cmd.Args 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] $($cmd.Name) 命令正常" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $($cmd.name) 命令失败" -ForegroundColor Red
    }
}
Write-Host ""

# 运行 pytest
Write-Host "[6/6] 运行 pytest 测试套件..." -ForegroundColor Yellow
pytest tests/ -v --tb=short
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 部分测试失败" -ForegroundColor Yellow
} else {
    Write-Host "[OK] 所有测试通过" -ForegroundColor Green
}
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   测试完成！" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "提示: 如果显示认证错误，这是正常的，" -ForegroundColor Gray
Write-Host "      因为还没有配置 Zoho API 凭证。" -ForegroundColor Gray
Write-Host ""
Write-Host "要配置认证，请运行: zsheet auth init" -ForegroundColor Cyan
Write-Host ""

Read-Host "按 Enter 键退出"
