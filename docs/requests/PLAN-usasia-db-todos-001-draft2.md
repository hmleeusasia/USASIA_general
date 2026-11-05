# PLAN usasia-db-todos-001 draft2 — todos table and pages in usasia_db
Status: draft2 (2026-11-05), approved by the user → D-20261105-1. draft1 reviewed by a fresh Sonnet (objections accepted except the is_private rename). Owner: hmlee (requirements) + Claude (code). Follows D-20261104-5. App repo: C:\USASIA Claude\usasia_db.

## Table `todos`
| Column | Type | todo.md source | Notes |
|---|---|---|---|
| code | string, unique, not null | ID | `^[TM]-[A-Za-z0-9-]+$`; editable. Combined IDs ("T-295+T-285") are split into rows |
| previous_code | string | — | old M- ID after a ticket gets its T- number; search finds both |
| parent_code | string | sub-task notes | parent row's code (T-640 → T-619) |
| title | string, not null | 할 일 | |
| store | string | 매장 | |
| tags | string | 분야 | `#pos #network` |
| status | enum, not null, default todo | 상태 | todo / doing / waiting / done / cancelled (대기·보류 → waiting) |
| waiting_on | string | 기다림(대상) | |
| next_step | text | 다음 | |
| due_on | date | due | only when the request has one |
| planned_for | date | section 1 "Now" | planned visit / work day |
| moved_on | date, not null | 움직임 | default today (Pacific) on create; editable (import keeps dates) |
| assignee | string | section 3a owner | person name, blank = owner |
| owner_email | string | — | signed-in account (login identity, not a contact) |
| is_private | boolean, default false | — | D-20261104-5: original lives in Drive; row holds a summary only |
| timestamps | | | |
Indexes: unique code; [status, due_on]; parent_code; planned_for. ⏸ = moved_on older than 30 days, computed in the view.

## Sensitive-value guard (R-SEC-02..05)
title, next_step, waiting_on, assignee, store, tags refuse: email addresses, phone-like numbers (10+ digits with separators), key-like strings (long base64/hex, "password", "api_key", "secret" followed by a value). Error message tells the user to keep the value in Drive. Names are allowed.

## Pages (behind Google login)
- /todos index: filters status, store; default hides done/cancelled; sort planned_for, due_on (nulls last), moved_on. Shows ⏸ and parent code.
- new / edit: one form, with a note "no emails, phones, passwords — keep those in Drive".
- No destroy route. Root → todos index; home page link kept.

## Build, test, deploy
- config.time_zone = "Pacific Time (US & Canada)".
- No Ruby on the PC: migration + db/schema.rb written by hand; tests run in GitHub CI (ci.yml `test` job).
- deploy.yml triggers on workflow_run of CI (success, main) + manual; no deploy when tests fail.
- Tests: model (validations, code format, guard, defaults, stale), controller (login required, non-allowed email refused, index filter/sort, create/update, no destroy route).
- After deploy: add a few real rows, repeat the backup restore test.

## Out of scope
Import of todo.md rows (next step), API/token, todo-sync switch, per-user visibility, sections 3/4 narrative notes (stay in todo.md until import design).
