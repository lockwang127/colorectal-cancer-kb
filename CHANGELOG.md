# CHANGELOG - 结直肠癌通用知识库

## [v1.3.1] - 2026-05-08

### 知识库更新规范确立 + GitHub 同步自动化

**新增文件：**

- `UPDATE_POLICY.md` — 确立前瞻性增量更新原则（只更新新文献，不回头补旧）
- `scripts/sync_to_github.py` — 一键同步构建产物到 GitHub（含 auto-commit + push）

**更新规范要点：**

- 批次命名：`literature_batch_YYYYMMDD.json`（日期格式）
- 已入库内容永久冻结，不再修改源批次文件
- 版本语义化递增（patch/minor/major）
- 每次构建自动 push 到 GitHub

---

## [v1.3.0] - 2026-05-07

### 临床研究知识扩展完成

**知识库规模**：3,738条三元组（+83%）

#### 新增内容批次

| 文件 | 条目 | 内容 |
|------|------|------|
| `literature_batch_immunotherapy.json` | +51 | MSI-H/dMMR免疫治疗（KEYNOTE-177、CheckMate-142、NICHE-2）；MSS联合策略（REGONIVO、AtezoTRIBE、LEAP-005）；irAEs分级管理；双特异性抗体（Cadonilimab、ADG126）；ctDNA指导ICI |
| `literature_batch_supportive_care.json` | +32 | WHO癌痛五阶梯；CINV三联止吐；G-CSF预防；ESPEN营养指南；LARS康复；造口护理；缓和医疗；老年CGA评估 |
| `literature_batch_cms_cris_molecular_subtypes.json` | +46 | CMS1-4分子分型；CRIS分型；MSI-H/dMMR；HER2/NTRK扩增；TMB；肿瘤出芽；脉管侵犯 |
| `literature_batch_ctDNA_MRD_TNT.json` | +33 | ctDNA/MRD检测；DYNAMIC研究；TNT策略Meta分析；cCR与观察等待 |
| `literature_batch_hereditary_epidemiology.json` | +37 | 林奇综合征；FAP（APC基因）；MAP；CMMRD；年轻发病CRC |
| `literature_batch_epidemiology_screening.json` | +24 | GLOBOCAN 2022流行病学；FIT/Cologuard筛查；结肠镜质量指标；IBD-CRC监测 |

#### 新增文件

- `data/kb.json` — 构建后的完整知识库（3,738条）
- `data/kb_meta.json` — 知识库元数据与统计
- `scripts/build_kb.py` — 知识库构建脚本（含自动domain推断）
- `scripts/tests/test_kb_format.py` — 格式验证工具

#### 知识域扩展

- Domain分类：11类 → **27类**
- 临床治疗-免疫治疗：2条 → **53条**
- 临床治疗-支持治疗：0条 → **32条**
- 证据I级：369条 → **557条**

---

## [v1.2.0] - 2026-05-06

### Phase 2 基础研究知识补充

- 新增基础研究批次（KRAS-KHMI机制轴、MAPK/PI3K通路、肿瘤微环境等）
- `literature_batch_20260506.json`（70条）
- `literature_batch_basic_research.json`（64条）

---

## [v1.1.0] - 2026-05-07

### 知识库结构修复

- 修复`build_kb.py`硬编码路径，改为相对路径+环境变量支持
- 253条未分类条目补充domain标签
- 新增`kb_meta.json`版本追踪文件
- 新增格式验证脚本

---

## [v1.0.0] - 2026-05-06

### 初始版本

- 知识库规模：3,515条三元组
- 主要来源：ASCRS指南、CSCO 2024、DACCA数据库
