"""
按照武汉理工大学本科生毕业设计（论文）模板格式化论文初稿
"""

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy
import re

INPUT_PATH = r"e:\graduate\docx\毕业论文初稿.docx"
OUTPUT_PATH = r"e:\graduate\docx\毕业论文_格式化.docx"

# 字号常量（EMU单位，1pt = 12700 EMU）
PT_XIAOER = Pt(18)  # 小二号
PT_SAN = Pt(16)  # 三号
PT_SI = Pt(14)  # 四号
PT_XIAOSI = Pt(12)  # 小四号
PT_ER = Pt(22)  # 二号（封面副标题等）

# 固定行距 = 20pt
FIXED_LINE_SPACING = Pt(20)

# 缩进2字符（小四号，2*12pt=24pt的EMU值，但用字符单位时用first_line_indent=Pt(24)）
FIRST_LINE_INDENT = Pt(24)  # 2字符 * 12pt/字符


def set_run_font(run, cn_font=None, en_font=None, size=None, bold=None):
    """设置run的字体"""
    if cn_font:
        run.font.name = cn_font
        run._element.rPr.rFonts.set(qn("w:eastAsia"), cn_font)
    if en_font:
        run.font.name = en_font
    if size:
        run.font.size = size
    if bold is not None:
        run.font.bold = bold


def set_paragraph_font(para, cn_font=None, en_font=None, size=None, bold=None):
    """对段落所有run设置字体"""
    for run in para.runs:
        if cn_font:
            run.font.name = cn_font
            run._element.rPr.rFonts.set(qn("w:eastAsia"), cn_font)
            # 同时确保西文字体
            if en_font:
                run.font.name = en_font
        if size:
            run.font.size = size
        if bold is not None:
            run.font.bold = bold


def ensure_rpr(run):
    """确保run有rPr元素"""
    rPr = run._element.get_or_add_rPr()
    return rPr


def set_run_fonts_detail(run, cn_font, en_font, size, bold=None):
    """精确设置run的中英文字体"""
    rPr = ensure_rpr(run)
    # 设置rFonts
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), en_font)
    rFonts.set(qn("w:hAnsi"), en_font)
    rFonts.set(qn("w:eastAsia"), cn_font)
    rFonts.set(qn("w:cs"), en_font)
    run.font.size = size
    if bold is not None:
        run.font.bold = bold


def format_chapter_title(para):
    """格式化章标题：黑体小二号，居中，段前后各1行（约18pt）"""
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = para.paragraph_format
    pf.space_before = Pt(18)
    pf.space_after = Pt(6)
    pf.first_line_indent = None
    pf.left_indent = None
    # 固定行距
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    for run in para.runs:
        set_run_fonts_detail(run, "黑体", "Times New Roman", PT_XIAOER, bold=True)
    # 如果段落没有run（空文本），直接设置style字体
    if not para.runs and para.text:
        run = para.add_run(para.text)
        # 清空原文
        for r in para.runs[:-1]:
            r.text = ""
        set_run_fonts_detail(run, "黑体", "Times New Roman", PT_XIAOER, bold=True)


def format_section1_title(para):
    """格式化一级节标题(X.X)：黑体三号，左对齐，段前后各8pt"""
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = para.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(8)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    for run in para.runs:
        set_run_fonts_detail(run, "黑体", "Times New Roman", PT_SAN, bold=False)


def format_section2_title(para):
    """格式化二级节标题(X.X.X)：黑体四号，左对齐，段前后各8pt"""
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = para.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(8)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    for run in para.runs:
        set_run_fonts_detail(run, "黑体", "Times New Roman", PT_SI, bold=False)


def format_body_para(para):
    """格式化正文：宋体/Times New Roman小四号，固定行距20pt，首行缩进2字符"""
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = para.paragraph_format
    pf.space_before = None
    pf.space_after = None
    pf.first_line_indent = FIRST_LINE_INDENT
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    for run in para.runs:
        set_run_fonts_detail(run, "宋体", "Times New Roman", PT_XIAOSI, bold=False)


def format_abstract_title(para, is_cn=True):
    """格式化摘要/Abstract标题"""
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = para.paragraph_format
    pf.space_before = Pt(18)
    pf.space_after = Pt(18)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    for run in para.runs:
        if is_cn:
            set_run_fonts_detail(run, "黑体", "Times New Roman", PT_XIAOER, bold=True)
        else:
            set_run_fonts_detail(run, "黑体", "Times New Roman", PT_XIAOER, bold=True)


