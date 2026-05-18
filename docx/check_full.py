import re
from docx import Document
from docx.oxml.ns import qn

doc = Document("毕业论文_吕智康_final.docx")
paras = doc.paragraphs

print("=" * 60)
print("【5】页脚与分页检查")
print("=" * 60)
for si, sec in enumerate(doc.sections):
    footer = sec.footer
    texts = []
    for p in footer.paragraphs:
        instr = [el.text for el in p._element.findall(".//" + qn("w:instrText"))]
        has_page = any("PAGE" in (t or "") for t in instr)
        if has_page:
            texts.append("PAGE字段")
        if p.text.strip():
            texts.append(repr(p.text.strip()))
    empty = "空"
    desc = str(texts) if texts else empty
    print(f"  section[{si}] 页脚: {desc}")

for i, p in enumerate(paras):
    if p.text.strip() == "Abstract":
        pPr = p._element.find(qn("w:pPr"))
        pb = pPr.find(qn("w:pageBreakBefore")) if pPr is not None else None
        pbval = pb.get(qn("w:val")) if pb is not None else None
        print(f"  Abstract[{i}] pageBreakBefore: {pb is not None}, val={pbval!r}")
        break

print()
print("=" * 60)
print("【6】图片后是否紧接图题")
print("=" * 60)


def has_drawing(p):
    return bool(p._element.findall(".//" + qn("w:drawing")))


for i in range(len(paras) - 2):
    p = paras[i]
    if has_drawing(p):
        nxt = paras[i + 1]
        cap = re.match(r"^图\d+-\d+", nxt.text.strip())
        if not cap:
            nxt2 = paras[i + 2]
            cap2 = re.match(r"^图\d+-\d+", nxt2.text.strip())
            if not cap2:
                print(f"  警告：[{i:03d}] 图片后[{i+1}] 不是图题: {nxt.text[:50]!r}")

print("  图题检查完成")

print()
print("=" * 60)
print("【7】参考文献格式检查")
print("=" * 60)
in_ref = False
for i, p in enumerate(paras):
    t = p.text.strip()
    if t == "参考文献":
        in_ref = True
        continue
    if in_ref and t == "致谢":
        break
    if in_ref and t:
        m = re.match(r"^\[(\d+)\](.+)", t)
        if not m:
            print(f"  格式异常[{i}]: {t[:60]!r}")
            continue
        num = int(m.group(1))
        content = m.group(2)
        if not re.search(r"\[J\]|\[D\]|\[C\]|\[M\]|\[N\]|\[R\]|arXiv", content):
            print(f"  缺类型标识[{i}]: [{num}]{content[:60]!r}")
        if not re.search(r"\d{4}", content):
            print(f"  缺年份[{i}]: [{num}]{content[:60]!r}")
print("  参考文献格式检查完成")

print()
print("=" * 60)
print("【8】正文引用上标位置合理性（标题上有上标？）")
print("=" * 60)
heading_pattern = re.compile(r"^第[1-6]章|^\d+\.\d+|^摘|^Abstract|^参考|^致谢")
for i, p in enumerate(paras):
    sups = [
        r.text for r in p.runs if r.font.superscript and re.search(r"\[\d+\]", r.text)
    ]
    if sups and heading_pattern.match(p.text.strip()):
        print(f"  警告[{i}] 标题含上标: {p.text.strip()[:60]!r}")
print("  上标位置检查完成")

print()
print("=" * 60)
print("【9】图4-6 与 图4-11 重复问题（首页截图）")
print("=" * 60)
for i, p in enumerate(paras):
    t = p.text.strip()
    if "图4-6" in t or "图4-11" in t:
        print(f"  [{i}] {t[:80]!r}")
