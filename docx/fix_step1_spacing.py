"""
步骤1：修复全文行间距
策略：
- 正文段落（非图片、非标题）：统一改为固定行距 400 twips（20磅），与标题一致
- 含图片的段落：改为 auto 单倍行距（lineRule=auto, line=240），让图片完整显示
- 图说明段落（图X-X）：保持 auto 行距，间距 before=40 after=120
- 空行段落（图片占位空行）：auto 行距
"""

import re
import shutil
from docx import Document
from docx.oxml.ns import qn
from lxml import etree

INPUT = "毕业论文_吕智康_fixed.docx"
OUTPUT = "毕业论文_吕智康_fixed2.docx"
shutil.copy2(INPUT, INPUT + ".step0bak")

doc = Document(INPUT)


def set_spacing(pPr, line, lineRule, before=None, after=None):
    """设置段落间距"""
    sp = pPr.find(qn("w:spacing"))
    if sp is None:
        sp = etree.SubElement(pPr, qn("w:spacing"))
        # 插到 pPr 合适位置
        pPr.remove(sp)
        # 找合适位置插入（在 outlineLvl 之前）
        ol = pPr.find(qn("w:outlineLvl"))
        if ol is not None:
            ol.addprevious(sp)
        else:
            pPr.append(sp)

    sp.set(qn("w:line"), str(line))
    sp.set(qn("w:lineRule"), lineRule)

    # 清除 before/after（只在明确指定时设置）
    for attr in [qn("w:before"), qn("w:after")]:
        if attr in sp.attrib:
            del sp.attrib[attr]

    if before is not None:
        sp.set(qn("w:before"), str(before))
    if after is not None:
        sp.set(qn("w:after"), str(after))


def ensure_pPr(p):
    pPr = p._element.find(qn("w:pPr"))
    if pPr is None:
        pPr = etree.Element(qn("w:pPr"))
        p._element.insert(0, pPr)
    return pPr


changed = 0
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    has_img = p._element.find(".//" + qn("w:drawing")) is not None

    # 跳过封面页（前30段左右）
    if i < 30:
        continue

    pPr = p._element.find(qn("w:pPr"))
    if pPr is None:
        continue

    sp = pPr.find(qn("w:spacing"))
    cur_line = sp.get(qn("w:line")) if sp is not None else None
    cur_rule = sp.get(qn("w:lineRule")) if sp is not None else None

    # 图说明段落（以"图"开头的短标题）
    if re.match(r"^图\d+-\d+", t):
        pPr = ensure_pPr(p)
        set_spacing(pPr, line=240, lineRule="auto", before=40, after=120)
        changed += 1
        continue

    # 含图片的段落：auto 行距，让图片完整显示
    if has_img:
        pPr = ensure_pPr(p)
        set_spacing(pPr, line=240, lineRule="auto", before=120, after=0)
        changed += 1
        continue

    # 空行（图片前后的空段）
    if not t and sp is not None:
        # 如果是 exact，改成 auto
        if cur_rule == "exact":
            set_spacing(pPr, line=240, lineRule="auto")
            changed += 1
        continue

    # 标题段落：不修改（已经是 exact 400）
    ol = pPr.find(qn("w:outlineLvl"))
    if ol is not None:
        continue

    # 正文段落：如果不是 exact 400，统一改为 exact 400
    if cur_rule != "exact" or cur_line != "400":
        set_spacing(pPr, line=400, lineRule="exact")
        changed += 1

print(f"行间距修复完成，共修改 {changed} 个段落")
doc.save(OUTPUT)
print(f"已保存: {OUTPUT}")
