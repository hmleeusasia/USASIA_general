---
name: mail-triage
description: Gmail·Outlook·인트라넷 메일을 크롬으로 읽고(메일을 열지 않음) mail_triage.md 기준으로 할 일/기다림/참고/자동·버림 분류, 업무 기록에 반영. 새 연락처·조직은 즉시 사용자에게 묻고 승인 시 드라이브 주소록·orgs.md에 추가. "메일 확인", "안 읽은 메일", "메일 정리" 때 사용.
---

# 메일 점검·분류 (mail-triage)

먼저 읽기: docs/users/<id>/profile.md(메일함·범위) → docs/kb/mail_triage.md(분류 기준) → docs/kb/orgs.md(조직 목록: 통째로 읽지 말고 발신 조직·도메인을 grep, D-20261104-3). 아래 메일함 읽는 법은 profile에 있는 메일함만
읽기만 한다: 보내기·지우기·이동·읽음 표시 변경 금지. 기준일 = 사용자가 말한 날짜, 없으면 CURRENT_STATE "마지막 업무 시작".

## 1. 메일함별 읽는 법
Gmail — 텍스트 방식(가벼움)
- Open `https://mail.google.com/mail/u/0/#inbox` in a new tab, wait 3 s. get_page_text returns empty here too (2026-11-04) → use javascript_tool on `tr.zA` rows: unread = class `zE`, date = `td.xW span` title; mask emails/phones/URLs in JS (browser.md rules 5–6)
- 기준일 이후 줄만 본다. 광고·알림(ChatGPT, Newegg, Claude Team 등)은 빼고 업무 메일만 표로

Outlook — 접근성 목록 방식 (메일을 열지 않음 → 읽음 처리 없음)
- Browser rules: docs/kb/browser.md (read first)
- `https://outlook.office.com/mail/` (or `/mail/sentitems`) → run `tools/browser/outlook_list.js` (CUTOFF = base date) → read `window._ol` in slices. Rows starting "Unread" = unread. Fallback: find "message list listbox" → read_page(ref, depth 3)
- 검색창 입력(isread:no 등)은 적용이 안 됐음 — 쓰지 말 것. 스크린샷은 필요할 때만(scale 0.6)
- 본문은 사용자가 고른 메일만: 클릭 → find "message body" → read_page(ref, max_chars 4000)
- 메일을 열면 읽음 처리됨 → 꼭 필요한 것만 열고, 연 메일을 보고에 적는다
- get_page_text는 Outlook에서 안 됨(시도하지 말 것)

인트라넷 메일(그룹웨어) — 스크린샷 1장
- **받은메일함만** 본다: `https://newintra.seoulgrocery.com/ngw/app/#/mail/list/Maildir/` 로 바로 이동(홈 화면 스크린샷은 멈출 수 있음) → 3초 대기 → 스크린샷(scale 0.7) 1장
- 인보이스 관련 개인메일함(안 읽음 약 4,250)은 보지 않는다. 전체 메일 화면도 쓰지 않는다
- get_page_text는 미리보기만 나옴. 기준일 지난 줄까지만 본다

보낸편지함 (기다림 판정용)
- Gmail `#sent` → get_page_text / Outlook 보낸 편지함 → find "message list listbox" → read_page / 인트라넷 보낸메일함 스크린샷 1장
- 내가 요청하고 답이 없는 건 → 기다림 후보 (사용자 확인 후 #waiting)

## 2. 분류
- mail_triage.md 판정 순서대로 메일(스레드)마다 하나. 규칙에 없으면 "추측" 표시
- 기한 요청·긴급·경고 뉘앙스·⚠보안은 분류와 상관없이 보고 맨 위
- 같은 건이 여러 메일함에 있으면 한 건

## 3. 새 연락처·조직 (바로 묻기 — 사용자 요청: 나중에 물으면 기억 못 함)
- orgs.md에 없는 회사·도메인, 주소록에 없는 사람이 보이면 그 자리에서 묻는다: "누구/어느 조직/무슨 관계?"
- 승인되면: 조직 → orgs.md 한 줄 / 사람 → 드라이브 본인 드라이브 Claude 폴더(profile) 10_주소록 (ID: docs/drive-index/claude-folder.md). 이 계정 커넥터는 셀 편집 불가 → Claude 폴더 90_변경대기 시트에 줄 단위로 적고(열: 요청일·대상 파일·작업·찾을 줄(이름)·열·새 값·승인·상태·반영일·비고 — 원본과 같은 10열, **주소록 한 칸 = 한 줄**, 승인 칸은 '승인(사용자 YYYY-MM-DD)', 상태 '대기'), CURRENT_STATE C절 H-sheet 건수 갱신. 반영은 클라우드 계정(D-20261102-17). 이 계정은 90_변경대기에도 줄을 못 붙이므로 변경 묶음마다 같은 열의 새 시트 `90_변경대기_YYYY-MM-DD_n`을 Claude 폴더에 만든다(create_file, CSV). 클라우드가 반영 후 원본 90_변경대기 시트로 옮겨 적고 묶음 파일 이름 앞에 `완료_`
- 주소록을 읽을 때는 90_변경대기와 `완료_`가 안 붙은 묶음 파일의 '대기' 줄도 함께 본다
- GitHub에는 이름·직함·소속까지만

## 4. 기록
- docs/log/YYYY/YYYY-MM-DD_<id>.md: 할 일 #open, 기다림 #waiting(대상·확인일), 참고 한 줄, 자동·버림은 "메일 점검" 줄에 건수만
- 경계 사례·사용자 판정은 mail_triage.md 2절, 확정된 규칙은 1절(사용자 확인 시에만)
- 메일 원문·주소·전화·비밀번호는 저장소에 쓰지 않음(docs/rules/security.md)
- Team member context (D-20261105-7): every mail involving a USASIA IT member (docs/team/INDEX.md) — even "not my scope" or reference — gets one row in docs/team/<name>.md "Work context" (date, one-line work summary from the list preview, link). Things we don't know about their area → "Ask when they join". Work facts only: no evaluations, HR, complaints, contacts. Same for chats the user pastes and STWS tickets they watch or own

## 5. Reply drafts
- Before a draft states facts from quotes, specs or files (models, power, storage, what is included, locations), first show a short table: **confirmed (source) / assumed**. Only confirmed facts go into the draft; ask the user about the assumed ones. Draft in the recipient's language; Claude never sends — the user sends (2026-11-03: IQ camera reply took 6 rounds from assumptions)
