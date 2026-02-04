#!/usr/bin/env python3
"""
清理异常历史记录脚本
- 移除过于频繁的状态变更记录
- 保留有意义的状态变更历史
- 备份原始数据
"""

import json
import os
import shutil
from datetime import datetime, timedelta
from collections import defaultdict

def clean_history():
    """清理异常历史记录"""
    
    # 文件路径
    history_file = 'history.json'
    backup_file = f'history_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    if not os.path.exists(history_file):
        print("❌ 历史记录文件不存在")
        return
    
    # 备份原始文件
    shutil.copy2(history_file, backup_file)
    print(f"✅ 已备份原始历史记录到: {backup_file}")
    
    # 读取历史记录
    with open(history_file, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    print(f"📊 原始历史记录数量: {len(history)}")
    
    # 清理逻辑
    cleaned_history = []
    user_last_status = {}  # 记录每个用户的最后状态
    user_last_time = {}    # 记录每个用户的最后更新时间
    
    # 设置清理参数
    min_interval_seconds = 60  # 最小间隔时间（秒）
    max_changes_per_hour = 10  # 每小时最大变更次数
    
    # 按时间排序
    history.sort(key=lambda x: x['timestamp'])
    
    # 用于统计每小时变更次数
    hourly_changes = defaultdict(int)
    
    for record in history:
        try:
            user = record['user']
            status = record['status']
            timestamp_str = record['timestamp']
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            
            # 生成小时键用于统计
            hour_key = f"{user}_{timestamp.strftime('%Y%m%d_%H')}"
            
            # 检查是否需要保留这条记录
            should_keep = True
            
            # 1. 检查最小间隔时间
            if user in user_last_time:
                time_diff = (timestamp - user_last_time[user]).total_seconds()
                if time_diff < min_interval_seconds:
                    should_keep = False
            
            # 2. 检查状态是否真的发生了变化
            if user in user_last_status and user_last_status[user] == status:
                should_keep = False
            
            # 3. 检查每小时变更频率
            if hourly_changes[hour_key] >= max_changes_per_hour:
                should_keep = False
            
            # 4. 特殊时间段检查（快速连续变更）
            if user in user_last_time:
                time_diff = (timestamp - user_last_time[user]).total_seconds()
                if time_diff < 10:  # 10秒内的变更认为是异常
                    should_keep = False
            
            if should_keep:
                cleaned_history.append(record)
                user_last_status[user] = status
                user_last_time[user] = timestamp
                hourly_changes[hour_key] += 1
            
        except Exception as e:
            print(f"⚠️ 处理记录时出错: {e}")
            # 如果处理出错，保留原记录
            cleaned_history.append(record)
    
    # 进一步清理：移除明显的测试记录
    final_history = []
    for record in cleaned_history:
        timestamp = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
        
        # 移除2025-07-15 01:41:00 - 01:45:00 期间的快速测试记录
        test_start = datetime(2025, 7, 15, 1, 41, 0)
        test_end = datetime(2025, 7, 15, 1, 45, 0)
        
        if test_start <= timestamp <= test_end:
            # 这个时间段的记录太频繁，可能是测试记录
            continue
        
        final_history.append(record)
    
    print(f"📊 清理后历史记录数量: {len(final_history)}")
    print(f"📊 移除记录数量: {len(history) - len(final_history)}")
    
    # 保存清理后的历史记录
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(final_history, f, ensure_ascii=False, indent=2)
    
    print("✅ 历史记录清理完成")
    
    # 显示统计信息
    print("\n📈 清理后统计信息:")
    user_stats = defaultdict(int)
    for record in final_history:
        user_stats[record['user']] += 1
    
    for user, count in user_stats.items():
        print(f"  {user}: {count} 条记录")
    
    if final_history:
        earliest = min(final_history, key=lambda x: x['timestamp'])['timestamp']
        latest = max(final_history, key=lambda x: x['timestamp'])['timestamp']
        print(f"\n📅 时间范围: {earliest} ~ {latest}")

if __name__ == '__main__':
    clean_history()