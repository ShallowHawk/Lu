#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试脚本
验证前后端对接是否正常
"""

import requests
import json
from datetime import datetime

def test_api():
    """测试API接口"""
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 开始测试API接口...")
    print("=" * 50)
    
    # 测试1: 获取系统信息
    print("\n1. 测试系统信息接口 GET /")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ 系统信息获取成功")
            print(f"   版本: {data.get('version', 'N/A')}")
            print(f"   消息: {data.get('message', 'N/A')}")
        else:
            print(f"❌ 获取系统信息失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 连接错误: {e}")
    
    # 测试2: 获取状态列表
    print("\n2. 测试状态列表接口 GET /get/status_list")
    try:
        response = requests.get(f"{base_url}/get/status_list")
        if response.status_code == 200:
            data = response.json()
            print("✅ 状态列表获取成功")
            print(f"   共有 {len(data.get('status_list', {}))} 种状态")
            for status_id, status_info in data.get('status_list', {}).items():
                print(f"   {status_id}: {status_info['name']} - {status_info['desc']}")
        else:
            print(f"❌ 获取状态列表失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 连接错误: {e}")
    
    # 测试3: 获取所有用户状态
    print("\n3. 测试用户状态接口 GET /query (所有用户)")
    try:
        response = requests.get(f"{base_url}/query")
        if response.status_code == 200:
            data = response.json()
            print("✅ 用户状态获取成功")
            
            if 'users' in data:
                print("   多用户格式:")
                for user_id, user_data in data['users'].items():
                    print(f"   - {user_data['display_name']} {user_data['emoji']}: {user_data['name']}")
                    if user_data.get('last_update'):
                        print(f"     最后更新: {user_data['last_update']}")
            else:
                print("   单用户格式:")
                print(f"   - {data.get('display_name', 'N/A')}: {data.get('name', 'N/A')}")
        else:
            print(f"❌ 获取用户状态失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 连接错误: {e}")
    
    # 测试4: 获取特定用户状态
    print("\n4. 测试特定用户状态接口 GET /query?user=木头")
    try:
        response = requests.get(f"{base_url}/query?user=木头")
        if response.status_code == 200:
            data = response.json()
            print("✅ 木头状态获取成功")
            print(f"   用户: {data.get('display_name', 'N/A')} {data.get('emoji', '')}")
            print(f"   状态: {data.get('name', 'N/A')} - {data.get('description', 'N/A')}")
            print(f"   最后更新: {data.get('last_update', 'N/A')}")
        else:
            print(f"❌ 获取木头状态失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 连接错误: {e}")
    
    # 测试5: 获取历史记录
    print("\n5. 测试历史记录接口 GET /history")
    try:
        response = requests.get(f"{base_url}/history")
        if response.status_code == 200:
            data = response.json()
            print("✅ 历史记录获取成功")
            print(f"   共有 {data.get('total', 0)} 条记录")
            
            if data.get('history'):
                print("   最近记录:")
                for item in data['history'][:3]:
                    print(f"   - {item['display_name']} {item['emoji']}: {item['name']}")
                    print(f"     时间: {item['timestamp']}")
        else:
            print(f"❌ 获取历史记录失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 连接错误: {e}")
    
    # 测试6: 设置状态 (仅测试，不实际设置)
    print("\n6. 测试状态设置接口 (仅验证参数)")
    test_params = {
        'secret': 'birthday2024',
        'status': '2',
        'user': '木头'
    }
    
    print(f"   测试参数: {test_params}")
    print("   (实际测试时请手动调用以避免改变状态)")
    
    print("\n" + "=" * 50)
    print("🎉 API测试完成!")
    print("\n💡 提示:")
    print("   - 如果看到连接错误，请确保Flask服务器正在运行")
    print("   - 运行命令: python app.py")
    print("   - 服务器地址: http://127.0.0.1:5000")
    print("   - 前端可以使用 fetch('/query') 获取所有用户状态")

if __name__ == "__main__":
    test_api() 