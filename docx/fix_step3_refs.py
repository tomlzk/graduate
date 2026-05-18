"""
步骤3：
1. 重写参考文献列表（17篇，含4篇英文，1篇2025年下半年）
2. 在第1章正文各段末尾/关键处插入上标引用
3. 后续章节适当添加1-2处引用上标
4. 删除图3-1双标题（段落143：含文字的那个"和传统的服务端渲染..."之后的重复空行/段）
   实际检查：图3-1下面只有一个说明"图3-1 系统总体架构图"，HTML内嵌标题需手动处理
"""

import re
import copy
import shutil
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree

INPUT = "毕业论文_吕智康_fixed3.docx"
OUTPUT = "毕业论文_吕智康_fixed4.docx"

doc = Document(INPUT)

# ============================================================
# 新参考文献列表（按引用次序排列）
# [1]-[7]: 第1章引用（国内外现状、技术背景）
# [8]-[13]: 第3/4章引用（系统设计、技术实现）
# [14]-[17]: 英文文献
# ============================================================
NEW_REFS = [
    # 第1章 - 国内外现状、高校信息系统、考试/教育平台
    "[1]操心慧,温智聪. 基于JavaWeb的线上考试系统的设计与实现[J].现代计算机,2023,29(24):90-96.",
    "[2]廖常武. 基于Web的高校成绩管理系统的设计与实现[J].科技风,2023,(27):4-6.DOI:10.19392/j.cnki.1671-7341.202327002.",
    "[3]周全. 高校学籍管理信息化平台的设计与实现[J].办公自动化,2023,28(09):61-64.",
    "[4]蒋金涛. 基于Web的高校在线考试系统设计[J].无线互联科技,2022,19(19):88-90.",
    "[5]刘庆海,徐雪梅. 基于Web的考试系统设计与实现[J].电脑编程技巧与维护,2021,(12):17-20.DOI:10.16184/j.cnki.comprg.2021.12.007.",
    "[6]范峰岩. 基于Web技术的计算机应用考试系统分析[J].电脑知识与技术,2021,17(28):122-124.DOI:10.14004/j.cnki.ckt.2021.3018.",
    "[7]付冬芹. 在线考试系统的设计与实现[D].北京交通大学,2023.DOI:10.26944/d.cnki.gbfju.2023.000427.",
    # 第1章 - 技术趋势（前后端分离、RESTful）
    "[8]黄芳,王纪鑫.基于Web的网络考试系统设计与实现[C]//中国计算机学会.2022中国高校计算机教育大会论文集.南宁学院高博软件学院,2022:72-77.DOI:10.26914/c.cnkihy.2022.092703.",
    "[9]王莉莉. 基于Web的学生信息管理系统设计与实现[J].信息记录材料,2022,23(07):154-158.DOI:10.16009/j.cnki.cn13-1295/tq.2022.07.024.",
    # 第3/4章 - Spring Boot、MyBatis-Plus、Vue3、JWT
    "[10]李旭东. 基于Web的高校电子商务系统设计[J].自动化技术与应用,2022,41(06):152-153+156.DOI:10.20033/j.1003-7241.(2022)06-0152-03.",
    "[11]陈灏,黄超. 基于WebAPP框架的电子学生证平台设计[J].信息记录材料,2022,23(05):186-188.DOI:10.16009/j.cnki.cn13-1295/tq.2022.05.014.",
    "[12]陈大胜. 基于WEB的单招考试确认系统的设计与实现[J].数据,2021,(10):90-92.",
    "[13]张慧. 基于Web的学生成绩管理系统设计[J].信息与电脑,2025,37(23):112-114.",
    # 英文文献
    "[14]Falebita O S. Secure web-based student information management system[J]. arXiv preprint arXiv:2211.00072, 2022.",
    "[15]Pradana W L, Wibowo A. Implementation of Agile and Waterfall Methods in a Web-Based Admission System for Streamlined Registration and Communication[J]. INOVTEK Polbeng-Seri Informatika, 2025, 10(1): 504-513.",
    "[16]Subramanian R R, Surekha B, SubbaRao P, et al. EduGuard–AI Based Online Exam Management System[C]//2025 International Conference on Computational Robotics, Testing and Engineering Evaluation (ICCRTEE). IEEE, 2025: 1-6.",
    "[17]Kaewsuwan S, Khwunnak C. The development of web-based application of registration system[J]. Engineering Access, 2022, 8(1): 101-105.",
]

