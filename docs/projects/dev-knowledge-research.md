# Dev knowledge record — research (Q22, with Q21)

Goal: per dev project, keep what each function/module does, what changed and why, problems hit, dependencies, and expected risks, so a new developer (or Claude) can pick it up. Status: research only, no design decision yet (2026-11-07).

## 1. Existing systems and what to borrow

| System | What it records | Storage | Borrow |
|---|---|---|---|
| ADR (Nygard; MADR template) | One decision per file: context, options, decision, consequences, status (proposed/accepted/superseded) | `docs/adr/NNNN-title.md` in the code repo | "Why we changed it" + superseded-by links. Close to our decisions.md, but per project |
| Conventional Commits + git trailers | Change type (feat/fix/refactor), scope, breaking change; trailers like `Refs:`, `Fixes:` | Commit messages | Machine-readable "what changed"; trailer `Lesson: L-007`, `ADR: 0003` to link commits to records |
| Keep a Changelog | Added/Changed/Fixed/Removed per release | `CHANGELOG.md` | Human summary of changes; can be generated from commits |
| Docstrings + generated docs (pydoc, Sphinx, mkdocstrings) | Function purpose, args, returns, raises | In code | Function meaning lives next to the code (never drifts far); index generated, not hand-written |
| ctags / Sourcegraph SCIP / LSP index | Symbols, definitions, references (who calls whom) | Generated index | Dependencies between functions should be **generated** (Python `ast`), not hand-kept |
| SBOM (CycloneDX, SPDX), lockfiles, pip-tools | External package dependencies + versions | `requirements*.txt`, lock, SBOM json | External deps from lockfile; record only *why* a package was chosen/pinned |
| Google SRE postmortem | Incident: impact, timeline, root cause, trigger, fix, action items, lessons | Doc per incident | Template for "problems" (symptom → cause → fix → prevention → action items) |
| Known-issues / KEDB (ITIL problem management) | Known error, workaround, permanent fix status | Database | "Risk / known issue" with open/closed state |
| Risk register (PM) | Risk, likelihood, impact, mitigation, owner, status | Table | risks.md columns |
| arc42 / C4 model | Architecture views: context, containers, components; cross-cutting concepts | Docs + diagrams | Module-level map in README (we already have ARCHITECTURE.md style) |
| Backstage software catalog | Component, owner, system, dependsOn, API (catalog-info.yaml) | YAML per repo | Small per-repo metadata file: owner, status, depends-on other repos |
| Fossil SCM | Code + tickets + wiki + tech notes in one SQLite file | SQLite | Proof that "records in a DB next to code" works; our usasia_db could hold the index |
| Jira / Linear / GitHub Issues | Work items, links (blocks, relates), labels | Hosted DB | Link types (blocks / caused-by / fixed-by) for problem ↔ change ↔ function |
| Architecture knowledge mgmt (Kruchten; "design rationale" research) | Rationale decays fastest; capture at decision time | — | Capture in the same commit/session, not later |

## 2. Takeaways
1. **Generate what code already knows** (symbols, call graph, imports, package versions); hand-write only meaning and *why*. Hand-kept dependency lists go stale.
2. **Records live in the code repo**, linked by ID from commits; this repo holds only an index (fits R-SEC-01, Q21).
3. Four hand-written record types cover the request: **Decision/Change (ADR)**, **Lesson (problem)**, **Risk/Known issue**, **Component note** (function/module meaning beyond the docstring).
4. Capture at the moment (commit trailer + session-end draft), review weekly.

## 3. Candidate data model (for discussion)

| Table | Key fields |
|---|---|
| component | id, path/symbol, kind (module/function/class), purpose, owner, status, generated_at |
| dependency | from_component, to_component or package, kind (calls/imports/package/service), source (generated/manual) |
| change | id, commit, date, component(s), type, what, why, adr_id |
| decision (ADR) | id, title, context, options, decision, consequences, status, superseded_by |
| lesson | id, date, component(s), symptom, cause, fix, prevention, commit, tags |
| risk | id, component(s), description, likelihood, impact, mitigation, status, opened/closed |
| link | from_id, to_id, kind (caused-by, fixed-by, supersedes, relates) |

Two storage options: (A) Markdown files in the dev repo (`docs/dev/adr/`, `lessons.md`, `risks.md`) + a generated `components.md`; (B) the same tables in usasia_db with Markdown export. A first, B later, is the low-risk path.

## 4. Open questions for the user
- Which dev repos are in scope (usasia_db only for now)?
- Will developers read this repo, or only their code repo?
- Language of dev records (repo text rule is English, D-20261103-5)?
- Generated index: run on commit (hook/CI) or at session-end?
