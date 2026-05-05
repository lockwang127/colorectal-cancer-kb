# 知识图谱关系数据模式

本文件定义知识三元组的数据格式。

## 关系（Relation）格式

```json
{
  "subject": "主体（字符串，必填）",
  "predicate": "谓词（字符串，必填）",
  "object": "客体（字符串，必填）",
  "conditions": {
    "条件1": "值1",
    "条件2": "值2"
  },
  "evidence_level": "证据等级（字符串，必填）",
  "source": "来源（字符串，必填）",
  "contributor": "贡献者（字符串，必填）",
  "date_added": "添加日期（ISO 8601，必填）",
  "confidence": "置信度（0.0-1.0，必填）",
  "note": "备注（字符串，可选）"
}
```

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `subject` | string | ✅ | 知识主体，如"结直肠癌" |
| `predicate` | string | ✅ | 关系谓词，如"一线治疗" |
| `object` | string | ✅ | 知识客体，如"FOLFOX方案" |
| `conditions` | object | ❌ | 适用条件（如分期、基因型） |
| `evidence_level` | string | ✅ | "I级" / "II级" / "III级" / "专家共识" |
| `source` | string | ✅ | 来源指南/文献 |
| `contributor` | string | ✅ | 贡献者姓名 |
| `date_added` | string | ✅ | ISO 8601格式，如"2026-05-06" |
| `confidence` | float | ✅ | 0.0-1.0，知识置信度 |
| `note` | string | ❌ | 补充说明 |

## 示例

```json
[
  {
    "subject": "结直肠癌",
    "predicate": "一线治疗",
    "object": "FOLFOX方案",
    "conditions": {
      "分期": "IV期",
      "MSI状态": "MSS"
    },
    "evidence_level": "I级",
    "source": "CSCO 2024",
    "contributor": "汪晓东",
    "date_added": "2026-05-06",
    "confidence": 0.95
  },
  {
    "subject": "KRAS G12C突变",
    "predicate": "可用药物",
    "object": "Sotorasib",
    "conditions": {
      "线数": "后线"
    },
    "evidence_level": "II级",
    "source": "NCCN 2024",
    "contributor": "汪晓东",
    "date_added": "2026-05-06",
    "confidence": 0.85
  }
]
```

## 谓词（Predicate）推荐值

| 谓词 | 说明 | 示例 |
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

**维护者**: 汪晓东  
**最后更新**: 2026-05-06
