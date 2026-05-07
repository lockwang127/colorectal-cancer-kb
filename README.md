# 结直肠癌通用知识库 (Colorectal Cancer Knowledge Base)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-orange.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![GitHub stars](https://img.shields.io/github/stars/lockwang127/colorectal-cancer-kb.svg)](https://github.com/lockwang127/colorectal-cancer-kb)
[![GitHub forks](https://img.shields.io/github/forks/lockwang127/colorectal-cancer-kb.svg)](https://github.com/lockwang127/colorectal-cancer-kb/network)
[![Last Commit](https://img.shields.io/github/last-commit/lockwang127/colorectal-cancer-kb.svg)](https://github.com/lockwang127/colorectal-cancer-kb/commits)
[![Knowledge Triplets](https://img.shields.io/badge/Knowledge-3738%20Triplets-green.svg)](data/kb.json)

🏥 一个结构化、开源的结直肠癌医学知识库，支持临床决策、科研查询与AI应用。

---

## 🎯 最新更新 (2026-05-07)

### ✅ Phase 3 临床研究知识扩展完成 — 知识库扩充至 3738 条

**新增内容批次**：

| 批次 | 条目 | 核心内容 |
|------|------|---------|
| `literature_batch_immunotherapy.json` | +51条 | MSI-H/dMMR免疫治疗（KEYNOTE-177、CheckMate-142）；MSS联合策略（REGONIVO、AtezoTRIBE、LEAP-005）；新辅助ICI（NICHE-2、VOLRAF）；irAEs分级管理；双特异性抗体（Cadonilimab、ADG126）；ctDNA指导ICI；微生物组/TLS生物标志物 |
| `literature_batch_supportive_care.json` | +32条 | WHO癌痛五阶梯；CINV三联止吐方案；G-CSF一级/二级预防；ESPEN营养指南；LARS康复；造口旁疝管理；缓和医疗早期引入；老年综合评估（CGA） |
| `literature_batch_cms_cris_molecular_subtypes.json` | +46条 | CMS1-4分型定义/发生率/预后；CRIS分型；MSI-H/dMMR；HER2/NTRK扩增；TMB；肿瘤出芽；脉管侵犯 |
| `literature_batch_ctDNA_MRD_TNT.json` | +33条 | ctDNA/MRD检测定义/临床时机；DYNAMIC研究；TNT策略Meta分析；cCR与观察等待；RAPIDO/STELLAR研究 |
| `literature_batch_hereditary_epidemiology.json` | +37条 | 林奇综合征（Amsterdam/Bethesda标准）；FAP（APC基因）；MAP；CMMRD；年轻发病CRC |
| `literature_batch_epidemiology_screening.json` | +24条 | GLOBOCAN 2022流行病学；FIT/Cologuard筛查；结肠镜质量指标（ADR/CIR）；IBD-CRC监测 |

**知识库规模**：
- 📊 **总三元组**: 3,738条（较2026-05-06增加83%）
- 🏷️ **Domain分类**: 27类
- 📋 **证据等级I级**: 557条
- 📚 **源文件数**: 18个批次文件

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
- ✅ **可追溯**：每条知识均标注原始来源（PMID/指南版本）
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
├── data/                           # 核心数据
│   ├── kb.json                     # 构建后的完整知识库（3738条）
│   ├── kb_meta.json                # 知识库元数据与统计
│   ├── guidelines/                 # 指南共识摘要
│   │   └── csco/                   # CSCO指南年度更新点
│   └── knowledge-graph/            # 知识图谱源文件（批次JSON）
├── scripts/                        # 数据处理脚本
│   ├── build_kb.py                # 知识库构建脚本
│   ├── tests/
│   │   └── test_kb_format.py      # 格式验证工具
│   ├── expand_from_literature.py   # 文献扩展脚本
│   ├── parse_ascrs_guidelines.py   # ASCRS指南解析
│   └── export_to_obsidian.py      # Obsidian格式导出
├── schemas/                        # 数据模式定义（JSON Schema）
├── docs/                          # 文档
└── obsidian-export/              # Obsidian格式导出
```

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/lockwang127/colorectal-cancer-kb.git
cd colorectal-cancer-kb
```

### 2. 加载知识库

```python
import json

with open('data/kb.json', 'r') as f:
    kb = json.load(f)

print(f"知识条目总数：{len(kb)}")
print(f"Domain分类：{len(set(item['domain'] for item in kb))} 类")
print(f"I级证据条目：{sum(1 for item in kb if item.get('evidence','').startswith('I级'))} 条")
```

### 3. 知识检索示例

```python
# 搜索关键词
results = [item for item in kb if 'MSI-H' in item.get('head','') or 'MSI-H' in str(item)]
print(f"MSI-H相关条目: {len(results)}")

# 按Domain筛选
immuno_kb = [item for item in kb if '免疫治疗' in item.get('domain','')]
print(f"免疫治疗条目: {len(immuno_kb)}")
```

### 4. 运行数据校验

```bash
python scripts/tests/test_kb_format.py
python scripts/build_kb.py   # 重新构建知识库
```

---

## 📊 数据质量

| 数据类型 | 当前条目 | 质量等级 |
|----------|----------|----------|
| **知识三元组（kb.json）** | **3,738** | 高 |
| 指南摘要 | 3 (CSCO/NCCN/ESMO) | 高 |
| 药物知识 | 20+ (含靶向/免疫) | 高 |
| 临床试验 | 100+ | 中高 |

### 知识域分布（Top 10）

| Domain | 条目数 | 占比 |
|--------|--------|------|
| 系统治疗 | 923 | 24.7% |
| 肛管癌 | 910 | 24.3% |
| 造口·随访·筛查 | 659 | 17.6% |
| 外科手术 | 296 | 7.9% |
| 阑尾肿瘤 | 181 | 4.8% |
| 临床治疗 | 152 | 4.1% |
| 围手术期管理 | 124 | 3.3% |
| 临床治疗-免疫治疗 | 53 | 1.4% |
| 基因靶点 | 56 | 1.5% |
| 其他（22个分类） | 384 | 10.3% |

### 证据等级分布

| 证据等级 | 条目数 | 说明 |
|----------|--------|------|
| I级 | 557 | RCT/大规模研究 |
| II级 | 133 | 队列研究/病例对照 |
| I级专家共识 | 2,864 | ASCRS/CSCO指南共识 |
| 专家共识 | 95 | 专家意见 |

---

## 🛠️ 技术栈

- **数据格式**：JSON（结构化三元组）+ Markdown（人类可读）
- **校验**：Python脚本 + JSON Schema
- **知识图谱**：JSON（可直接导入Neo4j/图数据库）
- **Obsidian兼容**：Markdown格式可直接导入Obsidian

---

## 📧 联系我们

- **项目负责人**：汪晓东（四川大学华西医院胃肠外科）
- **Email**：[请联系通过GitHub Issue](https://github.com/lockwang127/colorectal-cancer-kb/issues)
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

[![Star History Chart](https://api.star-history.com/svg?repos=lockwang127/colorectal-cancer-kb&type=Date)](https://star-history.com/#lockwang127/colorectal-cancer-kb&Date)

---

**Disclaimer**：本知识库仅供医学专业人士参考，不构成临床诊疗建议。临床决策请务必结合患者具体情况和最新指南。
