import pandas as pd
import os
from pathlib import Path
from easyofd.ofd import OFD
from pypdf import PdfReader
import zipfile
import xmltodict
from pyofd import OFDConverter


def parse_ofd(ofd_path, temp_dir):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # 解压OFD文件
    xml_path = unzip_ofd(ofd_path, temp_dir)

    # 解析XML内容
    with open(xml_path, "r", encoding="utf-8") as f:
        data = xmltodict.parse(f.read())

    # 清理临时文件
    os.remove(xml_path)
    # os.rmdir(temp_dir)

    return data


def unzip_ofd(ofd_path, output_dir):
    with zipfile.ZipFile(ofd_path, "r") as z:
        z.extractall(output_dir)
    return os.path.join(output_dir, "OFD.xml")


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
            print(f"OFD文件路径：{ofd_file_path}")

            converter = OFDConverter()
            converter.convert("input.ofd", "output.pdf")

            # pdf_file_path = os.path.join(input_path, f"{file_name}.pdf")
            print(f"当前正在处理文件：{ofd_file_path}")
            # 打开 PDF 文件
            with open(pdf_file_path, "rb") as file:  # 以二进制模式打开文件
                pdf_reader = PdfReader(pdf_file_path)  # 创建 PDF 阅读器对象
                # 获取 PDF 页数
                num_pages = len(pdf_reader.pages)  # 获取 PDF 文件总页数
                # print(f"总页数: {num_pages}")  # 打印总页数
                page = pdf_reader.pages[0]
                text = page.extract_text()
                print(text)
                ofd = OFD(pdf_file_path)
                print(ofd.get_text())  # 提取全文
