from easyofd import OFD
import os

if __name__ == "__main__":
    # 单文件转换
    ofd = OFD("D:\\develops\\python\\office_tools\\input\\input.ofd")
    ofd.to_pdf(ofd)  # 转换PDF
    ofd.to_image("output_dir", dpi=300)  # 导出图片