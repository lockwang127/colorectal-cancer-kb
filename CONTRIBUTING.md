# Contributing

Thank you for considering a contribution to the colorectal cancer knowledge base.

This repository only accepts contributions related to **colorectal cancer**. Other cancer domains and historical test materials are out of scope for this project.

## Accepted Contributions

### Medical knowledge

- guideline summaries
- structured knowledge triplets
- source and evidence-level corrections
- literature batch additions
- colorectal cancer surgery, systemic therapy, staging, follow-up, screening, LARS, molecular markers and survivorship knowledge

### Knowledge engineering

- schema improvements
- validation scripts
- deduplication and quality checks
- export utilities for RAG, JSONL, Markdown or vector database input

### Agent and RAG use

- standard evaluation questions
- retrieval examples
- prompt/context templates
- Agent Skill or workflow examples

## Out of Scope

Please do not submit:

- unrelated cancer knowledge bases
- patient-facing online consultation features
- identifiable patient records
- copied guideline or paper full text
- commercial medical service content
- materials without source attribution

## Data Requirements

Each structured knowledge entry should include:

- subject / head
- relation
- object / tail
- domain
- source
- evidence level
- confidence
- applicable conditions if needed

The source must be traceable to a guideline, consensus, paper, dataset or clearly identified professional note.

## Copyright Requirements

- Do not copy long passages from guidelines, papers or books.
- Use original summaries, structured extraction and interpretation.
- Keep source references clear.
- Mark uncertainty and evidence boundaries.

## Before Submitting

Run validation when possible:

```bash
python3 scripts/validate_data.py
```

Check:

- the contribution is colorectal-cancer related
- fields are complete
- sources are included
- evidence levels are clear
- no protected full text is included
- documentation is updated if needed

## Issues

Use GitHub Issues for:

- data errors
- missing sources
- schema suggestions
- RAG retrieval problems
- standard question proposals

Repository:

```text
https://github.com/lockwang127/colorectal-cancer-kb
```

## Review Principle

This project values reliability over volume. A small number of well-sourced entries is preferred to a large batch with weak attribution.
