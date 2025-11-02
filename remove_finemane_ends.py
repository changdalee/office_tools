import os
import re
import sys

def remove_trailing_number(folder_path):
    """去除文件名末尾的(1)等重复标记"""
    for filename in os.listdir(folder_path):
        # 方法1：字符串替换（适用于固定格式）
        new_name = filename.replace(' (1)', '').replace('(1)', '')

        # 方法2：正则表达式（更通用）
        new_name = re.sub(r'\(\d+\)$', '', new_name).strip()

        if new_name != filename:
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(f'Renamed: {filename} -> {new_name}')


if __name__ == '__main__':
    target_dir = "D:\\BaiduNetdiskDownload\\2025中经-建筑"
    if not os.path.isdir(target_dir):
        print(f"错误: {target_dir} 不是有效目录")
        sys.exit(1)
    remove_trailing_number(target_dir)