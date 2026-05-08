# 知识库更新规范

> 本文件定义了结直肠癌通用知识库（Colorectal Cancer Knowledge Base）的版本更新机制，确保知识库持续迭代、来源可追溯、GitHub 同步自动化。

---

## 一、更新原则

### 1. 前瞻性增量更新（唯一来源）

- **每次更新只添加新批次，不修改已入库的旧批次文件**
- 新批次命名格式：`literature_batch_YYYYMMDD.json`（日期为添加当日）
- 如果是专题扩展，使用有意义的英文主题后缀：`literature_batch_YYYYMMDD_[topic].json`

### 2. 已入库内容永久冻结

- 一旦三元组通过 build 脚本合并入 `kb.json`，对应的源批次文件**不再修改**
- 如需修正错误，新增一条正确的三元组，旧的不删除（避免版本混乱）

### 3. 版本号语义化递增

| 触发条件 | 版本号递增 |
|----------|-----------|
| 新增 ≥50 条三元组 | patch: x.x.**Z**+1 |
| 新增新 Domain 分类 | minor: x.**Y**.0 |
| 架构重构/字段变更 | major: **X**.0.0 |

---

## 二、更新流程

```
1. 新文献/指南整理 → 写入新批次 JSON（命名: literature_batch_YYYYMMDD.json）
2. python scripts/build_kb.py   ← 自动合并去重 + 更新 kb.json + kb_meta.json
3. GitHub 同步（自动）           ← 本地 push 到 origin main（见下方自动化）
4. 更新 CHANGELOG.md             ← 记录本次新增条目数、内容摘要
```

---

## 三、GitHub 自动同步机制

每次运行 `build_kb.py` 后，触发 GitHub 同步脚本 `scripts/sync_to_github.py`：

```bash
# 自动执行（推荐）
python scripts/build_kb.py && python scripts/sync_to_github.py

# 或手动触发
python scripts/sync_to_github.py
```

**同步内容：**

| 文件 | 说明 |
|------|------|
| `data/kb.json` | 合并后的完整知识库 |
| `data/kb_meta.json` | 元数据（版本/统计） |
| `data/knowledge-graph/*.json` | 所有源批次文件（含新批次） |
| `CHANGELOG.md` | 版本更新记录 |

**提交信息格式：**

```
feat: 新增 N 条三元组 (YYYY-MM-DD)

- [批次] 新增条目数
- [批次] 内容摘要
```

---

## 四、来源追踪

每条三元组的 `source` 字段标注原始出处：

| 类型 | source 示例 |
|------|-------------|
| 指南共识 | `CSCO CRC 2024` / `NCCN Colon 2024` |
| 临床试验 | `KEYNOTE-177 (NCT02563002)` |
| 期刊文献 | `Lancet Oncol 2024` |
| 数据库 | `DACCA 2025` |

---

## 五、知识域分类（27 类）

更新时优先映射到已有 Domain，必要时新增：

| Domain | 说明 |
|--------|------|
| 基因突变与分子机制 | KRAS/BRAF/MSI 等基因层面 |
| 肿瘤微环境 | 免疫细胞、PD-1/PD-L1 等 |
| 临床诊断 | 分期、病理、筛查 |
| 临床治疗 | 化疗/靶向/手术 |
| 随访与预后 | LARS、生活质量 |
| 肛管癌 | 肛管鳞癌专项 |
| 阑尾肿瘤 | 阑尾癌/黏液肿瘤 |
| 围手术期管理 | ERAS、营养 |
| 支持治疗 | 疼痛、CINV、营养 |
| 免疫治疗 | 免疫检查点抑制剂 |
| ... | ... |

---

## 六、审校要求

| 条目数 | 审校要求 |
|--------|---------|
| <10 条 | 自审即可 |
| 10-50 条 | 至少一名同行确认 |
| >50 条 | 正式 peer review 后入库 |

> 学术严谨性优先，宁缺毋滥。

---

## 七、GitHub Issues 协作

- 发现错误/缺漏 → GitHub Issue（附 PMID/来源）
- 新增建议 → GitHub Discussion
- 合并新批次 → Pull Request（review 后合入）

---

*本规范自 2026-05-08 起执行。*
