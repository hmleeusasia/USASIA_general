---
name: todo-sync
description: 개인 할 일 보드(docs/users/<id>/todo.md)와 STWS 티켓(보고용)을 동기화하고 "지금" 할 일을 제안한다. "할 일 목록", "티켓 동기화", "STWS 동기화" 때 사용 ("Todo:"로 시작하는 새 요청은 todo skill). start-day에서도 부른다.
---

# 할 일 동기화 (todo-sync)

원본 = docs/users/<id>/todo.md (<id>는 CLAUDE.md '누구인지' 규칙). STWS 담당자 번호는 profile.md. STWS는 보고용 → 티켓 상태 변경은 사용자가 승인한 목록만 Claude가 반영(5절), 생성·삭제·담당자 변경·댓글은 요청 시에만. 장기 프로젝트는 사용자가 따로 관리(관련 있으면 이름만 적음). D-20261102-18

## 1. STWS 읽기 (크롬, 읽기만; browser rules: docs/kb/browser.md)
- get_page_text는 티켓 목록 페이지에만 쓴다. 대시보드·티켓 상세 등 다른 화면은 find·read_page로 필요한 부분만 (대시보드엔 사원 명단·이메일이 나옴, 사용량·민감 정보)
- `https://stws.seoulgrocery.com/st/dashboard/tickets?page=N&per_page=20&sort=updated_at&direction=desc&assignee=<profile의 STWS 담당자 번호>`
- browser_batch로 [navigate → wait 2 → get_page_text]를 페이지마다. "x–y of N"으로 끝 확인. 첫 화면은 표가 늦게 뜨므로 wait 필수
- 내가 Reporter인 남의 티켓은 assignee 필터에 안 나옴 → 필요할 때만 필터 없이 1쪽 확인

## 2. 맞추기
- New ticket → add to section 2 with its T-number. STWS Resolved/Cancelled → status 끝/취소; `python3 tools/prune.py --apply` moves the row to archive 2 days later (history stays in the log, D-20261104-3). STWS "Closed" is not tracked — Resolved is the end (user, 2026-11-04)
- 메일·업무 기록의 #open 중 todo.md에 없는 것 → M-<짧은이름>으로 추가 (티켓 없음 표시)
- 움직임 = 둘 중 최근 날짜. 30일 넘으면 ⏸
- 줄 고칠 때: 경과는 그날 업무 기록으로, 보드 "다음"은 다음 할 행동 하나로 덮어쓰기(≤ 80자, 행 ≤ 220자). 경과 보기 `py tools/find.py --id <ID>` (D-20261106-3)
- 매장 약어: BV Bellevue, BV(구) Bellevue Legacy, LW Lynnwood, GLW GMart Lynnwood, MW Mellowway, IS Issaquah, RM Redmond, FW Federalway, UW, BL Ballard, CP Campeon, M2M, 본부 EGMM/NWHQ

## 3. "지금" 제안 (3~7건)
우선순위: 기한·긴급 메일 > 닫기만 하면 되는 건 > 최근 2주 움직인 매장 요청 > 오래 기다린 업체 건 재확인. 이유 한 줄씩. 사용자가 고르면 확정

## 4. 보고·저장
- 표: 새 티켓 / 상태 바뀜 / 해결 제안(끝났는데 STWS가 아직 Resolved 아님) / ⏸ 결정 필요 / "지금" 제안
- todo.md 머리줄 갱신일·건수 고치고 커밋

## 5. 상태 변경 반영 (승인된 목록만)
- 먼저 "T-번호 → 상태" 목록을 보여 주고 승인받는다. 승인은 그 목록에만 유효
- 티켓 주소 `https://stws.seoulgrocery.com/st/dashboard/tickets/<번호>` → wait 2 → 오른쪽 Status 드롭다운 클릭 → 값 클릭(Open, In progress, Pending, Resolved, Cancelled). 고르면 바로 저장됨(저장 버튼 없음)
- 확인: 같은 주소 다시 열고 find "Status select current value" → 값 확인 후 todo.md 4절에 기록
- After all STWS changes (status, ticket create, assignee): open the bell → notifications created by this session's own changes (actor = me, matching ticket, today) → click each to mark read (clicking marks it read; read items drop off the list, so clicking the top item repeatedly works). Leave notifications from other people unread. Confirm the unread count is gone (2026-11-03)
- Close(완전히 닫기)는 **사용자가 직접**(2026-11-02 사용자 결정). Claude는 Resolved까지만 바꾸고 "닫을 티켓: T-…" 목록만 보고. 다음 동기화 때 CLOSED면 todo.md에서 뺌 (참고: Close ticket 버튼은 브라우저 확인창을 띄워 크롬 도구가 멈춤)
- 드롭다운 위치는 화면마다 스크린샷(scale 0.6)으로 확인 후 클릭
- Create ticket (on request only; verified: hmlee, STWS permission Manager, 2026-11-04 — screens may differ by permission, Q16): top-bar Create → Request type "General IT Support", Store, Department ETC. Assignee is auto-set and locked in the form → after creating, open the ticket → "Change assignee" (2026-11-04). Parent ticket cannot be set to Resolved while a subtask is open
