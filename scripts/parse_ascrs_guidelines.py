#!/usr/bin/env python3
"""
批量解析ASCRS临床实践指南PDF，提取知识三元组
来源：~/Desktop/CRC通用知识库/*.pdf
"""

import pdfplumber
import json
import re
import os
from datetime import datetime

GUIDE_DIR = "/Users/wangxiaodong/Desktop/CRC通用知识库"
OUTPUT_DIR = "/Users/wangxiaodong/colorectal-cancer-kb/data/knowledge-graph"
MAIN_KB = f"{OUTPUT_DIR}/relations.json"
OUT_EXTENDED = f"{OUTPUT_DIR}/relations_ascrs.json"

# PDF文件映射（排除疑似重复）
PDF_MAP = {
    "repview (1)": {
        "title": "ASCRS阑尾肿瘤管理指南",
        "source": "ASCRS Clinical Practice Guidelines - Appendiceal Neoplasms 2023",
        "evidence": "I级专家共识",
        "pages": None
    },
    "repview (2)": {
        "title": "ASCRS遗传性腺瘤性息肉病管理指南",
        "source": "ASCRS Clinical Practice Guidelines - Inherited Adenomatous Polyposis Syndromes 2022",
        "evidence": "I级专家共识",
        "pages": None
    },
    "repview (3)": {
        "title": "ASCRS遗传性腺瘤性息肉病管理指南",
        "source": "ASCRS Clinical Practice Guidelines - Inherited Adenomatous Polyposis Syndromes 2022",
        "evidence": "I级专家共识",
        "pages": None
    },
    "repview (4)": {
        "title": "ASCRS直肠癌管理指南2020",
        "source": "ASCRS Clinical Practice Guidelines - Management of Rectal Cancer 2020",
        "evidence": "I级专家共识",
        "pages": None
    },
    "repview (5)": {
        "title": "ASCRS直肠癌管理指南2020-补充",
        "source": "ASCRS Clinical Practice Guidelines - Management of Rectal Cancer 2020 (补充版)",
        "evidence": "I级专家共识",
        "pages": None
    },
    "repview (6)": {
        "title": "ASCRS直肠癌2023补充指南",
        "source": "ASCRS Clinical Practice Guidelines - Rectal Cancer 2023 Supplement",
        "evidence": "I级专家共识",
        "pages": None
    },
    "repview (7)": {
        "title": "ASCRS造口手术指南",
        "source": "ASCRS Clinical Practice Guidelines - Ostomy Surgery 2021",
        "evidence": "I级专家共识",
        "pages": None
    },
    "repview (8)": {
        "title": "ASCRS老年衰弱围手术期评估指南",
        "source": "ASCRS Clinical Practice Guidelines - Perioperative Evaluation and Management of Frailty 2022",
        "evidence": "I级专家共识",
        "pages": None
    },
    "repview (9)": {
        "title": "ASCRS Lynch综合征外科治疗指南",
        "source": "ASCRS Clinical Practice Guidelines - Surgical Treatment of Lynch Syndrome 2021",
        "evidence": "I级专家共识",
        "pages": None
    },
    "repview (10)": {
        "title": "ASCRS监测与生存照护指南",
        "source": "ASCRS Clinical Practice Guidelines - Surveillance and Survivorship Care 2021",
        "evidence": "I级专家共识",
        "pages": None
    },
    "repview (11)": {
        "title": "ASCRS肠道准备指南",
        "source": "ASCRS Clinical Practice Guidelines - Use of Bowel Preparation in Elective Colon and Rectal Surgery 2019",
        "evidence": "I级专家共识",
        "pages": None
    },
    "repview": {
        "title": "ASCRS肛管鳞状细胞癌指南",
        "source": "ASCRS Clinical Practice Guidelines - Anal Squamous Cell Cancers 2018 (Revised)",
        "evidence": "I级专家共识",
        "pages": None
    }
}

# 去重：repview(3)和repview(2)都是息肉病，取一个
# repview(4)和repview(5)都是直肠癌2020，内容可能有差异，都保留
FILES_TO_PROCESS = [
    "repview (1).pdf",
    "repview (2).pdf",
    # "repview (3).pdf",  # 重复
    "repview (4).pdf",
    "repview (5).pdf",  # 保留，因为页数相同但可能内容有补充
    "repview (6).pdf",
    "repview (7).pdf",
    "repview (8).pdf",
    "repview (9).pdf",
    "repview (10).pdf",
    "repview (11).pdf",
    "repview.pdf",
]

