# Zoho Sheet CLI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个功能强大的命令行工具，用于与 Zoho Sheet API v2 交互。

## 功能特性

- 📊 **工作簿管理** - 创建、列出、删除、复制工作簿
- 📑 **工作表操作** - 添加、删除、重命名、排序工作表
- 📝 **单元格操作** - 读取、写入、格式化单元格
- 🔄 **行列操作** - 插入、删除、隐藏、调整行列
- 📤 **文件导入导出** - 支持 CSV、XLS、XLSX 格式
- 🔍 **搜索与筛选** - 在工作表中搜索数据
- 🔐 **OAuth2 认证** - 安全的认证流程

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install zoho-sheet-cli
```

### 从源码安装

```bash
git clone https://github.com/aiken/zoho-sheet-cli.git
cd zoho-sheet-cli
pip install -e .
```

## 快速开始

### 1. 配置认证

在使用 CLI 之前，你需要配置 Zoho OAuth2 认证信息：

```bash
# 方式1：使用环境变量
export ZOHO_CLIENT_ID="your_client_id"
export ZOHO_CLIENT_SECRET="your_client_secret"
export ZOHO_REFRESH_TOKEN="your_refresh_token"

# 方式2：使用配置文件
zsheet auth init
```

### 2. 开始使用

```bash
# 列出所有工作簿
zsheet workbook list

# 创建新工作簿
zsheet workbook create --name "My Workbook"

# 获取工作簿信息
zsheet workbook info <workbook_id>

# 查看帮助
zsheet --help
```

## 命令参考

### 认证命令

```bash
zsheet auth init              # 初始化认证配置
zsheet auth status            # 查看认证状态
zsheet auth refresh           # 刷新访问令牌
```

### 工作簿命令

```bash
zsheet workbook list                    # 列出所有工作簿
zsheet workbook create --name "Name"    # 创建新工作簿
zsheet workbook info <id>               # 获取工作簿信息
zsheet workbook delete <id>             # 删除工作簿
zsheet workbook copy <id> --name "New"  # 复制工作簿
zsheet workbook rename <id> --name "New" # 重命名工作簿
```

### 工作表命令

```bash
zsheet worksheet list <workbook_id>                    # 列出所有工作表
zsheet worksheet add <workbook_id> --name "Sheet1"     # 添加工作表
zsheet worksheet delete <workbook_id> <sheet_name>     # 删除工作表
zsheet worksheet rename <workbook_id> <old> --new "New" # 重命名工作表
```

### 单元格命令

```bash
# 读取单元格
zsheet cell get <workbook_id> <sheet> --cell A1

# 写入单元格
zsheet cell set <workbook_id> <sheet> --cell A1 --value "Hello"

# 批量写入
zsheet cell set-batch <workbook_id> <sheet> --data "A1:Hello,B1:World"

# 读取范围
zsheet cell range <workbook_id> <sheet> --range "A1:D10"
```

### 文件操作

```bash
# 导出为 CSV
zsheet file export <workbook_id> --format csv --output data.csv

# 导入 CSV
zsheet file import --file data.csv --name "Imported"
```

## 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `ZOHO_CLIENT_ID` | Zoho OAuth2 Client ID | 是 |
| `ZOHO_CLIENT_SECRET` | Zoho OAuth2 Client Secret | 是 |
| `ZOHO_REFRESH_TOKEN` | Zoho OAuth2 Refresh Token | 是 |
| `ZOHO_REGION` | Zoho 区域 (us, eu, in, cn, au, jp) | 否 (默认: us) |

## 获取 Zoho API 凭证

1. 访问 [Zoho API Console](https://api-console.zoho.com/)
2. 创建一个新的 "Self Client" 或 "Server-based Application"
3. 获取 Client ID 和 Client Secret
4. 使用 OAuth2 流程获取 Refresh Token

## 开发

```bash
# 克隆仓库
git clone https://github.com/aiken/zoho-sheet-cli.git
cd zoho-sheet-cli

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关链接

- [Zoho Sheet API v2 文档](https://www.zoho.com/sheet/help/api/v2/)
- [Zoho API Console](https://api-console.zoho.com/)
