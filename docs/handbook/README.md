# USASIA_general handbook
For a developer who has never seen this repo. Korean: [README.ko.md](README.ko.md).

| # | Page | You will know |
|---|---|---|
| 1 | [../ARCHITECTURE.md](../ARCHITECTURE.md) | What the repo is, principles, how Claude, hooks, skills and Drive fit together (overview) |
| 2 | [code-map.md](code-map.md) | Every Python tool and hook, each function, who calls it; hook rule modes; each skill and what it uses; each rule ID and where it is enforced |
| 3 | usasia_db repo, docs/handbook/ | The database app (data dictionary, request walkthrough) |

## How it stays correct
- `code-map.md` / `code-map.ko.md` are **generated** by `tools/handbook.py` from the code. Never edit them by hand.
- Meanings (en + ko) for modules, functions and skills: `docs/handbook/meta.json`. English falls back to the docstring.
- The git pre-commit hook (`tools/githooks/pre-commit`) runs `tools/handbook.py --check` whenever a commit touches tools/, .claude/skills/, docs/rules/ or docs/handbook/. It fails when a page is stale, a meaning is missing, or a page holds an email/IP address.
- After changing code: `py tools/handbook.py`, fill what it reports, stage, commit.

Not read by the generator (personal or machine-specific): docs/users/**, CLAUDE.local.md, .claude/settings*.json.
