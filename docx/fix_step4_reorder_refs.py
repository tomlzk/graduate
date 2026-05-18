import re
from docx import Document
from docx.oxml import OxmlElement

INPUT = "毕业论文_吕智康_fixed4.docx"
OUTPUT = "毕业论文_吕智康_final.docx"

doc = Document(INPUT)

NEW_REFS_ORDERED = [
    "[1]操心慧,温智聪. 基于JavaWeb的线上考试系统的设计与实现[J].现代计算机,2023,29(24):90-96.",
    "[2]廖常武. 基于Web的高校成绩管理系统的设计与实现[J].科技风,2023,(27):4-6.DOI:10.19392/j.cnki.1671-7341.202327002.",
    "[3]周全. 高校学籍管理信息化平台的设计与实现[J].办公自动化,2023,28(09):61-64.",
    "[4]蒋金涛. 基于Web的高校在线考试系统设计[J].无线互联科技,2022,19(19):88-90.",
    "[5]刘庆海,徐雪梅. 基于Web的考试系统设计与实现[J].电脑编程技巧与维护,2021,(12):17-20.DOI:10.16184/j.cnki.comprg.2021.12.007.",
    "[6]范峰岩. 基于Web技术的计算机应用考试系统分析[J].电脑知识与技术,2021,17(28):122-124.DOI:10.14004/j.cnki.ckt.2021.3018.",
    "[7]付冬芹. 在线考试系统的设计与实现[D].北京交通大学,2023.DOI:10.26944/d.cnki.gbfju.2023.000427.",
    "[8]黄芳,王纪鑫.基于Web的网络考试系统设计与实现[C]//中国计算机学会.2022中国高校计算机教育大会论文集.南宁学院高博软件学院,2022:72-77.DOI:10.26914/c.cnkihy.2022.092703.",
    "[9]王莉莉. 基于Web的学生信息管理系统设计与实现[J].信息记录材料,2022,23(07):154-158.DOI:10.16009/j.cnki.cn13-1295/tq.2022.07.024.",
    "[10]李旭东. 基于Web的高校电子商务系统设计[J].自动化技术与应用,2022,41(06):152-153+156.DOI:10.20033/j.1003-7241.(2022)06-0152-03.",
    "[11]陈灏,黄超. 基于WebAPP框架的电子学生证平台设计[J].信息记录材料,2022,23(05):186-188.DOI:10.16009/j.cnki.cn13-1295/tq.2022.05.014.",
    "[12]陈大胜. 基于WEB的单招考试确认系统的设计与实现[J].数据,2021,(10):90-92.",
    "[13]张慧. 基于Web的学生成绩管理系统设计[J].信息与电脑,2025,37(23):112-114.",
    "[14]Falebita O S. Secure web-based student information management system[J]. arXiv preprint arXiv:2211.00072, 2022.",
    "[15]Pradana W L, Wibowo A. Implementation of Agile and Waterfall Methods in a Web-Based Admission System for Streamlined Registration and Communication[J]. INOVTEK Polbeng-Seri Informatika, 2025, 10(1): 504-513.",
    "[16]Subramanian R R, Surekha B, SubbaRao P, et al. EduGuard-AI Based Online Exam Management System[C]//2025 International Conference on Computational Robotics, Testing and Engineering Evaluation (ICCRTEE). IEEE, 2025: 1-6.",
    "[17]Kaewsuwan S, Khwunnak C. The development of web-based application of registration system[J]. Engineering Access, 2022, 8(1): 101-105.",
]

in_ref = False
ref_paras = []
for p in doc.paragraphs:
    t = p.text.strip()
    if t == "参考文献":
        in_ref = True
        continue
    if in_ref and t == "致谢":
        break
    if in_ref and t and re.match(r"^\[\d+\]", t):
        ref_paras.append(p)

print(f"找到 {len(ref_paras)} 个参考文献段落")

for i, (p, new_text) in enumerate(zip(ref_paras, NEW_REFS_ORDERED)):
    old_text = p.text.strip()
    if p.runs:
        p.runs[0].text = new_text
        for run in p.runs[1:]:
            run.text = ""
    else:
        r = OxmlElement("w:r")
        t_el = OxmlElement("w:t")
        t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        t_el.text = new_text
        r.append(t_el)
        p._element.append(r)
    print(f"  [{i+1}] {old_text[:30]!r} -> {new_text[:30]!r}")

print()
print("=== 验证 ===")
in_ref = False
cnt = 0
for p in doc.paragraphs:
    t = p.text.strip()
    if t == "参考文献":
        in_ref = True
        continue
    if in_ref and t == "致谢":
        break
    if in_ref and t:
        print(f"  {t[:70]}")
        cnt += 1
print(f"共 {cnt} 条")

doc.save(OUTPUT)
print(f"已保存: {OUTPUT}")