# 从文件名提取key
def file_to_key(filename):
    return filename.replace(".pdf", "").strip()

# 高级三元组提取：基于ASCRS指南特征提取
def extract_triplets(text, source_info):
    """从ASCRS指南文本中提取知识三元组"""
    triplets = []
    lines = text.split("\n")

    # 证据等级映射
    evidence_map = {
        "强推荐": "I级证据",
        "弱推荐": "II级证据",
        "强烈推荐": "I级证据",
        "推荐": "II级证据",
        "建议": "专家共识",
        "共识": "专家共识",
        "Grade 1": "I级证据",
        "Grade 2": "II级证据",
        "Level 1": "I级证据",
        "Level 2": "II级证据",
        "Strong": "I级证据",
        "Moderate": "II级证据",
    }

    for line in lines:
        line = line.strip()
        if not line or len(line) < 8:
            continue

        # 跳过参考文献行
        if re.match(r"^\[\d+\]", line) or re.match(r"^\(\d+\)", line):
            continue
        if re.match(r"^\d+\.", line) and "reference" in line.lower():
            continue

        # 处理"XX适用于YY"模式的推荐语句
        # 例如："Preoperative chemotherapy is recommended for patients with T3-4 or N+ rectal cancer"
        # 检测治疗相关推荐
        treatment_patterns = [
            # 推荐做某事（治疗/手术/检查）
            (r"(.+?)(\b推荐\b|\brecommended\b|\bshould\b|\bconsider\b)(.+)",
             r"对于\1\3，\2"),
            # XX用于YY（适应证）
            (r"(.+?)(\b用于\b|\bfor\b patients with|\bindicated\b)(.+)",
             r"\1常用于\3"),
        ]

        # 提取关键临床事实
        clinical_facts = []

        # 模式1: T/N分期相关
        t_pattern = r"(T[0-4][a-d]?)"
        if re.search(t_pattern, line):
            match = re.search(t_pattern, line)
            t_stage = match.group(1)
            if "推荐" in line or "建议" in line or "consider" in line.lower() or "recommend" in line.lower():
                triplets.append({
                    "head": f"直肠癌{t_stage}期",
                    "relation": "临床处理原则",
                    "tail": line[:80].strip(),
                    "source": source_info["source"],
                    "evidence": "I级专家共识",
                    "domain": get_domain(line)
                })

        # 模式2: 基因/分子标志物
        biomarker_patterns = [
            r"MMR", r"dMMR", r"MSI", r"MSS", r"KRAS", r"NRAS", r"BRAF",
            r"HER2", r"PD-1", r"PD-L1", r"CEA", r"CA19-9", r"AFP"
        ]
        for bp in biomarker_patterns:
            if bp in line and len(line) > 15:
                if "治疗" in line or "化疗" in line or "免疫" in line or "靶向" in line:
                    triplets.append({
                        "head": bp,
                        "relation": "临床应用",
                        "tail": line[:80].strip(),
                        "source": source_info["source"],
                        "evidence": "I级专家共识",
                        "domain": "基因靶点"
                    })

        # 模式3: 药物/治疗方案
        drug_patterns = [
            r"(5-FU|卡培他滨|奥沙利铂|伊立替康|贝伐单抗|西妥昔单抗|帕尼单抗|氟尿嘧啶)",
            r"(FOLFIRI|FOLFOX|CAPOX|XELOX|FOLFOXIRI|mFOLFOX6)",
            r"(PD-1抑制剂|PD-L1抑制剂|纳武利尤单抗|帕博利珠单抗|度伐利尤单抗)",
            r"(新辅助|辅助|同步放化疗|转化治疗|维持治疗)"
        ]
        for dp in drug_patterns:
            if re.search(dp, line, re.IGNORECASE):
                triplets.append({
                    "head": "结直肠癌治疗",
                    "relation": "治疗方案",
                    "tail": line[:80].strip(),
                    "source": source_info["source"],
                    "evidence": "I级专家共识",
                    "domain": "系统治疗"
                })

        # 模式4: 手术相关
        surgery_keywords = ["手术", "切除", "切除术", "吻合", "造口", "保肛", "括约肌", "TME", "全直肠系膜"]
        if any(kw in line for kw in surgery_keywords):
            triplets.append({
                "head": "结直肠癌外科",
                "relation": "手术原则",
                "tail": line[:80].strip(),
                "source": source_info["source"],
                "evidence": "I级专家共识",
                "domain": "外科手术"
            })

        # 模式5: 监测/随访相关
        surveillance_keywords = ["监测", "随访", "surveillance", "survivorship", "CEA监测", "肠镜", "CT"]
        if any(kw in line.lower() for kw in ["监测", "随访", "surveillance", "survivorship"]):
            triplets.append({
                "head": "结直肠癌随访监测",
                "relation": "监测方案",
                "tail": line[:80].strip(),
                "source": source_info["source"],
                "evidence": "I级专家共识",
                "domain": "造口·随访·筛查"
            })

        # 模式6: 衰弱评估
        frailty_keywords = ["衰弱", "frailty", "老年", "围手术期", "合并症", "营养"]
        if any(kw in line.lower() for kw in ["衰弱", "frailty", "老年", "围手术期", "营养"]):
            triplets.append({
                "head": "老年衰弱评估",
                "relation": "围手术期管理",
                "tail": line[:80].strip(),
                "source": source_info["source"],
                "evidence": "I级专家共识",
                "domain": "围手术期管理"
            })

        # 模式7: Lynch/遗传综合征
        hereditary_keywords = ["Lynch", "FAP", "腺瘤性息肉", "遗传性", "胚系突变", "基因检测"]
        if any(kw in line for kw in hereditary_keywords):
            triplets.append({
                "head": "遗传性结直肠癌",
                "relation": "筛查与治疗",
                "tail": line[:80].strip(),
                "source": source_info["source"],
                "evidence": "I级专家共识",
                "domain": "基因靶点"
            })

        # 模式8: 阑尾肿瘤
        appendiceal_keywords = ["阑尾肿瘤", "粘液性", "低级别", "高级别", "腹膜假粘液瘤", "HIPEC", "CRS"]
        if any(kw in line for kw in appendiceal_keywords):
            triplets.append({
                "head": "阑尾肿瘤",
                "relation": "诊疗原则",
                "tail": line[:80].strip(),
                "source": source_info["source"],
                "evidence": "I级专家共识",
                "domain": "阑尾肿瘤"
            })

        # 模式9: 肛管癌
        anal_keywords = ["肛管", "肛缘", "鳞状细胞癌", "同步放化疗", "mitomycin", "丝裂霉素", "5-FU"]
        if any(kw in line.lower() for kw in ["肛管", "anal", "鳞状", "squamous"]):
            triplets.append({
                "head": "肛管鳞状细胞癌",
                "relation": "诊疗方案",
                "tail": line[:80].strip(),
                "source": source_info["source"],
                "evidence": "I级专家共识",
                "domain": "肛管癌"
            })

        # 模式10: 造口相关
        ostomy_keywords = ["造口", "回肠造口", "结肠造口", "造口还纳", "ostomy", "ileostomy", "colostomy"]
        if any(kw in line.lower() for kw in ["造口", "ostomy", "ileostomy", "colostomy"]):
            triplets.append({
                "head": "造口管理",
                "relation": "临床要点",
                "tail": line[:80].strip(),
                "source": source_info["source"],
                "evidence": "I级专家共识",
                "domain": "造口·随访·筛查"
            })

    return triplets

