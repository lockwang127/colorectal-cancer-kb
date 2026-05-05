# 结直肠癌通用知识库 (Colorectal Cancer Knowledge Base)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-orange.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![GitHub stars](https://img.shields.io/github/stars/wangxiaodong/colorectal-cancer-kb.svg)](https://github.com/wangxiaodong/colorectal-cancer-kb)
[![GitHub forks](https://img.shields.io/github/forks/wangxiaodong/colorectal-cancer-kb.svg)](https://github.com/wangxiaodong/colorectal-cancer-kb/network)
[![Last Commit](https://img.shields.io/github/last-commit/wangxiaodong/colorectal-cancer-kb.svg)](https://github.com/wangxiaodong/colorectal-cancer-kb/commits)

🏥 一个结构化、开源的结直肠癌医学知识库，支持临床决策、科研查询与AI应用。

---

## 📖 简介

本项目旨在构建一个**结构化、机器可读、可扩展**的结直肠癌医学知识库，包括：

- 📚 **指南共识摘要**（CSCO/NCCN/ESMO等，基于transformative use整理）
- 🧬 **知识图谱**（疾病-治疗-生物标记物关系网络）
- 💊 **药物知识库**（化疗、靶向、免疫药物的结构化数据）
- 🔬 **临床研究数据**（重要临床试验的关键数据提取）
- 📊 **流行病学统计**（发病、预后、筛查数据）

**本知识库强调**：
- ✅ **独立自主知识产权**：所有内容为整理、解读、再创作的成果
- ✅ **开源共享**：采用CC BY-NC-SA 4.0协议，允许非商业使用与演绎
- ✅ **可追溯**：每条知识均标注原始来源
- ✅ **AI-ready**：JSON格式结构化数据，便于RAG、知识图谱等AI应用

---

## 🎯 应用场景

| 应用 | 说明 |
|------|------|
| **临床决策支持** | 基于指南的推荐，辅助诊疗决策 |
| **医学AI训练** | 为医疗大模型提供结构化训练数据 |
| **患者教育** | 生成患者易懂的科普内容 |
| **科研查询** | 快速检索临床试验、药物信息 |
| **医疗质量改进** | 对照指南，评估诊疗规范性 |

---

## 📂 仓库结构

```
colorectal-cancer-kb/
├── data/                         # 核心数据
│   ├── guidelines/               # 指南共识摘要
│   │   ├── csco/                # CSCO指南年度更新点
│   │   ├── nccn/                # NCCN指南关键结论
│   │   └── esmo/                # ESMO共识
│   ├── knowledge-graph/          # 知识图谱三元组
│   ├── clinical-data/            # 临床研究数据
│   └── drugs/                   # 药物知识
├── schemas/                      # 数据模式定义（JSON Schema）
├── scripts/                      # 数据处理脚本（Mac/Linux）
├── docs/                        # 文档
└── obsidian-export/             # Obsidian格式导出
```

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/wangxiaodong/colorectal-cancer-kb.git
cd colorectal-cancer-kb
```

### 2. 查看指南摘要

```bash
cat data/guidelines/csco/csco-2024-colon.md
```

### 3. 加载知识图谱

```python
import json

with open('data/knowledge-graph/relations.json', 'r') as f:
    relations = json.load(f)

print(f"知识三元组数量：{len(relations)}")
```

### 4. 运行数据校验

```bash
python scripts/validate_data.py
```

---

## 📝 贡献指南

我们欢迎医学专业人士、AI研究者、开发者的贡献！

详见：[CONTRIBUTING.md](CONTRIBUTING.md)

**贡献方式**：
- 📚 补充指南摘要（请提供原始文献链接）
- 🧬 添加知识三元组
- 💊 完善药物知识
- 🐛 报告错误或提出改进建议

---

## ⚖️ 知识产权与版权声明

### 本项目的知识产权
- **代码、脚本、文档结构**：MIT License
- **医学知识内容（摘要、解读、结构化数据）**：CC BY-NC-SA 4.0
  - ✅ 允许：分享、演绎、用于研究/教育
  - ❌ 禁止：商业使用（需单独授权）

### 版权尊重
- ❌ **不包含**任何指南、文献的全文复制
- ✅ **仅包含**基于transformative use的摘要、解读、知识提取
- ✅ **所有内容**均标注原始来源链接，尊重原作者版权

---

## 📊 数据质量

| 数据类型 | 当前条目 | 目标条目 | 质量等级 |
|----------|----------|----------|----------|
| 指南摘要 | 0（初始化中） | 50+ | 高 |
| 知识三元组 | 0（初始化中） | 2000+ | 中高 |
| 药物知识 | 0（初始化中） | 100+ | 高 |
| 临床试验 | 0（初始化中） | 300+ | 中 |

---

## 🛠️ 技术栈

- **数据格式**：JSON（结构化）+ Markdown（人类可读）
- **校验**：JSON Schema + Python脚本
- **知识图谱**：JSON-LD / RDF（规划中）
- **Obsidian兼容**：所有Markdown文件均可直接导入Obsidian

---

## 📧 联系我们

- **项目负责人**：汪晓东（四川大学华西医院胃肠外科）
- **Email**：[请联系通过GitHub Issue](https://github.com/wangxiaodong/colorectal-cancer-kb/issues)
- **机构**：四川大学华西医院

---

## 📄 许可证

```
医学知识内容：CC BY-NC-SA 4.0
代码/脚本：MIT License
```

详见：[LICENSE](LICENSE) 文件。

---

## ⭐ Star History

如果这个知识库对您有帮助，请给我们一个星标！

[![Star History Chart](https://api.star-history.com/svg?repos=wangxiaodong/colorectal-cancer-kb&type=Date)](https://star-history.com/#wangxiaodong/colorectal-cancer-kb&Date)

---

**Disclaimer**：本知识库仅供医学专业人士参考，不构成临床诊疗建议。临床决策请务必结合患者具体情况和最新指南。
