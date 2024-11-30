import fitz  # PyMuPDF
import argparse
import os
import datetime

def is_page_empty(page):
    """检查页面是否为空"""
    text = page.get_text()
    images = page.get_images(full=True)
    if not text.strip() and not images:
        return True
    return False

def create_blank_pdf_page(width, height):
    """创建一个包含一个空白页面的 PDF 文档"""
    doc = fitz.open()  # 创建一个新的 PDF 文档
    doc.new_page(width=width, height=height)
    return doc

def split_pdf_vertically(input_pdf_path, output_pdf_path, offset=28.35):  # 1 cm 大约是 28.35 点
    # 打开原始 PDF 文件
    input_pdf = fitz.open(input_pdf_path)
    
    # 创建一个新的 PDF 文件用于保存分割后的页面
    output_pdf = fitz.open()

    for page_num in range(len(input_pdf)):
 
        page = input_pdf[page_num]

        if is_page_empty(page):
            # print(f'Page {page_num} is empty. doing...')

            # 创建两页空白页
            upper_blank_page = create_blank_pdf_page(rect.width, rect.height / 2 + offset)
            lower_blank_page = create_blank_pdf_page(rect.width, rect.height / 2 - offset)

            output_pdf.insert_pdf(upper_blank_page)
            output_pdf.insert_pdf(lower_blank_page)

            continue

        rect = page.rect
        rotate = page.rotation

        # 计算中点
        mid_y = rect.height / 2

        # 定义上下两部分的矩形区域
        upper_rect = fitz.Rect(rect.x0, rect.y0, rect.x1, mid_y + offset)
        lower_rect = fitz.Rect(rect.x0, mid_y - offset, rect.x1, rect.y1)
        

        # 根据页面的旋转角度，调整插入顺序
        if rotate == 180:  # 倒置方向

            # 插入下半部分
            lower_page = output_pdf.new_page(width=rect.width, height=lower_rect.height)
            lower_page.show_pdf_page(lower_page.rect, input_pdf, page_num, clip=lower_rect, rotate=rotate)

            # 插入上半部分
            upper_page = output_pdf.new_page(width=rect.width, height=upper_rect.height)
            upper_page.show_pdf_page(upper_page.rect, input_pdf, page_num, clip=upper_rect, rotate=rotate)
            
        elif rotate == 0 :  # 正常方向

            # 插入上半部分
            upper_page = output_pdf.new_page(width=rect.width, height=upper_rect.height)
            upper_page.show_pdf_page(upper_page.rect, input_pdf, page_num, clip=upper_rect, rotate=rotate)

            # 插入下半部分
            lower_page = output_pdf.new_page(width=rect.width, height=lower_rect.height)
            lower_page.show_pdf_page(lower_page.rect, input_pdf, page_num, clip=lower_rect, rotate=rotate)

    # 处理书签
    copy_bookmarks(input_pdf, output_pdf)

    # 保存输出 PDF 文件
    output_pdf.save(output_pdf_path)

   

def copy_bookmarks(input_pdf, output_pdf):
    toc = input_pdf.get_toc()

    #print("TOC:", toc)  # 添加这行打印书签目录

    new_toc = []

    for item in toc:
        level, title, page = item

        # 原来页码 x 的书签，强制复制到新 PDF 中页码 2x-1 的地方
        new_toc.append([level, title, 2 * page-1])

    output_pdf.set_toc(new_toc)

def main():
    parser = argparse.ArgumentParser(description="Split PDF pages vertically.")
    parser.add_argument("--input", help="Path to the input PDF file")
    parser.add_argument("--output", default="", help="Path to the output PDF file")
    parser.add_argument("--offset", type=float, default=8, help="Vertical offset in points (default: 28.35 for 1 cm)")

    args = parser.parse_args()

    # 如果没有提供输出路径，则生成默认路径
    if args.output == "":
        input_file_name = os.path.basename(args.input)
        file_name, file_ext = os.path.splitext(input_file_name)
        timestamp = datetime.datetime.now().strftime("%Y_%m%d_%H_%M_%S")
        output_dir = "split"
        os.makedirs(output_dir, exist_ok=True)
        output_file_name = f"{file_name}-split_{timestamp}{file_ext}"
        output_pdf_path = os.path.join(output_dir, output_file_name)
    else:
        output_pdf_path = args.output

    split_pdf_vertically(args.input, output_pdf_path, args.offset)

if __name__ == "__main__":
    main()
