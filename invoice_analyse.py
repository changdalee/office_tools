# 发票识别导入pypdf库
from pypdf import PdfReader

# 正则表达式规则匹配pdf文件的特定字符串
import re

# 用于重命名
import os

# import shutil

# 运行结果保存到excel
import pandas as pd

from pathlib import Path


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"Hi, {name}")  # Press F9 to toggle the breakpoint.


def has_negative(float_list):
    for num in float_list:
        if num < 0:
            return True
    return False


def invoice_train(text, df):
    last_year = text.rfind("年")
    last_month = text.rfind("月")
    # print(last_month - last_year)
    if last_month - last_year > 3:
        year = text[(last_year - 5) : (last_year - 1)]
        # print(year)
        month = text[(last_month - 3) : (last_month - 1)]
        # print(month)
        day = text[(last_month + 2) : (last_month + 4)]
        # print(day)
    else:
        year = text[(last_year - 4) : (last_year)]
        # print(year)
        month = text[(last_month - 2) : (last_month)]
        # print(month)
        day = text[(last_month + 1) : (last_month + 3)]
        # print(day)

    pos_fapiao = text.find("发票号码")
    # print(text[pos_fapiao + 5])
    if text[pos_fapiao + 5] == ":":
        invoice_num = re.findall(r"发票号码 [:：]\s*(\d+)", text)[0]
        # print(invoice_num)
    else:
        invoice_num = re.findall(r"发票号码[:：]\s*(\d+)", text)[0]
        # print(invoice_num)

    # print(f"invoice_num：{invoice_num}")
    fapiao_num = ""
    # print(f"fapiao_num：{fapiao_num}")

    invoice_day = f"{year}.{month}.{day}"
    # print(f"invoice_day：{invoice_day}")
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
    min_amount = min(amounts)
    # print(f"max_amount：{max_amount}")
    tax = min_amount
    tax = f"{tax:.2f}"
    # print(f"tax：{tax}")
    deduction = tax
    buyer_num = re.findall(r"中国水电基础局有限公司\s*(\d+)", text)
    # print(buyer_num[0])
    if buyer_num:
        buyer_num = buyer_num[0]
    else:
        buyer_num = "911202221030604602"
    # print(f"buyer_num：{buyer_num}")

    # new_file = f"{file_name}-{max_amount:.2f}.pdf"
    # new_file_path = os.path.join(output_path, new_file)
    # print(f"新文件名：{new_file_path}")
    # shutil.copy2(pdf_file_path, new_file_path)
    new_row = {
        "file_name": file_name,
        "数电票号码": invoice_num,
        "发票号码": fapiao_num,
        "开票日期": invoice_day,
        "金额": max_amount,
        "票面税额": tax,
        "有效抵扣税额": deduction,
        "购买方识别号": buyer_num,
    }
    # print(f"新数据-{new_file}：{new_row}")
    df.loc[len(df)] = new_row


# *****************************************************************************


def invoice_highway(text, df):
    last_year = text.rfind("年")
    fapiao_num = text[(last_year - 13) : (last_year - 5)]
    # print(f"fapiao_num：{fapiao_num}")
    invoice_num = text[(last_year - 26) : (last_year - 14)]
    # print(f"invoice_num：{invoice_num}")
    year = re.search(r"[\d.-]+年[\d.-]+", text)
    # print(year[0][:4])
    month = re.findall(r"年\s*(\d{2})", text)
    # print(month[0])
    day = re.findall(r"月\s*(\d{2})", text)
    # print(day[0])
    invoice_day = f"{year[0][:4]}.{month[0]}.{day[0]}"
    # print(f"invoice_day：{invoice_day}")
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
        min_amount = min(amounts)
    # print(f"max_amount：{max_amount}")
    tax = min_amount
    tax = f"{tax:.2f}"
    # print(f"tax：{tax}")
    deduction = tax
    buyer_num = re.findall(r"中国水电基础局有限公司\s*(\d+)", text)
    # print(buyer_num[0])
    if buyer_num:
        buyer_num = buyer_num[0]
    else:
        buyer_num = ""
    # print(f"buyer_num：{buyer_num}")

    # new_file = f"{file_name}-{max_amount:.2f}.pdf"
    # new_file_path = os.path.join(output_path, new_file)
    # print(f"新文件名：{new_file_path}")
    # shutil.copy2(pdf_file_path, new_file_path)
    new_row = {
        "file_name": file_name,
        "数电票号码": invoice_num,
        "发票号码": fapiao_num,
        "开票日期": invoice_day,
        "金额": max_amount,
        "票面税额": tax,
        "有效抵扣税额": deduction,
        "购买方识别号": buyer_num,
    }
    # print(f"新数据-{new_file}：{new_row}")
    df.loc[len(df)] = new_row