def format_keywords_para(para, is_cn=True):
    """格式化关键词行"""
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = para.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = None
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    if is_cn:
        # "关键词：" 用黑体四号，后面内容用宋体小四号
        for run in para.runs:
            set_run_fonts_detail(run, "宋体", "Times New Roman", PT_XIAOSI, bold=False)
    else:
        # "Key Words:" 用Times New Roman粗体四号，后面用小四号
        for run in para.runs:
            set_run_fonts_detail(run, "宋体", "Times New Roman", PT_XIAOSI, bold=False)


def format_reference_title(para):
    """参考文献/致谢标题：黑体小二号，居中"""
    format_chapter_title(para)


def format_reference_item(para):
    """参考文献条目：宋体小四号，固定行距"""
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = para.paragraph_format
    pf.space_before = None
    pf.space_after = None
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    for run in para.runs:
        set_run_fonts_detail(run, "宋体", "Times New Roman", PT_XIAOSI, bold=False)


def is_chapter_title(text):
    """判断是否为章标题：第X章"""
    return bool(re.match(r"^第\d+章", text.strip()))


def is_section1_title(text):
    """判断是否为一级节标题：X.X"""
    return bool(re.match(r"^\d+\.\d+\s+\S", text.strip())) and not re.match(
        r"^\d+\.\d+\.\d+", text.strip()
    )


def is_section2_title(text):
    """判断是否为二级节标题：X.X.X"""
    return bool(re.match(r"^\d+\.\d+\.\d+", text.strip()))


def is_reference_item(text):
    """判断是否为参考文献条目"""
    return bool(re.match(r"^\[\d+\]", text.strip()))


def set_page_margins(doc):
    """设置页面边距"""
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.left_margin = Cm(2.8)
        section.right_margin = Cm(2.7)
        section.top_margin = Cm(3.0)
        section.bottom_margin = Cm(2.6)


def main():
    doc = Document(INPUT_PATH)

    # 1. 设置页面边距
    print("=== 第1步：设置页面边距 ===")
    set_page_margins(doc)
    print("页面边距设置完成")

    # 2. 标记每个段落的角色并格式化
    print("\n=== 第2步：格式化各段落 ===")

    paragraphs = doc.paragraphs

    # 段落索引0是封面标题
    # 先分析每段的类型
    state = "cover"  # cover, abstract_cn, abstract_en, body, references, acknowledgment
    in_abstract_cn = False
    in_abstract_en = False
    in_references = False
    in_acknowledgment = False

    for i, para in enumerate(paragraphs):
        text = para.text.strip()

        print(f"[{i}] 处理: {text[:50]!r}")

        # ===== 封面标题 =====
        if i == 0:
            # 论文大标题：黑体二号居中
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf = para.paragraph_format
            pf.space_before = Pt(0)
            pf.space_after = Pt(0)
            pf.first_line_indent = None
            pf.left_indent = None
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pf.line_spacing = FIXED_LINE_SPACING
            for run in para.runs:
                set_run_fonts_detail(
                    run, "黑体", "Times New Roman", PT_XIAOER, bold=True
                )
            continue

        # ===== 空行 =====
        if not text:
            pf = para.paragraph_format
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pf.line_spacing = FIXED_LINE_SPACING
            continue

        # ===== 摘要标题 =====
        if text.startswith("摘") and ("要" in text):
            in_abstract_cn = True
            in_abstract_en = False
            format_abstract_title(para, is_cn=True)
            continue

        # ===== Abstract标题 =====
        if text == "Abstract":
            in_abstract_cn = False
            in_abstract_en = True
            format_abstract_title(para, is_cn=False)
            continue

        # ===== 关键词 =====
        if text.startswith("关键词"):
            format_keywords_para(para, is_cn=True)
            continue

        if text.startswith("Key Words"):
            format_keywords_para(para, is_cn=False)
            continue

        # ===== 参考文献标题 =====
        if text == "参考文献":
            in_references = True
            in_acknowledgment = False
            format_chapter_title(para)
            continue

        # ===== 致谢标题 =====
        if text.startswith("致"):
            in_references = False
            in_acknowledgment = True
            format_chapter_title(para)
            continue

        # ===== 章标题 =====
        if is_chapter_title(text):
            in_abstract_cn = False
            in_abstract_en = False
            in_references = False
            in_acknowledgment = False
            format_chapter_title(para)
            continue

        # ===== 节标题 X.X =====
        if is_section1_title(text):
            format_section1_title(para)
            continue

        # ===== 节标题 X.X.X =====
        if is_section2_title(text):
            format_section2_title(para)
            continue

        # ===== 参考文献条目 =====
        if in_references and is_reference_item(text):
            format_reference_item(para)
            continue

        # ===== 其他正文段落 =====
        format_body_para(para)

    # 保存
    print(f"\n=== 保存到: {OUTPUT_PATH} ===")
    doc.save(OUTPUT_PATH)
    print("保存完成！")


if __name__ == "__main__":
    main()