def get_domain(line):
    """根据内容判断知识域"""
    if any(kw in line for kw in ["化疗", "靶向", "免疫", "治疗", "药物"]):
        return "系统治疗"
    if any(kw in line for kw in ["手术", "切除", "吻合", "TME"]):
        return "外科手术"
    if any(kw in line for kw in ["分期", "T分期", "N分期", "AJCC"]):
        return "分期系统"
    if any(kw in line for kw in ["LARS", "低位前切除", "吻合口", "腹泻", "失禁"]):
        return "LARS与并发症"
    if any(kw in line for kw in ["基因", "KRAS", "MSI", "MMR", "BRAF", "分子"]):
        return "基因靶点"
    if any(kw in line for kw in ["病理", "营养", "预后", "生存"]):
        return "病理·营养·预后"
    if any(kw in line for kw in ["筛查", "随访", "造口", "监测"]):
        return "造口·随访·筛查"
    return "系统治疗"

# ===== 主要处理逻辑 =====
def main():
    print("=" * 60)
    print("ASCRS指南批量解析程序")
    print("=" * 60)

    # 加载现有知识库
    if os.path.exists(MAIN_KB):
        with open(MAIN_KB, "r", encoding="utf-8") as f:
            main_kb = json.load(f)
        print(f"✓ 主知识库加载成功，共 {len(main_kb)} 条\n")
    else:
        main_kb = []
        print("⚠ 主知识库不存在，将创建新库\n")

    all_new_triplets = []

    for filename in FILES_TO_PROCESS:
        filepath = os.path.join(GUIDE_DIR, filename)
        key = file_to_key(filename)
        source_info = PDF_MAP.get(key, {
            "title": filename,
            "source": f"ASCRS Guidelines - {filename}",
            "evidence": "I级专家共识"
        })

        if not os.path.exists(filepath):
            print(f"⚠ 文件不存在: {filename}")
            continue

        print(f"\n📄 处理: {filename}")
        print(f"   标题: {source_info['title']}")

        try:
            with pdfplumber.open(filepath) as pdf:
                print(f"   页数: {len(pdf.pages)}")
                full_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"

                # 提取三元组
                triplets = extract_triplets(full_text, source_info)
                print(f"   提取: {len(triplets)} 条知识三元组")

                # 进一步从文本中提取结构化内容
                # 重点提取推荐意见和关键数据
                structured = extract_structured_recommendations(full_text, source_info)
                print(f"   结构化提取: {len(structured)} 条")

                all_new_triplets.extend(triplets)
                all_new_triplets.extend(structured)

        except Exception as e:
            print(f"   ❌ 错误: {e}")

    # 去重
    seen = set()
    unique_triplets = []
    for t in all_new_triplets:
        key = (t.get("head", ""), t.get("relation", ""), t.get("tail", ""))
        if key not in seen and len(t["tail"]) > 10:
            seen.add(key)
            unique_triplets.append(t)

    print(f"\n{'=' * 60}")
    print(f"总计提取: {len(all_new_triplets)} 条，去重后: {len(unique_triplets)} 条")
    print(f"{'=' * 60}")

    # 保存ASCRS扩展包
    with open(OUT_EXTENDED, "w", encoding="utf-8") as f:
        json.dump(unique_triplets, f, ensure_ascii=False, indent=2)
    print(f"\n✓ ASCRS知识扩展包已保存: {OUT_EXTENDED}")

    # 合并到主知识库
    main_kb_extended = main_kb + unique_triplets

    # 保存扩展版主库
    with open(MAIN_KB, "w", encoding="utf-8") as f:
        json.dump(main_kb_extended, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 主知识库已更新: {len(main_kb)} → {len(main_kb_extended)} 条")
    print(f"   新增: {len(unique_triplets)} 条ASCRS指南知识")

    return unique_triplets

def extract_structured_recommendations(text, source_info):
    """从指南文本中提取结构化推荐意见"""
    triplets = []
    lines = text.split("\n")

    current_section = "一般原则"

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # 识别章节标题
        if len(line) < 60 and (line.isupper() or re.match(r"^\d+\.", line) or "#" in line):
            current_section = line[:50]

        # 跳过参考文献
        if re.match(r"^\[\d+\]", line) or re.match(r"^References?.*\d+$", line, re.IGNORECASE):
            continue

        # 提取推荐语句
        rec_keywords = [
            "推荐", "建议", "强推荐", "强烈建议",
            "recommend", "suggest", "should be", "is indicated",
            "may be considered", "is preferred", "is not recommended"
        ]

        if any(kw in line.lower() for kw in rec_keywords):
            if len(line) > 15 and len(line) < 200:
                domain = infer_domain(current_section, line)
                triplets.append({
                    "head": domain_to_entity(domain, line),
                    "relation": "ASCRS推荐",
                    "tail": line.strip(),
                    "source": source_info["source"],
                    "evidence": "I级专家共识",
                    "domain": domain
                })

        # 提取分期相关
        stage_keywords = ["T1", "T2", "T3", "T4", "N0", "N1", "N2", "M0", "M1"]
        for sk in stage_keywords:
            if sk in line and len(line) > 20:
                domain = infer_domain(current_section, line)
                triplets.append({
                    "head": f"结直肠癌{sk}期",
                    "relation": "分期管理",
                    "tail": line.strip()[:150],
                    "source": source_info["source"],
                    "evidence": "I级专家共识",
                    "domain": domain
                })

        # 提取关键数值（生存率、5年生存等）
        survival_match = re.findall(r"(\d+\.?\d*%)\s*(5年|生存|OS|PFS|DFS|总生存|无病生存)", line)
        for pct, label in survival_match:
            if len(line) > 20:
                domain = infer_domain(current_section, line)
                triplets.append({
                    "head": f"{label}率",
                    "relation": "临床预后",
                    "tail": line.strip()[:150],
                    "source": source_info["source"],
                    "evidence": "I级专家共识",
                    "domain": "病理·营养·预后"
                })

        # 提取评分量表
        scale_patterns = [
            ("GFI", "衰弱评估"),
            ("mFI", "衰弱评估"),
            ("ECOG", "体能评估"),
            ("ASA", "麻醉分级"),
            ("Charlson", "合并症评估"),
            ("APGAR", "造口评估"),
            ("LARS", "直肠癌术后功能"),
        ]
        for scale, context in scale_patterns:
            if scale in line and len(line) > 15:
                triplets.append({
                    "head": scale,
                    "relation": context,
                    "tail": line.strip()[:150],
                    "source": source_info["source"],
                    "evidence": "I级专家共识",
                    "domain": "围手术期管理"
                })

    return triplets

def infer_domain(section, line):
    section_lower = section.lower()
    line_lower = line.lower()

    if any(kw in section_lower or kw in line_lower for kw in ["化疗", "靶向", "免疫", "治疗", "systemic"]):
        return "系统治疗"
    if any(kw in section_lower or kw in line_lower for kw in ["手术", "切除", "外科", "surgery"]):
        return "外科手术"
    if any(kw in section_lower or kw in line_lower for kw in ["分期", "staging"]):
        return "分期系统"
    if any(kw in section_lower or kw in line_lower for kw in ["随访", "surveillance", "survivorship", "生存"]):
        return "造口·随访·筛查"
    if any(kw in section_lower or kw in line_lower for kw in ["衰弱", "frailty", "老年", "围手术期", "perioperative"]):
        return "围手术期管理"
    if any(kw in section_lower or kw in line_lower for kw in ["阑尾", "appendix", "appendiceal"]):
        return "阑尾肿瘤"
    if any(kw in section_lower or kw in line_lower for kw in ["肛管", "anal", "鳞状", "squamous cell"]):
        return "肛管癌"
    if any(kw in section_lower or kw in line_lower for kw in ["Lynch", "FAP", "遗传", "hereditary", "息肉"]):
        return "基因靶点"
    if any(kw in section_lower or kw in line_lower for kw in ["造口", "ostomy", "ileostomy"]):
        return "造口·随访·筛查"
    if any(kw in section_lower or kw in line_lower for kw in ["LARS", "低位前切", "功能", "肠道"]):
        return "LARS与并发症"
    if any(kw in section_lower or kw in line_lower for kw in ["病理", "营养", "预后", "生存", "pathology"]):
        return "病理·营养·预后"
    if any(kw in section_lower or kw in line_lower for kw in ["基因", "分子", "biomarker", "mutation"]):
        return "基因靶点"

    return "系统治疗"

def domain_to_entity(domain, line):
    mapping = {
        "系统治疗": "结直肠癌",
        "外科手术": "结直肠癌外科",
        "分期系统": "结直肠癌分期",
        "造口·随访·筛查": "结直肠癌随访",
        "围手术期管理": "结直肠癌围手术期",
        "阑尾肿瘤": "阑尾肿瘤",
        "肛管癌": "肛管癌",
        "基因靶点": "结直肠癌分子标志物",
        "LARS与并发症": "直肠癌术后功能",
        "病理·营养·预后": "结直肠癌预后",
    }
    return mapping.get(domain, "结直肠癌")

if __name__ == "__main__":
    main()
