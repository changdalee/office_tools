import re


def has_negative(float_list):
    for num in float_list:
        if num < 0:
            return True
    return False


text = """国 家 税 务 总 局
全
国
统
一 发 票 监
制
章
局务税省徽
安
买票请到 12306 发货请到 95306
发票号码 :25349119343000116078
Fuyangxi
G7721
2025 年 06 月 24 日
电子发票（铁路电子客票）
08:18 开 07 车 02F 号
票价 : ￥ 115.50
二等座
3412221991****0751 陈实
电子客票号 :1934366086061493257232025
中国水电基础局有限公司 统一社会信用代码 :911202221030604602
开票日期 :2025 年 06 月 25 日
Hefeinan
合肥南 站阜阳西 站
中国铁路祝您旅途愉快
购买方名称 :"""

pos_fapiao = text.find("发票号码")
print(text[pos_fapiao + 5])
if text[pos_fapiao + 5] == ":":
    invoice_num = re.findall(r"发票号码 [:：]\s*(\d+)", text)[0]
    print(invoice_num)
else:
    invoice_num = re.findall(r"发票号码[:：]\s*(\d+)", text)[0]
    print(invoice_num)
