#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动GUI版本的状态监控程序
"""

import sys
import os

# 确保可以导入其他模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from status_monitor_gui import main
    main()
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖都已安装")
    input("按回车键退出...")
except Exception as e:
    print(f"启动错误: {e}")
    input("按回车键退出...") 