# *****************************************************************************


def invoice_vat(text, df):
    last_year = text.find("年")
    invoice_num = text[(last_year - 25) : (last_year - 5)]
    # print(f"invoice_num：{invoice_num}")
    fapiao_num = ""
    # print(f"fapiao_num：{fapiao_num}")
    last_month = text.find("月")
    if last_month - last_year > 3:
        year = text[(last_year - 5) : (last_year - 1)]
    else:
        year = text[(last_year - 4) : (last_year)]
    # print(year)
    month = re.findall(r"年\s*(\d{2})", text)
    # print(month[0])
    day = re.findall(r"月\s*(\d{2})", text)
    # print(day[0])
    invoice_day = f"{year}.{month[0]}.{day[0]}"
    # print(f"invoice_day：{invoice_day}")
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
    min_amount = min(amounts)
    # print(f"max_amount：{max_amount}")
    tax = min_amount
    tax = f"{tax:.2f}"
    # print(f"tax：{tax}")
    deduction = tax
    buyer_num = re.findall(r"中国水电基础局有限公司\s*(\d+)", text)
    # print(buyer_num[0])
    if buyer_num:
        buyer_num = buyer_num[0]
    else:
        buyer_num = "911202221030604602"
    # print(f"buyer_num：{buyer_num}")

    # new_file = f"{file_name}-{max_amount:.2f}.pdf"
    # new_file_path = os.path.join(output_path, new_file)
    # print(f"新文件名：{new_file_path}")
    # shutil.copy2(pdf_file_path, new_file_path)
    new_row = {
        "file_name": file_name,
        "数电票号码": invoice_num,
        "发票号码": fapiao_num,
        "开票日期": invoice_day,
        "金额": max_amount,
        "票面税额": tax,
        "有效抵扣税额": deduction,
        "购买方识别号": buyer_num,
    }
    # print(f"新数据-{new_file}：{new_row}")
    df.loc[len(df)] = new_row


# *****************************************************************************

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

    df = pd.DataFrame(
        columns=[
            "file_name",
            "数电票号码",
            "发票号码",
            "开票日期",
            "金额",
            "票面税额",
            "有效抵扣税额",
            "购买方识别号",
        ]
    )

    # 遍历输入路径下的所有文件
    for file in os.listdir(input_path):
        if file.endswith(".pdf"):
            file_name = file.split(".")[0]
            # print(f"原文件名：{file_name}.pdf")
            pdf_file_path = os.path.join(input_path, file)
            # print(f"当前处理文件：{pdf_file_path}")
            # 打开 PDF 文件
            with open(pdf_file_path, "rb") as file:  # 以二进制模式打开文件
                pdf_reader = PdfReader(pdf_file_path)  # 创建 PDF 阅读器对象
                # 获取 PDF 页数
                num_pages = len(pdf_reader.pages)  # 获取 PDF 文件总页数
                # print(f"总页数: {num_pages}")  # 打印总页数
                page = pdf_reader.pages[0]
                text = page.extract_text()
                # print(text)

                # 发票金额栏能有2种¥￥开头以及1种未识别到的情况，所以需要匹配[¥￥\n]3种字符
                # 匹配能够独立识别的浮点数
                count = text.count("\x0c")
                if count > 1:
                    print(
                        f"注意：{pdf_file_path}可能有多张电子发票或存在备注页，为最大程度避免您的资金损失，建议手动重命名。"
                    )
                if "铁路" in text:
                    invoice_train(text, df)
                    print(f"{file_name}.pdf 处理完成")
                elif "通行费" in text:
                    invoice_highway(text, df)
                    print(f"{file_name}.pdf 处理完成")
                elif "增值税专用发票" in text:
                    invoice_vat(text, df)
                    print(f"{file_name}.pdf 处理完成")
                else:
                    print(
                        f"{file_name}.pdf 文件是其他发票类型，暂不支持, 请联系开发人员:李昌达,16621318031"
                    )
                    # exit(1)

    df.to_excel(output_path + "\\invoice_analyse.xlsx", index=False)
    print(f"Congratulations! the invoice_analyse.xlsx 已经保存完成")
