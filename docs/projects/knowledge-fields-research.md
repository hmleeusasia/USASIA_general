# Knowledge fields per project type — research (Q21/Q22 brainstorm)

Status: brainstorm only (user 2026-11-07: "반영은 나중에"). Source: general knowledge of the systems below, no web check yet. Asset/ticket data stays in GLPI (or the chosen asset system); this note covers **knowledge** fields that link to it.

## 1. Systems looked at

| System | Kind | Idea to borrow |
|---|---|---|
| KCS v6 (Consortium for Service Innovation) | Knowledge method | Article = **Issue / Environment / Resolution / Cause**; states Work in progress → Not validated → Validated → Archived; reuse count; "capture in the workflow, improve on reuse" |
| ITIL Known Error DB | Problem mgmt | Known error: symptom, root cause, **workaround**, permanent fix status, linked incidents |
| GLPI Knowledge base | ITSM + assets | KB item: subject, content, category, **target (who may see)**, linked to tickets/assets, FAQ flag, visibility dates, revisions |
| ServiceNow KB | ITSM | Article type, valid-to date (review), ownership group, CI link, helpful votes, flagged-as-wrong |
| IT Glue / Hudu (MSP docs) | IT documentation | **Per location** docs; "flexible assets" (custom typed templates: Internet/WAN, LAN, Printing, Backup, Vendor, Application); relations between items; password vault kept separate |
| NetBox | Infra source of truth (DCIM/IPAM) | Sites, devices, circuits (provider, circuit ID, termination), **journal entries** per object (dated notes), tags, custom fields |
| Snipe-IT | Asset mgmt | Asset → model → location, check-in/out history, maintenance records, warranty/EOL dates |
| Confluence templates | Wiki | How-to, **Troubleshooting article**, Runbook, Decision log, Retrospective, Meeting notes |
| Google SRE (runbook/postmortem) | Ops | Runbook: alert, impact, diagnosis steps, mitigation, escalation; postmortem: timeline, root cause, action items with owners |
| Diátaxis | Doc structure | Four doc kinds: tutorial, **how-to**, **reference**, **explanation** — don't mix them in one page |
| PCI DSS / audit practice | Compliance | Requirement ID, control owner, frequency, **evidence location**, last done, next due |
| ADR (MADR) | Dev | Decision, options, consequences, status, superseded-by |

## 2. Common fields (every knowledge record, all 5 types)

| Field | From | Note |
|---|---|---|
| id, title, type (how-to / troubleshooting / runbook / reference / decision / lesson / risk) | Diátaxis, Confluence | One kind per record |
| project, project_type, tags | ours (Q21) | `#proj-*` |
| scope: stores / sites, assets (GLPI ID), vendor | IT Glue, GLPI | **link by ID, never copy** asset data |
| environment (model, OS/firmware version, circuit type) | KCS | Answers "does this apply to me?" |
| state: draft → validated → archived | KCS | Validated = worked at least once in the field |
| owner, last_verified, review_by | ServiceNow | Stale knowledge is the main failure |
| reuse_count / last_used | KCS | Shows what matters; surfaces at session-end |
| sources: log entry, ticket (STWS/GLPI), Drive link, commit | ours | Originals stay in Drive (R-SEC-01) |
| sensitivity flag | ours | Points to Drive Claude folder; never the value |

## 3. Extra fields by type

| Type | Record kinds | Extra fields |
|---|---|---|
| Infrastructure | runbook, troubleshooting, change, site profile | site, circuit (provider, type, GLPI/NetBox ID), dependencies (upstream/downstream), impact if down, escalation path (vendor support level), maintenance window, rollback steps, monitoring check name |
| Store systems & devices | how-to, troubleshooting, known error, model profile | device model, firmware/app version, stores affected, workaround, permanent fix, vendor RMA path, spare-part note, EOL/warranty (from asset system) |
| Development | ADR, lesson, risk, component note | repo, component/function, commit, change why, dependency (generated), test added, superseded-by (see dev-knowledge-research.md) |
| Security & compliance | control, procedure, incident, exception | requirement ID (e.g. PCI DSS x.y), frequency, last done / next due, evidence location (Drive), control owner, exception approved by + expiry |
| Operations & admin | procedure, vendor profile, decision, checklist | vendor (orgs.md), contract/renewal date (amounts in Drive), approval chain, who to ask, recurring date, template link |

## 4. Ideas worth adopting first
1. **KCS states + last_verified** — cheap, fixes stale tips (pos_tips.md has no state today).
2. **Troubleshooting template = Issue / Environment / Cause / Resolution / Workaround** — fits our existing "symptom → cause → fix" log rule.
3. **Per-store page that only links** (IT Glue location view): store hub lists runbooks, known errors, circuits, assets by ID.
4. **Journal entries per object** (NetBox): dated notes on a store/asset/circuit = our log tags, already close.
5. **Compliance calendar** (next_due) feeding start-day.
6. **Generated reuse report** at weekly review: most-used, never-used, overdue review.

## 5. Questions for later
- Asset system: GLPI confirmed? Will it also hold the KB, or only assets/tickets? (GLPI KB vs usasia_db)
- Who validates a record (KCS "validated")?
- Same fields in Markdown front matter first, DB later?
