@echo off
chcp 65001 >nul
echo ==========================================
echo   Zoho Sheet CLI 本地测试脚本
echo ==========================================
echo.

:: 检查 Python
echo [1/6] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    exit /b 1
)
python --version
echo.

:: 创建虚拟环境
echo [2/6] 创建虚拟环境...
if not exist "venv" (
    python -m venv venv
    echo 虚拟环境创建完成
) else (
    echo 虚拟环境已存在
)
echo.

:: 激活虚拟环境
echo [3/6] 激活虚拟环境...
call venv\Scripts\activate.bat
echo 虚拟环境已激活
echo.

:: 安装依赖
echo [4/6] 安装依赖...
pip install -e ".[dev]" -q
if errorlevel 1 (
    echo [错误] 依赖安装失败
    exit /b 1
)
echo 依赖安装完成
echo.

:: 测试 CLI
echo [5/6] 测试 CLI 基础功能...
echo.
echo 5.1 测试版本...
zsheet --version
echo.

echo 5.2 测试主帮助...
zsheet --help
echo.

echo 5.3 测试子命令帮助...
echo - auth 命令:
zsheet auth --help >nul 2>&1 && echo   [OK] auth 命令正常 || echo   [FAIL] auth 命令失败

echo - workbook 命令:
zsheet workbook --help >nul 2>&1 && echo   [OK] workbook 命令正常 || echo   [FAIL] workbook 命令失败

echo - worksheet 命令:
zsheet worksheet --help >nul 2>&1 && echo   [OK] worksheet 命令正常 || echo   [FAIL] worksheet 命令失败

echo - cell 命令:
zsheet cell --help >nul 2>&1 && echo   [OK] cell 命令正常 || echo   [FAIL] cell 命令失败

echo - file 命令:
zsheet file --help >nul 2>&1 && echo   [OK] file 命令正常 || echo   [FAIL] file 命令失败
echo.

:: 运行 pytest
echo [6/6] 运行 pytest 测试套件...
pytest tests/ -v --tb=short
if errorlevel 1 (
    echo [警告] 部分测试失败
) else (
    echo [OK] 所有测试通过
)
echo.

echo ==========================================
echo   测试完成！
echo ==========================================
echo.
echo 提示: 如果显示认证错误，这是正常的，
echo       因为还没有配置 Zoho API 凭证。
echo.
echo 要配置认证，请运行: zsheet auth init
echo.

pause
