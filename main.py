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


def pdf_analyse_and_rename(file):
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    print(text)

    if not (("发票" in text) or ("收费票据" in text)):
        return (
            f"注意：{file}可能不是电子发票原件。如果确认是电子发票原件，请发送报错文件给limengcheng@akic.tech",
            "warning",
        )
    else:
        # 发票金额栏能有2种¥￥开头以及1种未识别到的情况，所以需要匹配[¥￥\n]3种字符
        # 匹配能够独立识别的浮点数
        count = text.count("\x0c")
        if count > 1:
            return (
                f"注意：{file}可能有多张电子发票或存在备注页，为最大程度避免您的资金损失，建议手动重命名。",
                "warning",
            )
        amounts = re.findall(r"[¥￥\n]\s*([-]?\d+\.\d{2})", text)
        amounts2 = re.findall(r"[¥￥]\s*(\d+\.\d{2})", text)
        max_amount = 0
        # 如果识别到2个人民币字符 且金额不相同的情况，定义为异常发票
        # 通常来说，要么只有1个人民币字符，要么3个金额，1个含税，1个不含税，1个税费，甚至更多个的情况。
        if len(amounts2) == 2 and len(set(amounts2)) == 2:
            return (
                f"警告：{file}中识别到有效¥字符的金额异常，请手动检查文件以确保所有金额都已正确识别。",
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
            print(max_amount)
            # new_file = f'{file[:-4]}_{max_amount}.pdf'
            new_file = f"{max_amount}.pdf"
            # 这里重命名情况比较罕见
            if os.path.exists(new_file):
                return (f"重命名失败！该目录下已有同名文件{new_file}", "warning")
            else:
                try:
                    # 更改PDF文件名称
                    os.renames(file, new_file)
                    os.system("copy " + new_file + " " + file)  # Windows
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


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print_hi("PyCharm")

    file = (
        "dzfp_24312000000381259558_上海临港益邦智能技术股份有限公司_20241204201232.pdf"
    )
    pdf_analyse_and_rename(file)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
