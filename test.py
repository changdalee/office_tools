import re


def has_negative(float_list):
    for num in float_list:
        if num < 0:
            return True
    return False


text = """电子发票（增值税专用发票） 发票号码：
开票日期：
购
买
方
信
息
统一社会信用代码 / 纳税人识别号：
销
售
方
信
息
统一社会信用代码 / 纳税人识别号：
名称： 名称：
项目名称 规格型号 单  位 数  量 单  价 金  额 税率 / 征收率 税  额
合 计
价税合计（大写） （小写）
备
注
开票人：
25342000000001408441
2025 年 01 月 03 日
中国水电基础局有限公司
911202221030604602
合肥市星光荟酒店管理有限公司
91340104MA8QP2TM1N
¥ 1981.13 ¥ 118.87
贰仟壹佰圆整 ¥ 2100.00
吴怀娜
吴怀娜
* 住宿服务 * 住宿费 6%天 1981.13 118.87330.1886792452836
收款人 : 周玲丽 ;    复核人 : 曹前跃 ;    
共 1 页  第 1 页"""

last_year = text.find("年")
invoice_num = text[(last_year - 25) : (last_year - 5)]
print(f"invoice_num：{invoice_num}")
fapiao_num = ""
print(f"fapiao_num：{fapiao_num}")
year = text[(last_year - 5) : (last_year - 1)]
print(year)
month = re.findall(r"年\s*(\d{2})", text)
print(month[0])
day = re.findall(r"月\s*(\d{2})", text)
print(day[0])
invoice_day = f"{year[0][:4]}.{month[0]}.{day[0]}"
print(f"invoice_day：{invoice_day}")
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
print(f"max_amount：{max_amount}")
tax = min_amount
tax = f"{tax:.2f}"
print(f"tax：{tax}")
deduction = tax
buyer_num = re.findall(r"中国水电基础局有限公司\s*(\d+)", text)
# print(buyer_num[0])
if buyer_num:
    buyer_num = buyer_num[0]
else:
    buyer_num = ""
print(f"buyer_num：{buyer_num}")
