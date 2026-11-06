# Expense rules (receipts, mileage)
Source: D-20261104-1, D-20261105-1, docs/kb/reimbursement.md (procedure and per-month steps stay there). Targets are per user (profile.md Tools table): the expense Sheet is the baseline; Notion as expense DB is optional (hmlee only today) and used only when the profile Tools table has a Notion row with Have = y. Write only to the targets the user has (D-20261106-1).

## R-EXP-01
"출발/depart" and "도착/arrive" messages are mileage events: log them live, the same turn, to the user's targets: the Sheet "Driving" tab, plus Notion if the profile Tools table has Notion = y. Do not wait for month-end.

## R-EXP-02
All dates and times use the user's time zone (profile.md). A source that stores UTC (e.g. Notion) → convert to the user's zone before writing to the Sheet.

## R-EXP-03
Before writing any Sheet row, read the target row back and confirm it is empty (2026-11-03 an off-by-one overwrote a row).

## R-EXP-04
Empty miles → fill from the same route in the Driving or previous mileage tab. No record for that route → leave the row out and tell the user.

## R-EXP-05
Company policy, the same for everyone (D-20261106-1). Mileage rows go to the Driving tab; everything else to the Others tab. Code by the first category; exception Meal+Visitor → WE0003. Lunch claim cap $18 (user trims the amount; a same-day receipt is still linked).

## R-EXP-06
Receipt intake: user scans into the Drive code folder and says so → Claude reads date/amount from the content (file names are unreliable), renames `Receipt - <place> - YYYY. M. D..pdf`, adds the Sheet Others row with the link, plus a Notion row (Unpaid) if the profile Tools table has Notion = y.

## R-EXP-07
Receipt photo in chat only when unavoidable: Claude makes a PDF and sends it back; the user uploads it (connector upload needs inline base64).
