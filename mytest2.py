# encoding: utf-8
import pandas as pd
import zipfile
import xmltodict
import requests
import os
from pathlib import Path
import shutil


def unzip_file(zip_path, unzip_path=None):
    """
    :param zip_path: ofd格式文件路径
    :param unzip_path: 解压后的文件存放目录
    :return: unzip_path
    """
    if not unzip_path:
        unzip_path = zip_path.split(".")[0]
    with zipfile.ZipFile(zip_path, "r") as f:
        for file in f.namelist():
            f.extract(file, path=unzip_path)
    return unzip_path


def parse_ofd(content, path):
    """
    :param content: ofd文件字节内容
    :param path: ofd文件存取路径
    """
    print(f"ofd文件路径：{path}")
    with open(path, "wb") as f:
        f.write(content)
    file_path = unzip_file(path)
    xml_path = f"{file_path}/OFD.xml"
    data_dict = {}
    with open(xml_path, "r", encoding="utf-8") as f:
        _text = f.read()
        tree = xmltodict.parse(_text)
        # 以下解析部分
        for row in tree["ofd:OFD"]["ofd:DocBody"]["ofd:DocInfo"]["ofd:CustomDatas"][
            "ofd:CustomData"
        ]:
            data_dict[row["@Name"]] = row.get("#text")
    shutil.rmtree(file_path)
    # os.remove(path)
    return data_dict


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
}
ofd_url = "http://222.143.33.74/spyx_api/storage/upload/qianzhang/988d08768b3d462fa16de7a5c62722e0.ofd"
res = requests.get(ofd_url, headers=headers)
_data_dict = parse_ofd(res.content, f'E://{ofd_url.split("/")[-1]}')
print(_data_dict)

"""
if __name__ == "__main__":
    # 对pandas配置，列名与数据对其显示
    pd.set_option("display.unicode.ambiguous_as_wide", True)
    pd.set_option("display.unicode.east_asian_width", True)
    # 显示所有列
    pd.set_option("display.max_columns", None)
    # 显示所有行
    # pd.set_option('display.max_rows', None)

    print(f"PyCharm")

    current_path = os.path.dirname(os.path.abspath(__file__))
    input_path = current_path + "\\input"
    if Path(input_path).is_dir():
        print(f"输入路径：{input_path} 已经存在")
    else:
        print(f"输入路径：{input_path} 不存在")
        os.makedirs(input_path)
        print(f"输入路径：{input_path} 创建成功")
    output_path = current_path + "\\output"
    if Path(output_path).is_dir():
        print(f"输出路径：{output_path} 已经存在")
    else:
        print(f"输入路径：{output_path} 不存在")
        os.makedirs(output_path)
        print(f"输入路径：{output_path} 创建成功")

    # 遍历输入路径下的所有文件
    for file in os.listdir(input_path):
        print(f"当前正在处理文件：{file}")
        if file.endswith(".ofd"):
            file_name = file.split(".")[0]
            print(f"原文件名：{file_name}")
            ofd_file_path = os.path.join(input_path, f"{file_name}.ofd")

            # pdf_file_path = os.path.join(input_path, f"{file_name}.pdf")
            print(f"当前正在处理文件：{ofd_file_path}")
            data_dict = parse_ofd(_text, ofd_file_path)
            print(data_dict)
"""
