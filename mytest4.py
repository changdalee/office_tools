from ofdpy import OFDReader

# 打开OFD文件
with OFDReader("input.ofd") as reader:
    # 获取文档信息
    doc_info = reader.document_info
    print(f"标题: {doc_info.title}")
    print(f"作者: {doc_info.author}")
    print(f"页数: {len(reader.pages)}")

    # 读取第一页内容
    if reader.pages:
        page = reader.pages[0]
        print("\n第一页内容:")
        for text in page.texts:
            print(text.content)
