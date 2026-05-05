# 结直肠癌通用知识库 - 初始化数据

## 本目录说明

本目录包含知识图谱的初始三元组数据。

---

## 当前状态

- ✅ Schema 已定义
- 🔄 数据初始化中...
- ⏳ 等待首批贡献

---

## 如何添加数据

### 方式一：直接编辑 JSON 文件

1. 打开 `relations.json`
2. 在数组中添加新的三元组（参考 `../schemas/README.md` 格式）
3. 运行校验脚本：
   ```bash
   python ../scripts/validate_data.py
   ```
4. 提交 PR

### 方式二：使用 Python 脚本添加

```python
import json

# 读取现有数据
with open('relations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 添加新三元组
new_relation = {
    "subject": "结直肠癌",
    "predicate": "一线治疗",
    "object": "FOLFOX方案",
    "conditions": {"分期": "IV期"},
    "evidence_level": "I级",
    "source": "CSCO 2024",
    "contributor": "您的姓名",
    "date_added": "2026-05-06",
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
- ✅ `evidence_level` 符合规范
- ✅ `source` 可追溯
- ✅ 无重复三元组
- ✅ JSON 格式正确

---

**初始化日期**: 2026-05-06  
**维护者**: 汪晓东
