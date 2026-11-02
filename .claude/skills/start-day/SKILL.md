---
name: start-day
description: USASIA IT 업무 시작 루틴. 저장소 동기화, 상태·열린 건·일정 확인, Gmail·Outlook 새 메일과 드라이브 변경을 훑어 오늘 할 일 표를 만들고 승인받는다. "업무 시작", "아침 루틴", "/start-day" 때 사용.
---

# 업무 시작 루틴 (start-day)

읽기만 한다. 메일 보내기·지우기·이동, 드라이브 수정·공유 변경은 하지 않는다.
결론 먼저, 표로 보고한다(한국어).

## 0. 장소 확인
- 로컬 PC(Windows, 크롬 확장 연결됨) → 아래 전부
- 클라우드 세션 → 1~3, 6만 (크롬 없음. 드라이브는 커넥터가 있으면 5도)

## 1. 동기화
- 로컬: `git pull origin main` (충돌·미커밋 변경 있으면 멈추고 보고)

## 2. 상태 읽기
- CLAUDE.md → docs/CURRENT_STATE.md → docs/kb/facts.md
- CURRENT_STATE의 "마지막 업무 시작"을 기준일로 쓴다 (없으면 7일 전)

## 3. 열린 건·일정
- `py tools/find.py --open` (기한초과 표시 확인)
- `py tools/find.py --due` (30일 일정)

## 4. 메일 (기준일 이후만)
Gmail — 텍스트 방식(가벼움)
- 크롬 새 탭에서 `https://mail.google.com/mail/u/0/#inbox` → get_page_text 1번 (검색 결과 화면은 get_page_text가 비어 나옴)
- 기준일 이후 줄만 본다. 광고·알림(ChatGPT, Newegg, Claude Team 등)은 빼고 업무 메일만 표로

Outlook — 접근성 목록 방식 (메일을 열지 않음 → 읽음 처리 없음)
- `https://outlook.office.com/mail/` → find "message list listbox" → read_page(ref, depth 3)
- 각 줄 앞 "Unread" = 안 읽음. 목록은 화면에 보이는 것만 나오므로 browser_batch로 [scroll 10 → read_page] 반복, 기준일 지나면 멈춤
- 검색창 입력(isread:no 등)은 적용이 안 됐음 — 쓰지 말 것. 스크린샷은 필요할 때만(scale 0.6)
- 본문은 사용자가 고른 메일만: 클릭 → find "message body" → read_page(ref, max_chars 4000)
- 메일을 열면 읽음 처리됨 → 꼭 필요한 것만 열고, 연 메일을 보고에 적는다
- get_page_text는 Outlook에서 안 됨(시도하지 말 것)

공통: 끝나면 만든 탭을 닫는다. 메일 원문은 저장소에 쓰지 않는다(요약만, storage_rules.md).

## 5. 드라이브 변경
- 드라이브 커넥터 search_files: `modifiedTime > '<기준일>T00:00:00Z'`, excludeContentSnippets true
- docs/drive-index에 없는 새 문서·바뀐 문서를 표로 (색인 갱신 후보)

## 6. 보고·승인
한 번에 보고:

| 구분 | 건 | 기한/날짜 | 제안 |
|---|---|---|---|
| 기한초과·열린 건 | | | |
| 30일 일정 | | | |
| 새 업무 메일 (Gmail/Outlook) | | | 기록·답장 초안 등 |
| 드라이브 변경 | | | 색인 갱신 여부 |

그다음 오늘 계획(할 일·등급 가벼움/무거움·맡을 곳)을 제안하고 승인을 받는다.
승인 뒤 CURRENT_STATE의 "마지막 업무 시작" 날짜를 오늘로 고친다.

## 사용량 메모
- 이 루틴은 새 세션 첫머리에 돌린다(긴 세션일수록 호출 1번 비용이 큼)
- 크롬 동작은 가능하면 browser_batch로 묶는다
- Microsoft 365 커넥터가 승인되면 Outlook 단계를 커넥터로 바꾼다
