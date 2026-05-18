"""
修复毕业论文_吕智康.docx 目录问题
原理：给所有标题段落添加 outlineLvl 大纲级别，使 WPS 的 TOC 字段能正常更新
- 只修改标题段落的 pPr（段落属性），不改字体/字号/颜色/封面等任何内容
"""

import re
import copy
import shutil
from docx import Document
from docx.oxml.ns import qn
from lxml import etree

INPUT = "毕业论文_吕智康.docx"
OUTPUT = "毕业论文_吕智康_fixed.docx"

# 先备份一份（以防万一）
shutil.copy2(INPUT, INPUT + ".bak2")
print(f"已备份: {INPUT}.bak2")

doc = Document(INPUT)
body = doc.element.body


def get_heading_level(text: str):
    """
    返回标题级别 0/1/2，或 None（不是标题）
    - 第X章 / 参考文献 / 致谢 → 0
    - X.X  → 1
    - X.X.X → 2
    """
    t = text.strip()
    if re.match(r"^第\d+章\s", t) or t in ("参考文献", "致谢"):
        return 0
    if re.match(r"^\d+\.\d+\.\d+", t):
        return 2
    if re.match(r"^\d+\.\d+\s", t) or re.match(r"^\d+\.\d+$", t):
        return 1
    return None


fixed = 0
for p in doc.paragraphs:
    level = get_heading_level(p.text)
    if level is None:
        continue

    pPr = p._element.find(qn("w:pPr"))
    if pPr is None:
        # 不存在 pPr，创建一个并插入到段落元素最前
        pPr = etree.SubElement(p._element, qn("w:pPr"))
        p._element.insert(0, pPr)

    # 检查是否已有 outlineLvl
    existing = pPr.find(qn("w:outlineLvl"))
    if existing is not None:
        current_val = int(existing.get(qn("w:val"), "9"))
        if current_val == level:
            continue  # 已经正确，跳过
        existing.set(qn("w:val"), str(level))
    else:
        # 插入 outlineLvl，按 OOXML 规范它应该放在 pPr 最后
        ol = etree.SubElement(pPr, qn("w:outlineLvl"))
        ol.set(qn("w:val"), str(level))

    fixed += 1
    print(f"  Level {level}: {p.text.strip()[:50]}")

print(f"\n共修改 {fixed} 个标题段落的大纲级别")
doc.save(OUTPUT)
print(f"已保存: {OUTPUT}")
print()
print("接下来操作：")
print("1. 用 WPS 打开 毕业论文_吕智康_fixed.docx")
print('2. 右键点击目录 → 更新域 → 选"更新整个目录"')
print("3. 确认目录正常后，另存覆盖原文件（或直接改名）")
