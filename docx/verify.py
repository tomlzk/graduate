from docx import Document
from docx.oxml.ns import qn
import re

doc = Document("毕业论文_吕智康_fixed4.docx")

# 验证1：Abstract 前是否有分页符
W_VAL = qn("w:val")
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "Abstract":
        pPr = p._element.find(qn("w:pPr"))
        pb = pPr.find(qn("w:pageBreakBefore")) if pPr is not None else None
        has_pb = pb is not None and pb.get(W_VAL) == "1"
        print(f"Abstract段落[{i}] pageBreakBefore: {has_pb}")
        break

# 验证2：页脚PAGE字段
for si, sec in enumerate(doc.sections):
    footer = sec.footer
    has_page_field = any(
        "PAGE" in (el.text or "")
        for p in footer.paragraphs
        for el in p._element.findall(".//" + qn("w:instrText"))
    )
    print(f"section[{si}] 页脚有PAGE字段: {has_page_field}")

# 验证3：图序号错误
print()
for i, p in enumerate(doc.paragraphs):
    t = p.text
    if "图4-1所示" in t and "图4-1  " not in t:
        print(f"警告段落[{i}]: {t[:80]!r}")
    if "图3-2所示" in t and "图3-2  " not in t:
        print(f"警告段落[{i}]: {t[:80]!r}")
print("图序号检查完成")

# 验证4：正文上标
print()
print("=== 上标引用（前10处）===")
count = 0
for i, p in enumerate(doc.paragraphs):
    for run in p.runs:
        if run.font.superscript and re.match(r"^\[\d+\]", run.text):
            print(f"  段落[{i}]: 上标 {run.text!r}")
            count += 1
    if count >= 10:
        break

# 验证5：参考文献
print()
print("=== 参考文献 ===")
in_ref = False
ref_count = 0
for p in doc.paragraphs:
    t = p.text.strip()
    if t == "参考文献":
        in_ref = True
        continue
    if in_ref and t == "致谢":
        break
    if in_ref and t:
        print(f"  {t[:90]}")
        ref_count += 1
print(f"共 {ref_count} 条参考文献")
