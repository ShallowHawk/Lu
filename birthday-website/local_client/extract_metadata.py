import os
import exifread
from datetime import datetime
import json

IMAGE_DIR = r"D:\LinLu\birthday-website\public\images"

def get_image_date(file_path):
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            
            # 尝试获取拍摄时间
            date_str = None
            if 'EXIF DateTimeOriginal' in tags:
                date_str = str(tags['EXIF DateTimeOriginal'])
            elif 'Image DateTime' in tags:
                date_str = str(tags['Image DateTime'])
                
            if date_str:
                # EXIF 日期格式通常为 YYYY:MM:DD HH:MM:SS
                try:
                    dt = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    return dt.strftime('%Y.%m.%d')
                except ValueError:
                    pass
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return None

def main():
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    image_data = []
    
    for filename in image_files:
        if 'avatar' in filename: continue # 跳过头像
        
        file_path = os.path.join(IMAGE_DIR, filename)
        date_str = get_image_date(file_path)
        
        # 如果没有EXIF信息，尝试从文件名解析（很多手机照片文件名包含日期）
        # 或者使用文件修改时间作为兜底
        if not date_str:
            try:
                mtime = os.path.getmtime(file_path)
                dt = datetime.fromtimestamp(mtime)
                date_str = dt.strftime('%Y.%m.%d')
            except:
                date_str = '未知日期'
        
        image_data.append({
            'filename': filename,
            'date': date_str,
            'path': file_path
        })
    
    # 按日期排序
    image_data.sort(key=lambda x: x['date'])
    
    print(json.dumps(image_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
