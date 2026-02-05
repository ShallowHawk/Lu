import time
import requests
import sys

# 配置
SERVER_URL = "http://101.43.113.154/api/status/update" # 部署后改为服务器IP
SECRET = "my_love_secret_2024"
USER_KEY = "mutou" # 或者 'qianyu'

def update_status(name, description, is_online=True):
    try:
        data = {
            "secret": SECRET,
            "user_key": USER_KEY,
            "name": name,
            "description": description,
            "is_online": is_online
        }
        res = requests.post(SERVER_URL, json=data)
        if res.status_code == 200:
            print(f"[{time.strftime('%H:%M:%S')}] 状态更新成功: {name}")
        else:
            print(f"状态更新失败: {res.text}")
    except Exception as e:
        print(f"连接错误: {e}")

def main():
    print("启动状态监控...")
    print("请输入当前状态 (Ctrl+C 退出)")
    
    # 简单的交互式更新
    while True:
        try:
            print("\n选择当前状态:")
            print("1. 勤勉工作")
            print("2. 摸鱼中")
            print("3. 游戏中")
            print("4. 休息中")
            print("5. 自定义")
            
            choice = input("请输入选项: ")
            
            if choice == '1':
                update_status("勤勉", "为了买猫粮努力工作中")
            elif choice == '2':
                update_status("摸鱼", "刷B站中，勿扰~")
            elif choice == '3':
                update_status("游戏", "在海拉鲁大陆探险")
            elif choice == '4':
                update_status("休息", "呼呼大睡中...")
            elif choice == '5':
                name = input("输入状态名称: ")
                desc = input("输入状态描述: ")
                update_status(name, desc)
            else:
                print("无效选项")
                
        except KeyboardInterrupt:
            print("\n退出监控")
            break

if __name__ == "__main__":
    main()