# ============================================================
# 各段落引用规划（段落索引 → 上标列表）
# 第1章大量引用，后续章节少量
# ============================================================
CITATION_PLAN = {
    # 1.1 研究背景
    70: [1, 2],  # "备考已经成为很多同学..."
    71: [3, 4],  # "就校园内的实际情况来看..."
    72: [5],  # "时效性问题..."
    # 1.2 研究目的
    75: [6],  # "本文想做的事情..."
    76: [7],  # "前后端分离架构..."
    # 1.3 国内外现状
    81: [8, 9],  # "国内目前面向备考的互联网产品..."
    82: [14, 17],  # "国外的在线学习社区..."
    83: [10, 11],  # "从技术趋势来看，前后端分离..."
    84: [12, 13],  # "从工程实践来看..."
    # 第3章
    152: [10],  # "前端选用Vue3..."
    153: [11],  # "后端基于Spring Boot..."
    # 第4章
    209: [6],  # "异常处理方面..."
    230: [5],  # "用户模块主要包含..."
    # 第5章
    322: [15, 16],  # "测试环境..."
}


# ============================================================
# 工具函数：给段落末尾添加上标引用
# ============================================================
def add_superscript_citations(para, numbers):
    """在段落末尾最后一个 run 后追加上标引用 [n]"""
    for num in numbers:
        run = para.add_run(f"[{num}]")
        run.font.superscript = True
        # 字号小一号
        run.font.size = None  # 继承


# ============================================================
# 添加上标引用
# ============================================================
added_cites = 0
for para_idx, cite_nums in sorted(CITATION_PLAN.items()):
    if para_idx >= len(doc.paragraphs):
        print(f"警告: 段落索引 {para_idx} 超出范围")
        continue
    p = doc.paragraphs[para_idx]
    t = p.text.strip()
    if not t:
        print(f"警告: 段落[{para_idx}] 为空")
        continue
    add_superscript_citations(p, cite_nums)
    added_cites += 1
    print(f"段落[{para_idx}] 添加引用上标 {cite_nums}: {t[:40]!r}...")

print(f"\n共添加 {added_cites} 处引用上标")

# ============================================================
# 替换参考文献部分
# ============================================================
# 找到"参考文献"段落
ref_start_idx = None
ref_end_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "参考文献":
        ref_start_idx = i
    if ref_start_idx and i > ref_start_idx and p.text.strip() == "致谢":
        ref_end_idx = i
        break

print(f"\n参考文献范围: [{ref_start_idx}] 到 [{ref_end_idx}]")

if ref_start_idx and ref_end_idx:
    # 参考文献正文段落是 ref_start_idx+1 到 ref_end_idx-1
    old_ref_paras = doc.paragraphs[ref_start_idx + 1 : ref_end_idx]
    print(f"现有参考文献条目数: {len(old_ref_paras)}")

    # 获取第一个参考文献段落的样式和格式信息（作为模板）
    template_para = old_ref_paras[0] if old_ref_paras else None

    # 删除现有参考文献段落（从后往前删除）
    body = doc.element.body
    paras_to_delete = []
    for p in old_ref_paras:
        if p.text.strip():  # 只删除有内容的
            paras_to_delete.append(p._element)

    for pel in paras_to_delete:
        body.remove(pel)

    # 找到"致谢"段落（重新查找，因为已删除段落）
    zhixie_para = None
    for p in doc.paragraphs:
        if p.text.strip() == "致谢":
            zhixie_para = p
            break

    if zhixie_para is None:
        print("错误: 未找到致谢段落")
    else:
        # 在"致谢"段落前插入新参考文献
        def get_ref_para_xml(template_para):
            """获取参考文献段落的 pPr XML"""
            if template_para:
                pPr = template_para._element.find(qn("w:pPr"))
                if pPr is not None:
                    return copy.deepcopy(pPr)
            return None

        template_pPr = get_ref_para_xml(template_para)

        # 从后往前在 zhixie_para 前插入（保持顺序）
        for ref_text in reversed(NEW_REFS):
            new_para = OxmlElement("w:p")

            # 添加 pPr
            if template_pPr is not None:
                new_para.append(copy.deepcopy(template_pPr))

            # 添加 run
            new_run = OxmlElement("w:r")

            # 如果 template_para 有 rPr，复制它
            if template_para and template_para.runs:
                rPr = template_para.runs[0]._element.find(qn("w:rPr"))
                if rPr is not None:
                    new_run.append(copy.deepcopy(rPr))

            new_t = OxmlElement("w:t")
            new_t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            new_t.text = ref_text
            new_run.append(new_t)
            new_para.append(new_run)

            zhixie_para._element.addprevious(new_para)

        print(f"已插入 {len(NEW_REFS)} 条新参考文献")

doc.save(OUTPUT)
print(f"\n已保存: {OUTPUT}")
