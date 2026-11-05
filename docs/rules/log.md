# Work log rules
Source: CLAUDE.md "Where things go" / judgment rules, docs/templates/daily_log.md, D-20261102-11, D-20261102-19, D-20261105-1. Template: docs/templates/daily_log.md. Hook: log-path (guard.py).

## R-LOG-01
One file per person per day: `docs/log/YYYY/YYYY-MM-DD_<id>.md`. Several sessions on one day append in time order. Over 200 lines → `YYYY-MM-DD_<id>-2.md`. Old logs → docs/archive/YYYY/.

## R-LOG-02
Each entry starts `### Title  #field #kind #target` with tags from docs/keywords.md (unregistered tags fail check.py). Add `#open` or `#waiting` when not finished; `#waiting` entries name who we wait for and a check date.

## R-LOG-03
Each entry must make sense alone: write vendor and store names in full; no "that case" / "the vendor above".

## R-LOG-04
Decisions are explained only in docs/decisions.md; the log carries the decision ID.

## R-LOG-05
Dates live in the entry body as YYYY-MM-DD. docs/calendar.md only for recurring or long-term dates. "Today/yesterday" and times follow the user's time zone in docs/users/<id>/profile.md, never the machine clock.

## R-LOG-06
No amounts, accounts, keys, IPs, serial numbers or personal contacts in log text (R-SEC-02). Link the Drive original instead.

## R-LOG-07
Create a hub `docs/{vendors,stores,assets,projects}/<name>.md` when the first related entry appears. No hand-written history tables in hubs; history comes from `tools/find.py`.

## R-LOG-08
Before writing a tip, run `tools/find.py <keyword> "#tip"`. If it already exists, promote it to docs/kb/<topic>.md and add one line to docs/kb/INDEX.md.
