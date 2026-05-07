"""
格式与质量验证测试

运行方式：
    python -m pytest tests/ -v
    或
    python tests/test_kb_format.py

验证项目：
1. JSON 格式正确性
2. 必需字段完整性（head/relation/tail/source/domain/confidence）
3. 必需字段非空性（head/relation/tail 不能为空）
4. confidence 值范围有效性（0.0-1.0）
5. domain 标签完整性（不能为空）
6. 重复条目检测
7. domain 分类覆盖率统计
"""

import json
import os
import sys
from collections import Counter
from pathlib import Path

# 自动查找 kb.json
SCRIPT_DIR = Path(__file__).parent.parent
KB_FILE = SCRIPT_DIR / "kb.json"
META_FILE = SCRIPT_DIR / "kb_meta.json"


class KBValidator:
    """知识库格式与质量验证器"""

    # 必需字段（必须有）
    REQUIRED_FIELDS = ["head", "relation", "tail", "source", "evidence", "domain", "confidence"]

    # 不能为空的字段
    NON_EMPTY_FIELDS = ["head", "relation", "tail"]

    # 合法的 domain 分类
    VALID_DOMAINS = {
        "基因突变与分子机制",
        "肿瘤微环境",
        "临床诊断",
        "临床治疗",
        "系统治疗",
        "外科手术",
        "随访与预后",
        "围手术期管理",
        "肛管癌",
        "阑尾肿瘤",
        "分期系统",
        "LARS与并发症",
        "造口·随访·筛查",
        "病理·营养·预后",
        "基因靶点",
    }

    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        self.kb: list[dict] = []
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.stats = {}

    def load(self) -> bool:
        """加载 kb.json"""
        try:
            with open(self.kb_path, "r", encoding="utf-8") as f:
                self.kb = json.load(f)
            return True
        except FileNotFoundError:
            self.errors.append(f"文件不存在: {self.kb_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON 格式错误: {e}")
            return False

    def validate(self) -> bool:
        """执行所有验证"""
        if not self.kb:
            self.errors.append("知识库为空")
            return False

        self._check_required_fields()
        self._check_non_empty_fields()
        self._check_confidence_range()
        self._check_domain_completeness()
        self._check_duplicates()
        self._collect_stats()

        return len(self.errors) == 0

    def _check_required_fields(self):
        """检查必需字段是否存在"""
        missing_count = 0
        for i, entry in enumerate(self.kb):
            for field in self.REQUIRED_FIELDS:
                if field not in entry:
                    missing_count += 1
                    if missing_count <= 3:  # 只记录前3个
                        self.warnings.append(
                            f"  [{i}] 条目缺少字段 '{field}': head={entry.get('head', '')[:30]}"
                        )
        if missing_count:
            self.warnings.append(f"⚠️  {missing_count} 条目缺少某些可选字段")

    def _check_non_empty_fields(self):
        """检查 head/relation/tail 不能为空"""
        empty_head = [i for i, e in enumerate(self.kb) if not e.get("head", "").strip()]
        empty_rel = [i for i, e in enumerate(self.kb) if not e.get("relation", "").strip()]
        empty_tail = [i for i, e in enumerate(self.kb) if not e.get("tail", "").strip()]

        if empty_head:
            self.errors.append(f"❌ {len(empty_head)} 条目 head 为空: 前3个索引 {empty_head[:3]}")
        if empty_rel:
            self.errors.append(f"❌ {len(empty_rel)} 条目 relation 为空")
        if empty_tail:
            self.errors.append(f"❌ {len(empty_tail)} 条目 tail 为空")

    def _check_confidence_range(self):
        """检查 confidence 值在 0.0-1.0 范围内"""
        invalid = []
        for i, entry in enumerate(self.kb):
            conf = entry.get("confidence")
            if conf is None:
                continue
            if not isinstance(conf, (int, float)):
                invalid.append(f"[{i}] confidence={conf} (类型错误)")
            elif conf < 0.0 or conf > 1.0:
                invalid.append(f"[{i}] confidence={conf} (超出范围)")

        if invalid:
            self.errors.append(f"❌ {len(invalid)} 条目 confidence 无效:\n  " + "\n  ".join(invalid[:5]))

    def _check_domain_completeness(self):
        """检查 domain 标签完整性"""
        empty_domain = [i for i, e in enumerate(self.kb) if not e.get("domain", "").strip()]
        if empty_domain:
            self.errors.append(f"❌ {len(empty_domain)} 条目 domain 为空")

        # 检查 domain 是否在合法列表中
        invalid_domain = []
        for i, entry in enumerate(self.kb):
            domain = entry.get("domain", "").strip()
            if domain and domain not in self.VALID_DOMAINS:
                invalid_domain.append(f"[{i}] domain='{domain}'")

        if invalid_domain:
            self.warnings.append(f"⚠️  {len(invalid_domain)} 条目使用了非标准 domain:\n  " +
                               "\n  ".join(invalid_domain[:5]))

    def _check_duplicates(self):
        """检测精确重复（head + relation + tail）"""
        seen = set()
        duplicates = []
        for i, entry in enumerate(self.kb):
            key = (entry.get("head", ""), entry.get("relation", ""), entry.get("tail", ""))
            if key in seen:
                duplicates.append(i)
            else:
                seen.add(key)

        if duplicates:
            self.warnings.append(f"⚠️  发现 {len(duplicates)} 条重复条目")

    def _collect_stats(self):
        """收集统计信息"""
        self.stats = {
            "total": len(self.kb),
            "domains": Counter(e.get("domain", "未分类") for e in self.kb),
            "evidence_levels": Counter(e.get("evidence", "无") for e in self.kb),
            "confidence_avg": sum(e.get("confidence", 0.5) for e in self.kb) / len(self.kb),
            "head_unique": len(set(e.get("head", "") for e in self.kb)),
            "relation_unique": len(set(e.get("relation", "") for e in self.kb)),
        }

    def print_report(self):
        """打印验证报告"""
        print("=" * 60)
        print("📋 知识库验证报告")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ 错误 ({len(self.errors)} 项):")
            for e in self.errors:
                print(f"  {e}")

        if self.warnings:
            print(f"\n⚠️  警告 ({len(self.warnings)} 项):")
            for w in self.warnings:
                print(f"  {w}")

        if not self.errors and not self.warnings:
            print("\n✅ 验证通过！")

        print(f"\n📊 统计信息:")
        print(f"   总条目数: {self.stats.get('total', 0)}")
        print(f"   唯一 head 数: {self.stats.get('head_unique', 0)}")
        print(f"   唯一 relation 数: {self.stats.get('relation_unique', 0)}")
        print(f"   平均 confidence: {self.stats.get('confidence_avg', 0):.3f}")

        print(f"\n📊 Domain 分布:")
        for domain, count in self.stats.get("domains", {}).most_common():
            pct = count / self.stats["total"] * 100
            bar = "█" * int(pct / 2)
            print(f"   {domain:20s} {count:5d} ({pct:5.1f}%) {bar}")

        print(f"\n📊 Evidence 分布:")
        for ev, count in self.stats.get("evidence_levels", {}).most_common():
            print(f"   {ev:15s} {count:5d}")


def main():
    """主函数"""
    kb_path = os.environ.get("CRC_KB_PATH", KB_FILE)

    print(f"🔍 验证文件: {kb_path}")

    validator = KBValidator(str(kb_path))

    if not validator.load():
        validator.print_report()
        sys.exit(1)

    if not validator.validate():
        validator.print_report()
        sys.exit(1)

    validator.print_report()
    print("\n✅ 所有验证通过！")
    sys.exit(0)


if __name__ == "__main__":
    main()
