"""
步骤2：
1. 在 Abstract 段落前插入分页符
2. 在所有 section 的页脚添加居中页码
3. 修复图序号引用错误：
   - 段227: "如图4-1所示" → "如图4-3所示"（用户登录时序图实际是图4-3）
   - 段168: "如图3-2" → "如图3-4"（ER图实际是图3-4）
"""

import re
import shutil
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH
from lxml import etree

INPUT = "毕业论文_吕智康_fixed2.docx"
OUTPUT = "毕业论文_吕智康_fixed3.docx"

doc = Document(INPUT)

# ============================================================
# 1. 在 Abstract 段落前插入分页符
# ============================================================
abstract_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "Abstract":
        abstract_idx = i
        break

if abstract_idx is not None:
    abstract_para = doc.paragraphs[abstract_idx]
    pPr = abstract_para._element.find(qn("w:pPr"))
    if pPr is None:
        pPr = etree.SubElement(abstract_para._element, qn("w:pPr"))
        abstract_para._element.insert(0, pPr)
    # 添加 pageBreakBefore
    pb = pPr.find(qn("w:pageBreakBefore"))
    if pb is None:
        pb = etree.SubElement(pPr, qn("w:pageBreakBefore"))
    pb.set(qn("w:val"), "1")
    print(f"已在 Abstract 段落(索引{abstract_idx})前添加分页符")
else:
    print("警告: 未找到 Abstract 段落")


# ============================================================
# 2. 添加页脚页码（所有 section）
# ============================================================
def add_page_number_to_footer(section):
    footer = section.footer
    # 清空现有页脚内容
    for p in footer.paragraphs:
        for child in list(p._element):
            p._element.remove(child)

    if footer.paragraphs:
        para = footer.paragraphs[0]
    else:
        para = footer.add_paragraph()

    # 设置居中
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 设置字体
    run = para.add_run()
    run.font.name = "Times New Roman"
    run.font.size = None  # 用默认

    # 添加页码字段: { PAGE }
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")

    instrText = OxmlElement("w:instrText")
    instrText.text = " PAGE "
    instrText.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")

    run._element.append(fldChar1)
    run._element.append(instrText)
    run._element.append(fldChar2)


for si, section in enumerate(doc.sections):
    add_page_number_to_footer(section)
    print(f"section[{si}] 页脚页码已添加")

# ============================================================
# 3. 修复图序号引用错误
# ============================================================
fixes = [
    # (段落索引, 原文本片段, 新文本片段)
    (227, "如图4-1所示", "如图4-3所示"),
    (168, "如图3-2所示", "如图3-4所示"),
]

for para_idx, old_frag, new_frag in fixes:
    p = doc.paragraphs[para_idx]
    full_text = p.text
    if old_frag in full_text:
        # 修改 run 中的文本
        for run in p.runs:
            if old_frag in run.text:
                run.text = run.text.replace(old_frag, new_frag)
                print(f"段落[{para_idx}] 修复: {old_frag!r} → {new_frag!r}")
                break
        else:
            # 如果跨 run，重建文本
            new_full = full_text.replace(old_frag, new_frag)
            # 清除所有 run，重写
            for run in p.runs:
                run.text = ""
            if p.runs:
                p.runs[0].text = new_full
                print(f"段落[{para_idx}] 跨run修复: {old_frag!r} → {new_frag!r}")
            else:
                print(f"段落[{para_idx}] 警告: 无法修复（无run）")
    else:
        print(f"段落[{para_idx}] 未找到 {old_frag!r}，当前文本: {full_text[:80]!r}")

doc.save(OUTPUT)
print(f"\n已保存: {OUTPUT}")
