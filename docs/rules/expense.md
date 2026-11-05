# Expense rules (receipts, mileage)
Source: D-20261104-1, D-20261105-1, docs/kb/reimbursement.md (procedure and per-month steps stay there). Targets (Notion DB, Sheet, receipt folders) are per user: docs/users/<id>/profile.md or docs/kb/reimbursement.md.

## R-EXP-01
"출발/depart" and "도착/arrive" messages are mileage events: log them live, the same turn, to Notion and the Sheet "Driving" tab. Do not wait for month-end.

## R-EXP-02
All dates and times use the user's time zone (profile.md). Notion stores UTC → convert to PDT/PST before writing to the Sheet.

## R-EXP-03
Before writing any Sheet row, read the target row back and confirm it is empty (2026-11-03 an off-by-one overwrote a row).

## R-EXP-04
Empty miles → fill from the same route in the Driving or previous mileage tab. No record for that route → leave the row out and tell the user.

## R-EXP-05
Mileage rows go to the Driving tab; everything else to the Others tab. Code by the first category; exception Meal+Visitor → WE0003. Lunch claim cap $18 (user trims the amount; a same-day receipt is still linked).

## R-EXP-06
Receipt intake: user scans into the Drive code folder and says so → Claude reads date/amount from the content (file names are unreliable), renames `Receipt - <place> - YYYY. M. D..pdf`, adds the Notion row (Unpaid) and the Sheet Others row with the link.

## R-EXP-07
Receipt photo in chat only when unavoidable: Claude makes a PDF and sends it back; the user uploads it (connector upload needs inline base64).
