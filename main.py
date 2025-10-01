# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pypdf import PdfReader

# 正则表达式规则匹配pdf文件的特定字符串
import re

# 用于重命名
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {name}")  # Press F9 to toggle the breakpoint.


def has_negative(float_list):
    for num in float_list:
        if num < 0:
            return True
    return False


def pdf_analyse_and_rename(pdf_reader, pdf_file_path, out_path):
    # reader = PdfReader(file)
    number_of_pages = len(pdf_reader.pages)
    page = pdf_reader.pages[0]
    text = page.extract_text()
    # print(text)

    if not (("发票" in text) or ("收费票据" in text)):
        return (
            f"注意：{pdf_file_path}可能不是电子发票原件。如果确认是电子发票原件，请发送报错文件给limengcheng@akic.tech",
            "warning",
        )
    else:
        # 发票金额栏能有2种¥￥开头以及1种未识别到的情况，所以需要匹配[¥￥\n]3种字符
        # 匹配能够独立识别的浮点数
        count = text.count("\x0c")
        if count > 1:
            return (
                f"注意：{pdf_file_path}可能有多张电子发票或存在备注页，为最大程度避免您的资金损失，建议手动重命名。",
                "warning",
            )
        amounts = re.findall(r"[¥￥\n]\s*([-]?\d+\.\d{2})", text)
        amounts2 = re.findall(r"[¥￥]\s*(\d+\.\d{2})", text)
        max_amount = 0
        # 如果识别到2个人民币字符 且金额不相同的情况，定义为异常发票
        # 通常来说，要么只有1个人民币字符，要么3个金额，1个含税，1个不含税，1个税费，甚至更多个的情况。
        if len(amounts2) == 2 and len(set(amounts2)) == 2:
            return (
                f"警告：{pdf_file_path}中识别到有效¥字符的金额异常，请手动检查文件以确保所有金额都已正确识别。",
                "warning",
            )

        if amounts:
            amounts = [float(x) for x in amounts]
            # 通常情况都是取金额最大的，除非有负数出现，那样就再做一轮筛选，用人民币字符去筛选出来。
            if has_negative(amounts):
                if not amounts2:
                    return (
                        f"警告：没有找到相关票面金额，暂时无法识别。恳请您把报错文件:{file}发送到limengcheng@akic.tech",
                        "warning",
                    )
                else:
                    amounts = [float(x) for x in amounts2]
            max_amount = max(amounts)
            print(f"最大金额为：{max_amount}")
            # new_file = f'{file[:-4]}_{max_amount}.pdf'
            new_file = f"{max_amount}.pdf"
            print(f"新文件名：{new_file}")
            print(f"当前文件名：{pdf_file_path}")
            os.chdir(pdf_file_path)
            print(f"是否存在同名文件：{os.path.exists(new_file)}")
            print(f"当前工作目录：{os.getcwd()}")
            # 这里重命名情况比较罕见
            if os.path.exists(new_file):
                return (f"重命名失败！该目录下已有同名文件{new_file}", "warning")
            else:
                try:
                    # 更改PDF文件名称
                    os.renames(pdf_file_path, new_file)
                    os.system("copy " + new_file + " " + out_path)  # Windows
                    return (f"重命名成功！{new_file}", "message")
                except OSError as e:
                    # 捕捉异常并执行相应的操作
                    if e.errno == 63:
                        return (
                            f"发生未知错误{e}，可能是文件名太长无法重命名，请尝试缩短文件名或使用缩写",
                            "warning",
                        )
                    else:
                        return (
                            f"发生未知错误{e}，有可能是因为你打开了某个pdf，请关闭后重试",
                            "warning",
                        )
        else:
            return (f"{file}没有识别到该发票的相关金额。", "warning")


def create_folder(folder_path):
    """
    创建指定路径的文件夹
    :param folder_path: 要创建的文件夹路径
    :return: 返回创建结果信息
    """
    try:
        os.makedirs(folder_path, exist_ok=True)
        return f"文件夹 '{folder_path}' 创建成功"
    except Exception as e:
        return f"创建文件夹失败: {str(e)}"


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print_hi("PyCharm")

    # file = "D:\\develops\\python\\office_tools\\503280.0.pdf"
    file = "503280.0.pdf"
    # 打开 PDF 文件
    pdf_file_path = file  # 指定 PDF 文件路径
    with open(pdf_file_path, "rb") as file:  # 以二进制模式打开文件
        pdf_reader = PdfReader(pdf_file_path)  # 创建 PDF 阅读器对象

    # 获取 PDF 页数
    num_pages = len(pdf_reader.pages)  # 获取 PDF 文件总页数
    print(f"总页数: {num_pages}")  # 打印总页数
    # print(pdf_reader.pages[0].extract_text())  # 提取第一页文本
    current_path = os.path.dirname(os.path.abspath(__file__))
    # print(current_path)
    out_path = current_path + "\output"
    # print(out_path)
    result = create_folder(out_path)
    # print(result)

    pdf_analyse_and_rename(pdf_reader, pdf_file_path, out_path)
