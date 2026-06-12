# Colorectal Cancer Knowledge Graph Data

## 本目录说明

本目录保存结直肠癌知识库的结构化三元组批次。当前主格式使用 `head / relation / tail`，同时保留少量早期 `subject / predicate / object` 文件以兼容历史数据。

---

## 当前状态

- Current release: `v1.0.0`
- Updated: `2026-05-07`
- Structured triplets: `3,738`
- Knowledge domains: `27`
- Source batches: `18`

---

## 如何添加数据

### 方式一：直接编辑 JSON 文件

1. 打开相应主题批次文件，或在 `relations.json` 中追加经整理后的三元组。
2. 使用 `head / relation / tail / source / evidence / domain` 格式，并尽量补充 `confidence`。
3. 运行校验脚本：
   ```bash
   python3 scripts/validate_data.py
   ```
4. 提交 PR。

### 方式二：使用 Python 脚本添加

```python
import json

# 读取现有数据
with open('relations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 添加新三元组
new_relation = {
    "head": "转移性结直肠癌",
    "relation": "一线治疗方案",
    "tail": "FOLFOX 或 CAPEOX 可作为常用化疗骨架",
    "conditions": {"分期": "IV期"},
    "evidence": "I级",
    "source": "CSCO 2024",
    "domain": "系统治疗",
    "confidence": 0.95
}

data.append(new_relation)

# 保存
with open('relations.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

---

## 数据质量检查

- ✅ 所有必填字段完整
- ✅ `evidence` 符合规范
- ✅ `source` 可追溯
- ✅ `domain` 属于结直肠癌知识库范围
- ✅ 无重复三元组
- ✅ JSON 格式正确

---
