# Colorectal Cancer Knowledge Base

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/Knowledge-CC%20BY--NC--SA%204.0-orange.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![GitHub stars](https://img.shields.io/github/stars/lockwang127/colorectal-cancer-kb.svg)](https://github.com/lockwang127/colorectal-cancer-kb)
[![Last Commit](https://img.shields.io/github/last-commit/lockwang127/colorectal-cancer-kb.svg)](https://github.com/lockwang127/colorectal-cancer-kb/commits)
[![Knowledge Triplets](https://img.shields.io/badge/Knowledge-3%2C738%20Triplets-green.svg)](data/knowledge-graph/relations.json)

结直肠癌结构化医学知识库，面向医学研究、知识工程、RAG 原型和 Agent 工作流开发。

本仓库只维护 **colorectal cancer / 结直肠癌** 相关内容。其它癌种或历史测试内容不属于本仓库主线，也不作为 lock2.wang 的内容来源。

## Project Status

| Item | Current |
|------|--------:|
| Version | `v1.0.0` |
| Updated | `2026-05-07` |
| Structured triplets | `3,738` |
| Knowledge domains | `27` |
| Source batches | `18` |

Public resource entry:

- Website: [https://lock2.wang](https://lock2.wang)
- Downloads: [https://lock2.wang/downloads/](https://lock2.wang/downloads/)

## What This Repository Provides

- Structured colorectal cancer knowledge triplets
- Guideline and literature-derived evidence snippets
- JSON data for downstream retrieval and analysis
- Schema and validation scripts
- Source material organization for RAG and Agent prototypes

It is designed to support:

- evidence retrieval
- local knowledge search
- RAG context construction
- knowledge quality review
- Agent Skill and workflow prototyping

## Boundaries

This repository does **not** provide:

- patient-facing online consultation
- individualized diagnosis or treatment advice
- medical record processing
- commercial medical service
- unrestricted copying of guideline or paper full text

All clinical use requires professional review and reference to the latest original guidelines and literature.

## Repository Structure

```text
colorectal-cancer-kb/
├── data/
│   ├── guidelines/               # guideline notes and summaries
│   └── knowledge-graph/          # structured triplet batches
├── schemas/                      # schema documentation
├── scripts/                      # validation and processing scripts
├── docs/                         # project and design docs
├── obsidian-export/              # Obsidian-oriented export
└── web/                          # historical web prototype
```

## Knowledge Domains

Top domains in the current release:

| Domain | Entries |
|--------|--------:|
| 系统治疗 | 923 |
| 肛管癌 | 910 |
| 造口·随访·筛查 | 659 |
| 外科手术 | 296 |
| 阑尾肿瘤 | 181 |
| 临床治疗 | 152 |
| 围手术期管理 | 124 |
| 基因靶点 | 56 |
| 临床治疗-免疫治疗 | 53 |
| 病理·营养·预后 | 41 |

## Main Sources

The knowledge base is built from structured summaries and extracted knowledge based on sources such as:

- ASCRS clinical practice guidelines
- CSCO 2024 colorectal cancer guideline
- NCCN colon / rectal / anal cancer guideline materials
- ESMO-related evidence summaries
- AJCC staging references
- selected literature batches on immunotherapy, ctDNA/MRD/TNT, CMS/CRIS, supportive care, LARS and survivorship

The repository stores structured summaries and knowledge extraction results, not full copies of copyrighted source documents.

## Quick Start

Clone the repository:

```bash
git clone https://github.com/lockwang127/colorectal-cancer-kb.git
cd colorectal-cancer-kb
```

Run validation:

```bash
python3 scripts/validate_data.py
```

Inspect source batches:

```bash
ls data/knowledge-graph/
```

For a ready-to-run local query module, use the lock2.wang download package:

```text
https://lock2.wang/downloads/colorectal-cancer-kb-cli.zip
```

The CLI package includes `kb.py`, `validator.py`, `exporter.py`, `stats.py`, `examples/` and `docs/`.

## Relationship With lock2.wang

This GitHub repository is the public source and version history for the colorectal cancer knowledge base.

lock2.wang provides:

- public-facing resource explanation
- direct download packages for users who cannot access GitHub reliably
- Python query module package
- Agent Skill package
- workflow and evaluation examples

Recommended flow:

1. Update structured knowledge in this repository.
2. Validate data and update metadata.
3. Build release packages locally.
4. Publish downloads through lock2.wang.
5. Keep GitHub as the source history and collaboration surface.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

Preferred contributions:

- colorectal cancer guideline summaries
- structured triplets with source and evidence level
- data validation improvements
- RAG evaluation questions
- documentation for knowledge engineering and Agent use

Please do not submit unrelated cancer domains to this repository.

## License

Medical knowledge content:

- CC BY-NC-SA 4.0

Code, scripts and schema helpers:

- MIT-style use unless otherwise specified in individual files.

## Disclaimer

This repository is for medical knowledge engineering, research, education and AI prototype development. It is not a clinical decision system and does not replace professional medical judgment.
