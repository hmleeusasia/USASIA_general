# Security and storage rules
Source: D-20261102-16, former docs/storage_rules.md. Enforced in part by hooks sens-email, sens-secret (tools/hooks/guard.py) and git pre-commit.

## R-SEC-01
GitHub holds secondary docs only: index, summaries, keywords, links, decision summaries, dates, tips. Originals and refined data live in the company Google Drive. When unsure, send it to Drive.

## R-SEC-02
Never in the repo (Drive only, link from the repo):
| Kind | Where |
|---|---|
| Prices, quotes, contract terms, billed amounts | Drive (link only) |
| Accounts, license keys, Wi-Fi keys | Drive security folder |
| Staff/customer personal data (phone, address, SSN, pay) | Drive. Vendor contacts: name and title only |
| IP ranges, firewall settings, network diagrams | Drive |
| POS/payment details (PCI scope) | Drive |
| Legal disputes, HR matters | Drive |
| Email originals | Drive or mailbox; repo gets a summary |
PO, invoice and ticket numbers may be written.

## R-SEC-03
Sensitive values (emails, phones, account numbers, circuit IDs) go only to the Drive "Claude" folder (private, inherited sharing off). The repo keeps IDs and column names only: docs/drive-index/claude-folder.md. The folder is never shared; writes only from approved local sessions.

## R-SEC-04
Passwords and secret keys are stored nowhere: not in the repo, not in the Drive Claude folder, not in memory files.

## R-SEC-05
Found a sensitive value while writing → leave it out and tell the user "recommend keeping this in Drive". After a hook block on a sensitive value, ask the user; do not retry with variations.
