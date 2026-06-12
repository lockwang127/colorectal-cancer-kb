# lock2.wang Web Interface Direction

This document replaces an early public Q&A prototype note. The current website direction is a resource platform for colorectal cancer knowledge engineering, RAG prototypes and Agent workflows, not a patient-facing medical chatbot or registration-based consultation product.

## Current Public Site Role

lock2.wang should make the repository easier to understand and use:

- explain what the colorectal cancer knowledge base contains
- show representative question types and evaluation tasks
- provide direct download packages for users who cannot access GitHub reliably
- describe Python module, Agent Skill and workflow use cases
- point contributors back to the GitHub repository for versioned source history

## Recommended First-Screen Modules

The homepage should keep four resource blocks at the same visual level:

| Module | Purpose |
|--------|---------|
| Colorectal cancer knowledge base | Structured triplets and source batches |
| Vector database | Retrieval layer prepared for RAG experiments |
| Agent Skill library | Reusable skill packages for Codex or similar agents |
| Agents library | Curator, retrieval, evaluation and release workflows |

## Access Model

The default public access model is download-first:

- no forced account registration for static resources
- GitHub for source history and issues
- lock2.wang downloads for packaged releases
- optional future registration only if there is a clear need for private dashboards, usage analytics or restricted collaboration

## Boundaries

The site should avoid:

- patient-facing diagnosis or treatment promises
- online consultation positioning
- claims based on personal authority
- unrelated cancer domains
- copyrighted guideline or paper full-text redistribution

## Current Implementation Location

The actively maintained lock2.wang implementation lives outside this historical `web/` prototype and is built in the local project folder:

```text
prof.wang/v3-site
```

The historical `web/` folder can remain as an archived prototype, but it should not be treated as the current public product direction.
