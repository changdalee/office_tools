import fitz  # PyMuPDF
import os
from ofdparser import OfdDocument  # 需安装ofdparser库


def ofd_to_pdf(ofd_file_path, pdf_file_path):
    """
    将OFD文件转换为PDF格式
    :param ofd_file_path: 输入的OFD文件路径
    :param pdf_file_path: 输出的PDF文件路径
    """
    if not os.path.exists(ofd_file_path):
        raise FileNotFoundError(f"OFD文件不存在: {ofd_file_path}")

    # 读取OFD文件
    ofd_doc = OfdDocument(ofd_file_path)
    pdf_doc = fitz.open()

    # 逐页转换
    for page_number in range(len(ofd_doc.pages)):
        ofd_page = ofd_doc.get_page(page_number)
        pdf_page = pdf_doc.new_page(width=ofd_page.width, height=ofd_page.height)
        pdf_page.show_pdf_page(pdf_page.rect, ofd_doc.get_pdf_from_page(page_number))

    # 保存PDF
    pdf_doc.save(pdf_file_path)
    pdf_doc.close()


if __name__ == "__main__":
    try:
        ofd_to_pdf("input.ofd", "output.pdf")
        print("转换成功！")
    except Exception as e:
        print(f"转换失败: {e}")
