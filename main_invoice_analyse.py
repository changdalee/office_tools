# 发票识别导入pypdf库
from pypdf import PdfReader

# 正则表达式规则匹配pdf文件的特定字符串
import re

# 用于重命名
import os
import shutil

# 运行结果保存到excel
import pandas as pd


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {name}")  # Press F9 to toggle the breakpoint.


def has_negative(float_list):
    for num in float_list:
        if num < 0:
            return True
    return False


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    # 对pandas配置，列名与数据对其显示
    pd.set_option("display.unicode.ambiguous_as_wide", True)
    pd.set_option("display.unicode.east_asian_width", True)
    # 显示所有列
    pd.set_option("display.max_columns", None)
    # 显示所有行
    # pd.set_option('display.max_rows', None)

    print_hi("PyCharm")

    # file = "D:\\develops\\python\\office_tools\\503280.0.pdf"
    current_path = os.path.dirname(os.path.abspath(__file__))
    input_path = current_path + "\\input"
    output_path = current_path + "\\output"

    # print(f"当前路径：{current_path}")
    # print(f"输入路径：{input_path}")
    # print(f"输出路径：{output_path}")
    df = pd.DataFrame(columns=["file_name", "invoice_num", "money"])

    # 遍历输入路径下的所有文件
    for file in os.listdir(input_path):
        if file.endswith(".pdf"):
            file_name = file.split(".")[0]
            print(f"原文件名：{file_name}.pdf")
            pdf_file_path = os.path.join(input_path, file)
            print(f"当前处理文件：{pdf_file_path}")
            # 打开 PDF 文件
            with open(pdf_file_path, "rb") as file:  # 以二进制模式打开文件
                pdf_reader = PdfReader(pdf_file_path)  # 创建 PDF 阅读器对象
                # 获取 PDF 页数
                num_pages = len(pdf_reader.pages)  # 获取 PDF 文件总页数
                # print(f"总页数: {num_pages}")  # 打印总页数
                page = pdf_reader.pages[0]
                text = page.extract_text()
                # print(text)

                if not (("发票" in text) or ("收费票据" in text) or ("通行票" in text)):
                    print(
                        f"注意：{pdf_file_path}可能不是电子发票原件。如果确认是电子发票原件，请发送报错文件给16923071@qq.com"
                    )
                else:
                    # 发票金额栏能有2种¥￥开头以及1种未识别到的情况，所以需要匹配[¥￥\n]3种字符
                    # 匹配能够独立识别的浮点数
                    count = text.count("\x0c")
                    if count > 1:
                        print(
                            f"注意：{pdf_file_path}可能有多张电子发票或存在备注页，为最大程度避免您的资金损失，建议手动重命名。"
                        )
                    invoice_num = re.findall(r"发票号码[::\n]\s*(\d+)", text)
                    amounts = re.findall(r"[¥￥\n]\s*([-]?\d+\.\d{2})", text)
                    amounts2 = re.findall(r"[¥￥]\s*(\d+\.\d{2})", text)
                    max_amount = 0
                    # 如果识别到2个人民币字符 且金额不相同的情况，定义为异常发票
                    # 通常来说，要么只有1个人民币字符，要么3个金额，1个含税，1个不含税，1个税费，甚至更多个的情况。
                    if len(amounts2) == 2 and len(set(amounts2)) == 2:
                        print(
                            f"警告：{pdf_file_path}中识别到有效¥字符的金额异常，请手动检查文件以确保所有金额都已正确识别。"
                        )

                    if amounts:
                        amounts = [float(x) for x in amounts]
                        # 通常情况都是取金额最大的，除非有负数出现，那样就再做一轮筛选，用人民币字符去筛选出来。
                        if has_negative(amounts):
                            if not amounts2:
                                print(
                                    f"警告：没有找到相关票面金额，暂时无法识别。恳请您把报错文件:{file}发送到16923071@qq.com"
                                )
                            else:
                                amounts = [float(x) for x in amounts2]
                        max_amount = max(amounts)
                        # print(f"最大金额为：{max_amount}")
                        # new_file = f'{file[:-4]}_{max_amount}.pdf'
                        # new_file = f"{max_amount}.pdf"
                        new_file = f"{file_name}.pdf"
                        new_file_path = os.path.join(output_path, new_file)
                        print(f"新文件名：{new_file_path}")
                        shutil.copy2(pdf_file_path, new_file_path)
                        new_row = {
                            "file_name": file,
                            "invoice_num": invoice_num,
                            "money": max_amount,
                        }
                        print(new_row)
                        # print(df)
                        df.loc[len(df)] = new_row
                        # print(df)
            df.to_excel(output_path + "\\invoice_analyse.xlsx", index=False)
