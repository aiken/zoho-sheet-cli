# Zoho Sheet CLI 本地测试指南

## 📋 环境要求

- Python 3.8 或更高版本
- pip (Python 包管理器)
- Git

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/aiken/zoho-sheet-cli.git
cd zoho-sheet-cli
```

### 2. 创建虚拟环境（推荐）

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
# 基础安装
pip install -e .

# 开发安装（包含测试工具）
pip install -e ".[dev]"
```

## 🧪 测试项目

### 测试 1：基础 CLI 功能（无需认证）

```bash
# 检查版本
zsheet --version
# 预期输出: zsheet, version 0.1.0

# 查看主帮助
zsheet --help

# 查看子命令帮助
zsheet auth --help
zsheet workbook --help
zsheet worksheet --help
zsheet cell --help
zsheet file --help
```

### 测试 2：认证命令

```bash
# 查看认证指南
zsheet auth guide

# 初始化认证（交互式）
zsheet auth init
# 按提示输入 Client ID、Client Secret、Refresh Token

# 查看认证状态
zsheet auth status
```

### 测试 3：运行测试套件

```bash
# 运行所有测试
pytest -v

# 运行特定测试文件
pytest tests/test_cli.py -v
pytest tests/test_config.py -v
pytest tests/test_client.py -v

# 带覆盖率报告
pytest --cov=zoho_sheet_cli --cov-report=html
```

### 测试 4：使用演示脚本

```bash
# 运行演示脚本
python examples/demo.py
```

## 🔐 完整功能测试（需要 Zoho 账号）

### 步骤 1：获取 API 凭证

1. 访问 https://api-console.zoho.com/
2. 点击 "Add Client" → "Self Client"
3. 记录 Client ID 和 Client Secret
4. 生成授权码：
   - Scope: `ZohoSheet.data.ALL`, `ZohoSheet.workbooks.ALL`
   - Time Duration: 10 minutes
   - Scope Description: Zoho Sheet Access
5. 换取 Refresh Token：

```bash
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "code=YOUR_AUTH_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=http://localhost" \
  -d "grant_type=authorization_code"
```

保存返回的 `refresh_token`

### 步骤 2：配置认证

```bash
# 方式 1：使用命令
zsheet auth init

# 方式 2：环境变量
export ZOHO_CLIENT_ID="your_client_id"
export ZOHO_CLIENT_SECRET="your_client_secret"
export ZOHO_REFRESH_TOKEN="your_refresh_token"
export ZOHO_REGION="us"  # 可选: us, eu, in, cn, au, jp
```

### 步骤 3：测试完整功能

```bash
# ===== 工作簿操作 =====

# 列出所有工作簿
zsheet workbook list

# 创建新工作簿
zsheet workbook create --name "测试工作簿"

# 获取工作簿信息
zsheet workbook info <workbook_id>

# 复制工作簿
zsheet workbook copy <workbook_id> --name "副本"

# 重命名工作簿
zsheet workbook rename <workbook_id> --name "新名称"

# ===== 工作表操作 =====

# 列出工作表
zsheet worksheet list <workbook_id>

# 添加工作表
zsheet worksheet add <workbook_id> --name "新工作表"

# 重命名工作表
zsheet worksheet rename <workbook_id> "旧名称" --new "新名称"

# 删除工作表
zsheet worksheet delete <workbook_id> "工作表名称"

# ===== 单元格操作 =====

# 读取单元格
zsheet cell get <workbook_id> "Sheet1" --cell A1

# 写入单元格
zsheet cell set <workbook_id> "Sheet1" --cell A1 --value "Hello World"

# 读取范围
zsheet cell range <workbook_id> "Sheet1" --range "A1:D10"

# 批量写入（范围）
zsheet cell set-range <workbook_id> "Sheet1" \
  --range "A1:B2" \
  --values '[["A1","B1"],["A2","B2"]]'

# ===== 文件操作 =====

# 导出为 Excel
zsheet file export <workbook_id> --format xlsx --output data.xlsx

# 导出为 CSV
zsheet file export <workbook_id> --format csv --output data.csv

# 导入文件
zsheet file import --file data.csv --name "导入的数据"
```

### 步骤 4：JSON 输出模式

所有命令都支持 `--json` 或 `-j` 标志，用于脚本集成：

```bash
# 获取 JSON 格式输出
zsheet workbook list --json
zsheet workbook info <workbook_id> --json
zsheet cell get <workbook_id> Sheet1 --cell A1 --json
```

## 🛠️ 故障排除

### 问题 1：命令未找到

```bash
# 检查安装
which zsheet  # macOS/Linux
where zsheet  # Windows

# 重新安装
pip install -e .
```

### 问题 2：认证失败

```bash
# 检查环境变量
echo $ZOHO_CLIENT_ID
echo $ZOHO_CLIENT_SECRET
echo $ZOHO_REFRESH_TOKEN

# 重新初始化认证
zsheet auth init

# 刷新令牌
zsheet auth refresh
```

### 问题 3：API 错误

```bash
# 启用调试模式
zsheet --debug workbook list
```

## 📊 测试检查清单

- [ ] Python 3.8+ 已安装
- [ ] 虚拟环境已激活
- [ ] 包安装成功
- [ ] `zsheet --version` 正常输出
- [ ] `zsheet --help` 显示帮助
- [ ] 所有子命令帮助正常
- [ ] pytest 测试通过
- [ ] 演示脚本运行正常
- [ ] （可选）已配置 Zoho 认证
- [ ] （可选）工作簿操作正常
- [ ] （可选）单元格操作正常
- [ ] （可选）文件导入导出正常

## 📝 反馈

遇到问题请在 GitHub 提交 Issue：
https://github.com/aiken/zoho-sheet-cli/issues
