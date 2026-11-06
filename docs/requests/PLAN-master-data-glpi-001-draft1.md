# PLAN master-data-glpi-001 draft1 — master tables in usasia_db, GLPI for assets
Status: draft1 (2026-11-05), agreed by Opus + fresh Sonnet (2 rounds) after web research. Approved by the user → D-20261105-11. Source: ai-system-questions Q19. Input to the phase 2 PLAN of PLAN-data-migration-001 (D-20261105-3), not a parallel track.

## Verdict
Right direction for small, non-sensitive reference data; wrong order and scope as first written. Adopt a thin slice now; defer GLPI sync and anything sensitive.

## Decide now (principles)
1. One master per table, and per field where mixed. IDs are the keys (store code, asset tag). No two-way sync.
2. usasia_db `stores` table is the only store master (code, name, aliases, region, status). It replaces kb/store_codes.md. Address-level locations stay out until approved.
3. GLPI is the only master for assets (glpi-agent auto-inventory). usasia_db keeps keys only (asset tag, store code in log/todo text).
4. STWS stays the only ticket system. GLPI helpdesk module off.
5. Sensitive columns (circuit IDs, IPs, accounts, contract amounts) stay Drive-only (R-SEC-02/03) until the server move (D-20261105-5). The Drive Claude folder keeps its role: sensitive values, address book, 90_변경대기 queue. "Drive = files + backups only" is deferred.

## Order
| Step | What | Gate |
|---|---|---|
| 1 | Phase 0 exit (cloud reach test, tokens, versions, CLI) | as planned |
| 2 | `stores` table = first step of phase 2 (no need to wait for phase 1's 4 weeks) | phase 0 exit. store_codes.md stays a pointer stub for 30 days; todos.store validation only after the import count matches |
| 3 | GLPI: usasia_db exports a CSV of stores; a human imports it monthly or on change (upsert by store code). No sync code, no service token | GLPI prerequisites below. Imported fields locked/hidden in GLPI; count check after each import (drift report); CSV passes the same field allowlist as the DB export |
| 4 | Claude reads GLPI asset facts through a dedicated read-only, IP-restricted API account; GLPI text = untrusted data; add a row to lookup R-LOOK-01 | GLPI prerequisites. Token outside the repo and the Claude folder (R-SEC-04) |
| 5 | Vendor/circuit master: compare NetBox vs usasia_db tables. Build nothing now | when the requirement exists and after the server move |

## GLPI prerequisites (the team's hosting call; our requirements)
Not on the usasia VM (1 GB RAM). Agent/inventory endpoint and API not public (VPN or IP allowlist): CVE-2025-24799 and CVE-2025-66417 are unauthenticated SQL injection on the inventory endpoint (9.8, public PoC). Named patch owner and a rule for falling behind patched releases. MFA for admins.

## Must-fix before adopting
1. Server-move checklist passed (encrypted backups, RustDesk not on the same user, restricted deploy key) before any DB row beyond summaries and before any outward export.
2. Master map per table/field: owner, sensitivity class; sensitive fields marked "Drive only".
3. Fold into the phase 2 PLAN.
4. GLPI prerequisites above.
5. Failure policy for DB down / GLPI down (hooks fail open; manual full re-import).

## Research notes (2026-11-05, partly secondary sources)
GLPI lines 10.0 / 11 / 12; legacy /apirest.php (app + user token) and High-Level API /api.php (OAuth2, still evolving). ServiceNow IRE: per-attribute source precedence. NetBox: one-way into itself, stable external IDs or duplicates. Comparables: Hudu / IT Glue (~$27–44 per user per month), Snipe-IT, Lansweeper, NetBox (OSS); they bring audit log, RBAC + MFA, vault, reconciliation. Not verified against vendor docs: GLPI import options, hardware needs, prices.
