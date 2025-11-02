import base64
import os
import sys
from easyofd.ofd import OFD
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('宋体', '方正书宋简体.ttf'))


def cvt_ofd(file_path):
    file_prefix = os.path.splitext(os.path.split(file_path)[1])[0]
    with open(file_path, "rb") as f:
        ofdb64 = str(base64.b64encode(f.read()), "utf-8")
    ofd = OFD()
    ofd.read(ofdb64, save_xml=True, xml_name=f"{file_prefix}_xml")
    pdf_bytes = ofd.to_pdf()  # 转pdf
    img_np = ofd.to_jpg()  # 转图片
    ofd.del_data()

    with open(f"{file_prefix}.pdf", "wb") as f:
        f.write(pdf_bytes)

    for idx, img in enumerate(img_np):
        img.save(f"{file_prefix}_{idx}.jpg")


if __name__ == "__main__":
    cvt_ofd("D:\\develops\\python\\office_tools\\input\\input.ofd")