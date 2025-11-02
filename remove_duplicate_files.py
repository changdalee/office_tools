import os
import hashlib
import sys

def calculate_md5(filepath):
    """计算文件MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def find_duplicates(root_dir):
    """查找重复文件并返回待删除列表"""
    hashes = {}
    duplicates = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                file_hash = calculate_md5(filepath)
                if file_hash in hashes:
                    duplicates.append(filepath)
                else:
                    hashes[file_hash] = filepath
            except (IOError, PermissionError) as e:
                print(f"跳过无法读取的文件: {filepath} - {str(e)}")

    return duplicates


def delete_with_confirmation(file_list):
    """交互式确认后删除文件"""
    for filepath in file_list:
        try:
            os.remove(filepath)
            print(f"已删除: {filepath}")
        except Exception as e:
            print(f"删除失败 {filepath}: {str(e)}")


if __name__ == "__main__":


    print("用法: python remove_duplicates.py <目录路径>")

    target_dir = "D:\\BaiduNetdiskDownload"
    if not os.path.isdir(target_dir):
        print(f"错误: {target_dir} 不是有效目录")
        sys.exit(1)


    print(f"正在扫描 {target_dir}...")
    dup_files = find_duplicates(target_dir)

    if not dup_files:
        print("未发现重复文件")
    else:
        print(f"发现 {len(dup_files)} 个重复文件")
        delete_with_confirmation(dup_files)
