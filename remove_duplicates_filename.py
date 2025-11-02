import os
from collections import defaultdict
from pathlib import Path


def find_duplicates_by_name_and_size(folder_path):
    """通过文件名和文件大小识别重复文件"""
    files_map = defaultdict(list)

    for root, _, files in os.walk(folder_path):
        for filename in files:
            filepath = Path(root) / filename
            try:
                file_size = os.path.getsize(filepath)
                # 使用文件名+大小作为唯一标识
                file_key = (filename.lower(), file_size)
                files_map[file_key].append(filepath)
            except OSError:
                continue

    # 只返回重复项（值列表长度>1的项）
    return {k: v for k, v in files_map.items() if len(v) > 1}


def delete_duplicates(duplicates_dict, dry_run=False):
    """处理重复文件（保留第一个，删除后续）"""
    deleted_count = 0

    for (name, size), paths in duplicates_dict.items():
        print(f"\n发现重复文件: {name} ({size} bytes)")
        print(f"原始文件: {paths[0]}")

        for dup in paths[1:]:
            if dry_run:
                print(f"[模拟] 将删除: {dup}")
            else:
                try:
                    os.remove(dup)
                    print(f"已删除: {dup}")
                    deleted_count += 1
                except Exception as e:
                    print(f"删除失败 {dup}: {str(e)}")

    print(f"\n操作完成，共删除 {deleted_count} 个重复文件")


if __name__ == '__main__':
    import argparse
    '''
    parser = argparse.ArgumentParser(description='快速删除重复文件工具')
    parser.add_argument('D:\\BaiduNetdiskDownload\\2025中经-建筑', help='要扫描的文件夹路径')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行模式')
    args = parser.parse_args()
    '''
    remove_dir="D:\\BaiduNetdiskDownload"
    duplicates = find_duplicates_by_name_and_size(remove_dir)
    if duplicates:
        delete_duplicates(duplicates)
    else:
        print("未发现重复文件")
