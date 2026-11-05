# Rules index
Read this at the task announcement (CLAUDE.md Session 2), then read only the area files the task needs. Pass their paths in every subagent brief. Plan: docs/requests/PLAN-rule-routing-001-draft2.md (D-20261104-2).

| Area | File | Scope | Trigger words | Trigger paths | IDs |
|---|---|---|---|---|---|
| security | security.md | What may be stored where; sensitive values; what to do on finding one | password, email, phone, account, circuit, IP, 비밀번호, 계정 | any repo write | R-SEC-01..05 |
| log | log.md | Daily work log files and entries, hubs, dates, tips | log, 기록, 로그, tip, 팁 | docs/log/**, docs/{vendors,stores,assets,projects}/** | R-LOG-01..08 |
| expense | expense.md | Receipts and mileage into Notion + Sheet | 출발, 도착, depart, arrive, receipt, 영수증, mileage, 경비 | (connectors only) | R-EXP-01..07 |

Rules: one `## R-<AREA>-NN` heading per rule; IDs are never reused; each file ≤ 3,000 chars; personal values (mailboxes, URLs, STWS numbers) stay in docs/users/<id>/profile.md. Not yet moved: rules still inside skills and kb files (moved when those files are edited, by 2026-12-31).
