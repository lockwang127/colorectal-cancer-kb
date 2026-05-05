# 结直肠癌通用知识库 - 贡献指南

感谢您考虑为这个知识库做出贡献！

---

## 🌟 我们欢迎以下类型的贡献

### 1. 医学知识贡献（医学专业人士）
- 📚 **指南摘要**：整理各大指南（CSCO/NCCN/ESMO等）的更新要点
- 🧬 **知识三元组**：添加疾病-治疗-生物标记物之间的关系
- 💊 **药物知识**：补充/修正药物的结构化数据
- 🔬 **临床研究**：添加重要临床试验的关键数据
- 📊 **流行病学数据**：补充发病率、预后等统计数据

### 2. 技术贡献（开发者/AI研究者）
- 🐛 **代码改进**：优化数据处理脚本
- 📐 **Schema设计**：完善数据模式定义
- 🔍 **数据校验**：编写数据质量检查工具
- 🤖 **AI应用**：基于本知识库开发应用（需遵守许可证）

### 3. 文档贡献
- 📝 **翻译**：将指南摘要翻译为英文/其他语言
- 📖 **使用文档**：编写教程、最佳实践
- 🎨 **可视化**：设计知识图谱可视化工具

---

## 📋 贡献流程

### 方式一：Fork + Pull Request（推荐）

```bash
# 1. Fork 本仓库到你的 GitHub 账号
# 2. 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/colorectal-cancer-kb.git
cd colorectal-cancer-kb

# 3. 创建新分支
git checkout -b feature/add-csco-2024-summary

# 4. 进行修改
# 添加/修改文件...

# 5. 提交变更
git add .
git commit -m "添加CSCO 2024结肠癌指南摘要"

# 6. 推送到你的 Fork
git push origin feature/add-csco-2024-summary

# 7. 在 GitHub 上创建 Pull Request
```

### 方式二：直接提交 Issue
如果您不确定如何提交 PR，可以：
1. 在 [Issues](https://github.com/wangxiaodong/colorectal-cancer-kb/issues) 中描述您的建议
2. 我们的维护者会帮您实现

---

## 📐 数据格式规范

### 1. 指南摘要（Markdown）

**文件位置**：`data/guidelines/{source}/{year}-{disease}.md`

**格式要求**：
```markdown
---
title: "指南标题"
year: 2024
source: "指南全称"
type: "guideline_summary"
tags: ["标签1", "标签2"]
contributor: "贡献者姓名"
date_added: "2026-05-06"
---

# 指南标题

## 关键更新
### 1. 更新点标题
- **更新内容**：...
- **证据等级**：...
- **适用人群**：...

## 与上一版本差异
...

## 贡献者解读
（您的专业解读，这是transformative work）
```

**版权要求**：
- ❌ **不要**复制指南原文超过400字
- ✅ **要做**原创摘要、解读、知识提取
- ✅ **必须**标注原始来源链接

---

### 2. 知识三元组（JSON）

**文件位置**：`data/knowledge-graph/relations.json`

**格式要求**：
```json
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
  "contributor": "贡献者姓名",
  "date_added": "2026-05-06",
  "confidence": 0.95
}
```

**质量要求**：
- `evidence_level`：必须是 "I级" / "II级" / "III级" / "专家共识"
- `confidence`：0.0-1.0，表示知识置信度
- `source`：必须可追溯至原始文献/指南

---

### 3. 药物知识（JSON）

**文件位置**：`data/drugs/{category}.json`

**格式要求**：
```json
{
  "name": "药物名称",
  "english_name": "English name",
  "type": "化疗药|靶向药|免疫药",
  "target": "作用靶点（如适用）",
  "indication": "适应症",
  "dosage": "剂量与用法",
  "common_adverse_events": ["不良反应1", "不良反应2"],
  "contraindications": ["禁忌症1", "禁忌症2"],
  "evidence_level": "证据等级",
  "source": "来源指南",
  "contributor": "贡献者",
  "date_added": "2026-05-06"
}
```

---

## ✅ 提交前检查清单

- [ ] 我的贡献不包含任何受版权保护的全文内容
- [ ] 所有知识条目都标注了原始来源
- [ ] 我遵循了对应的数据格式规范
- [ ] 我运行了数据校验脚本（`python scripts/validate_data.py`）
- [ ] 我的代码/脚本通过了基本测试
- [ ] 我更新了相关的文档（如适用）

---

## 🚀 审查流程

1. **自动检查**：GitHub Actions 会自动运行数据校验
2. **人工审查**：维护者会审查内容的科学准确性
3. **反馈修改**：可能需要您根据反馈进行修改
4. **合并**：审查通过后，您的贡献将被合并到主分支

---

## 💬 行为准则

- 尊重所有贡献者
- 提供建设性的反馈
- 保持科学严谨性
- 尊重知识产权和版权

---

## 📧 联系方式

如有疑问，请：
- 创建 [Issue](https://github.com/wangxiaodong/colorectal-cancer-kb/issues)
- 联系维护者：汪晓东（华西医院）

---

**再次感谢您的贡献！🙏**
