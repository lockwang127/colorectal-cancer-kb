"""
从原始 colorectal-cancer-kb-main/data/knowledge-graph/ 合并所有 JSON 文件，
统一格式、去重，输出 kb.json。

用法：
    python build_kb.py

环境变量（可选）：
    CRC_KB_SRC   - 源数据目录路径
    CRC_KB_OUT   - 输出文件路径
    CRC_KB_VER   - 版本号（如 "1.0.0"）

默认：相对于本脚本所在目录的相对路径
"""

import json
import os
import sys
from datetime import datetime

# ============================================================
# 路径配置：支持环境变量覆盖
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 默认路径（相对于脚本位置）
DEFAULT_SRC = os.path.join(SCRIPT_DIR, "../prof.wang/colorectal-cancer-kb-main/data/knowledge-graph")
DEFAULT_OUT = os.path.join(SCRIPT_DIR, "kb.json")

SRC_DIR = os.environ.get("CRC_KB_SRC", DEFAULT_SRC)
OUT_FILE = os.environ.get("CRC_KB_OUT", DEFAULT_OUT)
VERSION = os.environ.get("CRC_KB_VER", "1.0.0")

# ============================================================
# Domain 标签修复映射（用于自动补充空 domain）
# ============================================================
# head → domain 的映射规则（按关键词匹配）
DOMAIN_RULES: list[tuple[list[str], str]] = [
    # 基础生物学
    (["KRAS", "NRAS", "BRAF", "PIK3CA", "PTEN", "APC", "SMAD4", "TP53", "TGFBR2",
      "基因", "突变", "分子特征", "分子分型", "CMS", "MSI", "dMMR", "林奇综合征"],
     "基因突变与分子机制"),
    # 肿瘤微环境
    (["免疫", "T细胞", "PD-1", "PD-L1", "CTLA-4", "肿瘤微环境", "TME", "CAF",
      "髓系", "巨噬细胞", "淋巴细胞"],
     "肿瘤微环境"),
    # 临床诊断
    (["筛查", "流行病学", "危险因素", "分期", "分期系统", "AJCC", "TNM"],
     "临床诊断"),
    # 病理
    (["病理", "分化", "分化程度", "脉管侵犯", "神经侵犯", "出芽", "肿瘤沉积"],
     "临床诊断"),
    # 临床治疗 - 外科
    (["手术", "TME", "taTME", "MiTME", "机器人", "腹腔镜", "开腹", "CME",
      "保肛", "造口", "吻合口漏", "APR", "ISR", "切除范围"],
     "临床治疗"),
    # 临床治疗 - 系统治疗
    (["化疗", "靶向", "免疫治疗", "新辅助", "辅助化疗", "FOLFOX", "FOLFIRI",
      "FOLFOXIRI", "卡培他滨", "贝伐单抗", "西妥昔单抗", "帕尼单抗",
      "Pembrolizumab", "Nivolumab", "nivolumab", "pembrolizumab"],
     "临床治疗"),
    # 随访与预后
    (["随访", "监测", "LARS", "生活质量", "功能结局", "造口管理"],
     "随访与预后"),
    # 肛管癌
    (["肛管", "肛门"],
     "肛管癌"),
    # 阑尾肿瘤
    (["阑尾"],
     "阑尾肿瘤"),
    # 围手术期
    (["围手术期", "ERAS", "营养", "衰弱", "ASA", "麻醉", "并发症", "加速康复"],
     "围手术期管理"),
]


def infer_domain(head: str, existing_domain: str) -> str:
    """根据 head 内容推断并补充 domain 标签"""
    if existing_domain and existing_domain.strip():
        return existing_domain.strip()

    head_lower = head.lower()
    for keywords, domain in DOMAIN_RULES:
        if any(kw.lower() in head_lower for kw in keywords):
            return domain
    return "临床治疗"  # 默认归入临床治疗


