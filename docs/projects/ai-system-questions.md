# AI 시스템 만들기 — 모아 둔 고민 (나중에 한꺼번에 결정)  #proj-ai-system
<!-- 2026-11-03 사용자 요청: 공용/개인 구분 같은 틀 고민은 바로 정하지 말고 여기에 모은다. 새 고민이 나오면 Claude가 한 줄 추가하고 사용자에게 "숙제에 추가함"이라고만 알린다.
     결정되면 decisions.md(공용) 또는 users/<id>/(개인)에 쓰고 여기서는 "→ D-..."로 표시. 관련: D-20261102-19, CURRENT_STATE H-multi -->

| # | 고민 | 나온 날 | 지금 상태·제안 |
|---|---|---|---|
| Q1 | 결정을 공용/개인으로 나눌까? 개인 결정 파일(`users/<id>/decisions.md`)과 번호(`D-<id>-날짜-n`) | 2026-11-03 | 오늘 결정 D-20261103-1·4는 공용 규칙+hmlee 사정이 섞임. D-2·3은 공용 |
| Q2 | 공용 결정은 누가 승인? (hmlee 개발자 / Dan Choi 부장 / 팀 합의) | 2026-11-02 | H-multi 미정 항목 |
| Q3 | CURRENT_STATE를 공용(저장소 작업)과 개인(`users/<id>/state.md`)으로 나눌까? | 2026-11-03 | 오늘 클라우드·로컬 동시 수정으로 push 거절 1회 발생 |
| Q4 | 로컬도 main 직접 대신 브랜치에서 작업할까? (D-12 개정) | 2026-11-03 | 클라우드 ff 실패 시 처리 절차도 필요 |
| Q5 | git 이력의 예전 이메일 주소 정리(filter-repo + 강제 push + 재클론) | 2026-11-02 | 실제 15개 이상 확인(2026-11-03). 한 사람일 때가 쉬움 |
| Q6 | 팀 공용 민감 값·주소록·90_변경대기를 공유 드라이브로? (D-16·17 개정) | 2026-11-03 | 각자 Claude 폴더만으로는 팀원이 서로 못 봄 |
| Q7 | 사람별 git 사용자·커밋 작성자 표시 (클라우드 커밋이 "Claude"로만 남음) | 2026-11-03 | |
| Q8 | mail_triage.md 0절(hmlee 담당 범위)을 users/hmlee/mail_rules.md로 옮기기 | 2026-11-02 | H-multi 2단계 |
| Q9 | 공동 편집 파일(vendors/·calendar.md) 정리·archive 때 남의 내용 보호 규칙 | 2026-11-03 | |
| Q10 | check.py를 커밋 전에 자동 실행(pre-commit hook) | 2026-11-03 | 지금은 규칙만, hook 없음 |
| Q11 | 05_Inbox·06_Files 절차를 skill로 만들까? (팀원도 같은 방식) | 2026-11-03 | D-20261103-4 |
| Q12 | Existing Korean docs → English: bulk convert now, or convert as each file is edited? Which first (skills, kb, CLAUDE.md)? Keep Korean synonyms in keywords.md for search? | 2026-11-03 | D-20261103-5 set English for new text |
| Q13 | Onboarding tutorial (new teammate, fresh Claude account) — **receipt/expense setup step**: (1) ask where receipt photos/PDFs are stored (Drive folder per code?) (2) ask where expenses are recorded; if none, create it (Notion DB + Sheet from template) (3) ask whether they already track expenses another way, adopt theirs. Reference flow: kb/reimbursement.md "Daily receipt intake" | 2026-11-03 | User request; goes into onboarding.md (H-multi stage 2) |
| Q14 | Lean context: minimal md + hooks enforce rules (SessionStart digest, PreToolUse guard, Stop checklist). Plan: docs/requests/PLAN-lean-context-001-draft2.md | 2026-11-03 | Agreed Opus+Sonnet, awaiting user approval. Includes Q10 |
