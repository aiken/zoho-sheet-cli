"""
Zoho Sheet CLI 使用示例

运行前请先设置环境变量:
    export ZOHO_CLIENT_ID="your_client_id"
    export ZOHO_CLIENT_SECRET="your_client_secret"
    export ZOHO_REFRESH_TOKEN="your_refresh_token"
"""

import os
from zoho_sheet_cli.client import ZohoSheetClient
from zoho_sheet_cli.config import Config


def demo_without_auth():
    """演示：未认证状态下的 CLI 功能"""
    print("=" * 50)
    print("测试 1: 检查认证状态")
    print("=" * 50)
    
    config = Config()
    print(f"已配置 Client ID: {bool(config.client_id)}")
    print(f"已配置 Client Secret: {bool(config.client_secret)}")
    print(f"已配置 Refresh Token: {bool(config.refresh_token)}")
    print(f"当前区域: {config.region}")
    print(f"是否已认证: {config.is_authenticated}")
    
    if not config.is_authenticated:
        print("\n⚠️  未配置认证信息，请先运行: zsheet auth init")
        return False
    return True


def demo_with_auth():
    """演示：已认证状态下的 API 调用"""
    print("\n" + "=" * 50)
    print("测试 2: API 调用示例")
    print("=" * 50)
    
    try:
        client = ZohoSheetClient()
        print("✓ 客户端初始化成功")
        
        # 列出工作簿
        print("\n列出工作簿...")
        workbooks = client.list_workbooks()
        print(f"  找到 {len(workbooks)} 个工作簿")
        for wb in workbooks[:3]:  # 只显示前3个
            print(f"  - {wb.get('workbook_name')} (ID: {wb.get('resource_id')})")
        
        if workbooks:
            workbook_id = workbooks[0].get('resource_id')
            
            # 列出工作表
            print(f"\n列出工作簿 {workbook_id} 的工作表...")
            worksheets = client.list_worksheets(workbook_id)
            print(f"  找到 {len(worksheets)} 个工作表")
            for ws in worksheets:
                print(f"  - {ws.get('sheet_name')}")
            
            # 读取单元格
            if worksheets:
                sheet_name = worksheets[0].get('sheet_name')
                print(f"\n读取单元格 A1...")
                cell_data = client.get_cell(workbook_id, sheet_name, "A1")
                print(f"  值: {cell_data.get('data', {}).get('value')}")
        
        return True
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        return False


def demo_commands():
    """演示：命令行用法示例"""
    print("\n" + "=" * 50)
    print("测试 3: 命令行用法示例")
    print("=" * 50)
    
    commands = [
        ("查看帮助", "zsheet --help"),
        ("查看版本", "zsheet --version"),
        ("认证状态", "zsheet auth status"),
        ("列出工作簿", "zsheet workbook list"),
        ("创建工作簿", "zsheet workbook create --name '测试工作簿'"),
        ("列出工作表", "zsheet worksheet list <workbook_id>"),
        ("读取单元格", "zsheet cell get <workbook_id> Sheet1 --cell A1"),
        ("写入单元格", "zsheet cell set <workbook_id> Sheet1 --cell A1 --value 'Hello'"),
        ("导出文件", "zsheet file export <workbook_id> --format xlsx --output data.xlsx"),
    ]
    
    for desc, cmd in commands:
        print(f"\n{desc}:")
        print(f"  $ {cmd}")


if __name__ == "__main__":
    print("Zoho Sheet CLI 测试脚本")
    print("=" * 50)
    
    # 测试 1: 检查认证状态
    is_auth = demo_without_auth()
    
    # 测试 2: 如果有认证信息，测试 API 调用
    if is_auth:
        demo_with_auth()
    
    # 测试 3: 显示命令行用法
    demo_commands()
    
    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)