def normalize(entry: dict) -> dict:
    """统一两种 schema → 标准五元组 + 元数据"""
    if "head" in entry:
        # Schema A: head/relation/tail
        base = {
            "head": entry["head"],
            "relation": entry["relation"],
            "tail": entry["tail"],
            "source": entry.get("source", ""),
            "evidence": entry.get("evidence", entry.get("evidence_level", "")),
            "domain": infer_domain(entry["head"], entry.get("domain", "")),
            "confidence": entry.get("confidence", 0.5),
            "conditions": entry.get("conditions", None),
        }
    else:
        # Schema B: subject/predicate/object
        base = {
            "head": entry.get("subject", ""),
            "relation": entry.get("predicate", ""),
            "tail": entry.get("object", ""),
            "source": entry.get("source", ""),
            "evidence": entry.get("evidence_level", entry.get("evidence", "")),
            "domain": infer_domain(entry.get("subject", ""), entry.get("domain", "")),
            "confidence": entry.get("confidence", 0.5),
            "conditions": entry.get("conditions", None),
        }

    # 可选字段
    if entry.get("pmid"):
        base["pmid"] = entry["pmid"]

    base["update_date"] = datetime.now().strftime("%Y-%m-%d")

    return base


def build():
    # 检查源目录
    if not os.path.isdir(SRC_DIR):
        print(f"❌ 错误：源目录不存在: {SRC_DIR}")
        print(f"   可设置环境变量 CRC_KB_SRC 指定正确的路径")
        sys.exit(1)

    # 确保输出目录存在
    out_dir = os.path.dirname(OUT_FILE)
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    print(f"📂 源目录: {SRC_DIR}")
    print(f"📄 输出文件: {OUT_FILE}")
    print(f"🏷️  版本: {VERSION}")
    print()

    all_entries = []
    seen = set()
    stats = {"total": 0, "duplicates": 0, "by_file": {}}

    for fname in sorted(os.listdir(SRC_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(SRC_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"  ⚠ skip [{fname}]: {e}")
            continue

        if not isinstance(data, list):
            print(f"  - [{fname}]: 非列表格式，跳过")
            continue
        if len(data) == 0:
            print(f"  - [{fname}]: 空列表")
            continue

        added = 0
        skipped_dup = 0
        for entry in data:
            stats["total"] += 1
            norm = normalize(entry)
            key = (norm["head"], norm["relation"], norm["tail"])
            if key in seen:
                skipped_dup += 1
                stats["duplicates"] += 1
                continue
            seen.add(key)
            all_entries.append(norm)
            added += 1

        stats["by_file"][fname] = {"added": added, "skipped": skipped_dup}
        dup_note = f" (跳过 {skipped_dup} 重复)" if skipped_dup else ""
        print(f"  + [{fname}]: {added} 条新条目{dup_note}")

    # 写入 kb.json
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完成: {len(all_entries)} 条唯一条目 (去重 {stats['duplicates']} 条)")
    print(f"📄 输出: {OUT_FILE}")

    # 统计 domain 分布
    domains: dict[str, int] = {}
    sources: dict[str, int] = {}
    evidence_levels: dict[str, int] = {}

    for e in all_entries:
        d = e.get("domain") or "未分类"
        domains[d] = domains.get(d, 0) + 1

        s = e.get("source", "")[:60]
        if s:
            sources[s] = sources.get(s, 0) + 1

        ev = e.get("evidence", "") or "无等级"
        evidence_levels[ev] = evidence_levels.get(ev, 0) + 1

    print(f"\n📊 Domain 分布:")
    for d, c in sorted(domains.items(), key=lambda x: -x[1]):
        print(f"   {d}: {c}")

    print(f"\n📊 Evidence 分布:")
    for ev, c in sorted(evidence_levels.items(), key=lambda x: -x[1]):
        print(f"   {ev}: {c}")

    print(f"\n📊 Top 来源 (前5):")
    for s, c in sorted(sources.items(), key=lambda x: -x[1])[:5]:
        print(f"   {s}: {c}")

    # 生成 kb_meta.json
    meta_out = os.path.join(os.path.dirname(OUT_FILE), "kb_meta.json")
    meta = {
        "version": VERSION,
        "update_date": datetime.now().strftime("%Y-%m-%d"),
        "total_entries": len(all_entries),
        "total_duplicates_removed": stats["duplicates"],
        "source_files": stats["by_file"],
        "domains": domains,
        "evidence_levels": evidence_levels,
        "top_sources": dict(sorted(sources.items(), key=lambda x: -x[1])[:10]),
    }
    with open(meta_out, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"\n📋 元数据: {meta_out}")


if __name__ == "__main__":
    build()
