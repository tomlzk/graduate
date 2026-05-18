from pathlib import Path
import re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

BASE_DIR = Path(r"e:\graduate\docx")
CONTENT_PATH = BASE_DIR / "thesis_v4_content.txt"
OUTPUT_PATH = BASE_DIR / "毕业论文_吕智康.docx"

PT_XIAOER = Pt(18)
PT_SAN = Pt(16)
PT_SI = Pt(14)
PT_XIAOSI = Pt(12)
FIXED_LINE_SPACING = Pt(20)
FIRST_LINE_INDENT = Pt(24)


def ensure_rpr(run):
    return run._element.get_or_add_rPr()


def set_run_fonts_detail(run, cn_font, en_font, size, bold=None):
    rpr = ensure_rpr(run)
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    rfonts.set(qn("w:ascii"), en_font)
    rfonts.set(qn("w:hAnsi"), en_font)
    rfonts.set(qn("w:eastAsia"), cn_font)
    rfonts.set(qn("w:cs"), en_font)
    run.font.size = size
    if bold is not None:
        run.font.bold = bold


def apply_font_to_paragraph(para, cn_font, en_font, size, bold=None):
    if not para.runs:
        para.add_run(para.text)
    for run in para.runs:
        set_run_fonts_detail(run, cn_font, en_font, size, bold=bold)


def set_page_margins(doc):
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.left_margin = Cm(2.8)
        section.right_margin = Cm(2.7)
        section.top_margin = Cm(3.0)
        section.bottom_margin = Cm(2.6)


def is_chapter_title(text):
    return bool(re.match(r"^第\d+章", text.strip()))


def is_section1_title(text):
    text = text.strip()
    return bool(re.match(r"^\d+\.\d+\s+\S", text)) and not bool(
        re.match(r"^\d+\.\d+\.\d+", text)
    )


def is_section2_title(text):
    return bool(re.match(r"^\d+\.\d+\.\d+\s*", text.strip()))


def is_reference_item(text):
    return bool(re.match(r"^\[\d+\]", text.strip()))


def format_cover_title(para):
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = para.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    apply_font_to_paragraph(para, "黑体", "Times New Roman", PT_XIAOER, bold=True)


def format_chapter_title(para):
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = para.paragraph_format
    pf.space_before = Pt(18)
    pf.space_after = Pt(6)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    apply_font_to_paragraph(para, "黑体", "Times New Roman", PT_XIAOER, bold=True)


def format_section1_title(para):
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = para.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(8)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    apply_font_to_paragraph(para, "黑体", "Times New Roman", PT_SAN, bold=False)


def format_section2_title(para):
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = para.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(8)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    apply_font_to_paragraph(para, "黑体", "Times New Roman", PT_SI, bold=False)


def format_body_para(para):
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = para.paragraph_format
    pf.space_before = None
    pf.space_after = None
    pf.first_line_indent = FIRST_LINE_INDENT
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    apply_font_to_paragraph(para, "宋体", "Times New Roman", PT_XIAOSI, bold=False)


def format_abstract_title(para):
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = para.paragraph_format
    pf.space_before = Pt(18)
    pf.space_after = Pt(18)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    apply_font_to_paragraph(para, "黑体", "Times New Roman", PT_XIAOER, bold=True)


def format_keywords_para(para):
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = para.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(0)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    apply_font_to_paragraph(para, "宋体", "Times New Roman", PT_XIAOSI, bold=False)


def format_reference_item(para):
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = para.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    apply_font_to_paragraph(para, "宋体", "Times New Roman", PT_XIAOSI, bold=False)


def is_figure_placeholder(text):
    return bool(re.match(r"^\[图\d+-\d+\]$", text.strip()))


def is_figure_caption(text):
    return bool(re.match(r"^图\d+-\d+\s+\S", text.strip()))


def format_figure_placeholder(para):
    for run in para.runs:
        run.text = ""
    if not para.runs:
        para.add_run()
    para.runs[0].text = "（请在此处插入图片截图）"
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = para.paragraph_format
    pf.space_before = Pt(6)
    pf.space_after = Pt(0)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    set_run_fonts_detail(para.runs[0], "宋体", "Times New Roman", PT_XIAOSI, bold=False)


def format_caption(para):
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = para.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(6)
    pf.first_line_indent = None
    pf.left_indent = None
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = FIXED_LINE_SPACING
    apply_font_to_paragraph(para, "宋体", "Times New Roman", PT_XIAOSI, bold=False)


def add_page_break(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run()
    br = OxmlElement("w:br")
    br.set(qn("w:type"), "page")
    run._element.append(br)


def format_paragraphs(doc):
    in_references = False
    cover_done = False
    for index, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        has_picture = any(
            elem.tag.endswith("}drawing") for elem in para._element.iter()
        )
        if has_picture:
            continue
        if not cover_done and text and not text.startswith("摘"):
            format_cover_title(para)
            cover_done = True
            continue
        if not text:
            pf = para.paragraph_format
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pf.line_spacing = FIXED_LINE_SPACING
            continue
        if text == "摘  要" or text == "摘 要" or text == "Abstract":
            in_references = False
            format_abstract_title(para)
            continue
        if text.startswith("关键词") or text.startswith("Key Words"):
            format_keywords_para(para)
            continue
        if text == "参考文献" or text == "致谢":
            in_references = text == "参考文献"
            format_chapter_title(para)
            continue
        if is_chapter_title(text):
            in_references = False
            format_chapter_title(para)
            continue
        if is_section2_title(text):
            format_section2_title(para)
            continue
        if is_section1_title(text):
            format_section1_title(para)
            continue
        if in_references and is_reference_item(text):
            format_reference_item(para)
            continue
        br_elems = para._element.findall(f".//{qn('w:br')}")
        if br_elems:
            continue
        if is_figure_placeholder(text):
            format_figure_placeholder(para)
            continue
        if is_figure_caption(text):
            format_caption(para)
            continue
        format_body_para(para)


def load_paragraphs():
    raw = CONTENT_PATH.read_text(encoding="utf-8")
    parts = [part.strip() for part in re.split(r"\n\s*\n", raw) if part.strip()]
    return parts


def count_chinese_characters(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def main():
    paragraphs = load_paragraphs()
    if not paragraphs:
        raise SystemExit("正文内容为空，无法生成论文。")

    content_text = "\n".join(paragraphs)
    cn_count = count_chinese_characters(content_text)
    print(f"中文字符数: {cn_count}")
    if cn_count < 25000:
        print(f"警告：中文字符数 {cn_count} 不足 25000，请检查内容。")

    doc = Document()
    set_page_margins(doc)

    prev_was_chapter = False
    for idx, text in enumerate(paragraphs):
        is_chap = is_chapter_title(text) or text in ("参考文献", "致谢")
        if is_chap and idx > 0 and not prev_was_chapter:
            add_page_break(doc)
        doc.add_paragraph(text)
        prev_was_chapter = is_chap

    format_paragraphs(doc)
    doc.save(str(OUTPUT_PATH))
    print(f"已生成: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
