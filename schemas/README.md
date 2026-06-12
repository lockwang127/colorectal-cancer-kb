# Knowledge Graph Relation Schema

本文件定义结直肠癌知识三元组的当前数据格式。主格式为 `head / relation / tail`，早期 `subject / predicate / object` 字段仅用于历史兼容。

## 关系（Relation）格式

```json
{
  "head": "主体（字符串，必填）",
  "relation": "关系（字符串，必填）",
  "tail": "客体或结论（字符串，必填）",
  "source": "来源指南、共识或文献（字符串，必填）",
  "evidence": "证据等级或证据类型（字符串，必填）",
  "domain": "知识域（字符串，必填）",
  "confidence": "置信度（0.0-1.0，推荐）",
  "conditions": {
    "条件1": "值1",
    "条件2": "值2"
  },
  "note": "备注（字符串，可选）"
}
```

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `head` | string | ✅ | 知识主体，如"转移性结直肠癌" |
| `relation` | string | ✅ | 关系，如"一线治疗方案" |
| `tail` | string | ✅ | 知识客体、结论或说明 |
| `source` | string | ✅ | 来源指南、共识、文献或数据批次 |
| `evidence` | string | ✅ | "I级" / "II级" / "III级" / "专家共识" / 文献证据 |
| `domain` | string | ✅ | 知识域，如"系统治疗"、"外科手术" |
| `confidence` | float | 推荐 | 0.0-1.0，知识置信度；批量抽取数据可后续补齐 |
| `conditions` | object | ❌ | 适用条件（如分期、基因型） |
| `note` | string | ❌ | 补充说明 |

## 示例

```json
[
  {
    "head": "转移性结直肠癌",
    "relation": "一线治疗方案",
    "tail": "FOLFOX 或 CAPEOX 可作为常用化疗骨架",
    "conditions": {
      "分期": "IV期",
      "MSI状态": "MSS"
    },
    "source": "CSCO 2024",
    "evidence": "I级",
    "domain": "系统治疗",
    "confidence": 0.95
  },
  {
    "head": "KRAS G12C突变",
    "relation": "后线治疗探索",
    "tail": "KRAS G12C 抑制剂联合策略仍需结合适应证、可及性和证据等级评估",
    "conditions": {
      "线数": "后线"
    },
    "source": "NCCN 2024",
    "evidence": "II级",
    "domain": "系统治疗",
    "confidence": 0.85
  }
]
```

## Relation 推荐方向

| Relation | 说明 | 示例 |
|-------|------|------|
| `一线治疗` | 一线治疗方案 | 结直肠癌 → FOLFOX |
| `可用药物` | 可用的药物 | KRAS突变 → Sotorasib |
| `禁忌症` | 禁忌情况 | 呋喹替尼 → 重度肝损伤 |
| `生物标记物` | 相关标记物 | 结直肠癌 → KRAS |
| `并发症` | 常见并发症 | LARS → 排便急迫 |
| `危险因素` | 危险因素 | 结直肠癌 → 红肉饮食 |
| `筛查方法` | 筛查手段 | 结直肠癌 → 结肠镜 |
| `预后因素` | 预后相关因素 | MSI-H → 较好预后 |

---

Last updated: 2026-05-07
