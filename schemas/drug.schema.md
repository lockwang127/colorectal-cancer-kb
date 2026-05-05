# 结直肠癌通用知识库 - 药物知识数据模式

本文件定义药物知识的数据格式。

## 数据格式

### 化疗药（chemotherapy.json）

```json
[
  {
    "name": "FOLFOX方案",
    "english_name": "FOLFOX regimen",
    "type": "化疗方案",
    "components": ["奥沙利铂", "亚叶酸钙", "5-氟尿嘧啶"],
    "indication": "结直肠癌辅助治疗/晚期一线治疗",
    "dosage": "奥沙利铂85mg/m² IV d1；亚叶酸400mg/m² IV d1；5-FU 400mg/m² bolus d1，然后2400mg/m² CIVI 46h",
    "cycle": "每2周重复",
    "common_adverse_events": ["周围神经毒性", "中性粒细胞减少", "黏膜炎"],
    "evidence_level": "I级推荐",
    "source": "CSCO 2024",
    "contributor": "汪晓东",
    "date_added": "2026-05-06"
  }
]
```

### 靶向药（targeted.json）

```json
[
  {
    "name": "西妥昔单抗",
    "english_name": "Cetuximab",
    "type": "靶向药",
    "target": "EGFR",
    "indication": "RAS野生型结直肠癌一线治疗",
    "dosage": "首剂400mg/m²，维持剂量250mg/m²每周",
    "common_adverse_events": ["痤疮样皮疹", "低镁血症", "输液反应"],
    "contraindications": ["RAS突变", "BRAF V600E突变"],
    "evidence_level": "I级推荐",
    "source": "CSCO 2024",
    "contributor": "汪晓东",
    "date_added": "2026-05-06"
  }
]
```

### 免疫药（immunotherapy.json）

```json
[
  {
    "name": "帕博利珠单抗",
    "english_name": "Pembrolizumab",
    "type": "免疫检查点抑制剂",
    "target": "PD-1",
    "indication": "MSI-H/dMMR结直肠癌",
    "dosage": "400mg q4w 或 200mg q3w",
    "common_adverse_events": ["疲劳", "甲状腺功能减退", "免疫相关不良反应"],
    "biomarkers": ["MSI-H", "dMMR", "TMB-H"],
    "evidence_level": "I级推荐",
    "source": "CSCO 2024",
    "contributor": "汪晓东",
    "date_added": "2026-05-06"
  }
]
```

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | 药物中文名 |
| `english_name` | string | ✅ | 英文通用名 |
| `type` | string | ✅ | 药物类型 |
| `target` | string | ❌ | 作用靶点（靶向/免疫药必填） |
| `indication` | string | ✅ | 适应症 |
| `dosage` | string | ✅ | 剂量与用法 |
| `common_adverse_events` | array | ✅ | 常见不良反应 |
| `contraindications` | array | ❌ | 禁忌症 |
| `biomarkers` | array | ❌ | 相关生物标记物 |
| `evidence_level` | string | ✅ | 证据等级 |
| `source` | string | ✅ | 来源指南 |
| `contributor` | string | ✅ | 贡献者 |
| `date_added` | string | ✅ | 添加日期 ISO 8601 |

---

**维护者**: 汪晓东  
**最后更新**: 2026-05-06
