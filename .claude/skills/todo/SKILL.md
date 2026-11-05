---
name: todo
description: 사용자가 말로 준 새 요청을 할 일 목록에 추가. 메시지가 "Todo", "todo:", "할일:"로 시작하거나 "/todo"일 때 사용. 한 메시지에 여러 건이어도 됨.
---

# 할 일 추가 (todo)

사용자 메모 형식(아는 것만): 요청자, 매장, 기한, 티켓 여부, 내용. 빠진 건 묻지 않고 비워 둔다.

## 1. 나누기
- 요청자 → 이름·직함 (주소록·orgs.md에 없으면 끝에 "추가할까요?" 한 번 묻기)
- 매장 → docs/kb/store_codes.md 약어로 (모르면 사용자 말 그대로)
- 기한 → 요청에 있을 때만 날짜로 (이번 주=그 주 금요일, 이번 달=말일). 없으면 기한 없음
- 조건(예: "BV 갈 때") → 다음 칸에

## 2. 기존 건 확인
- docs/users/<id>/todo.md에서 같은 매장·비슷한 내용의 T-티켓·M-건을 찾는다
- 비슷한 게 있으면 "T-606과 같은 건인가요?"를 보고에 함께 묻고, 답이 오기 전엔 새 ID로 적어 둔다

## 3. 적기 (값은 R-SEC-02 (docs/rules/security.md)대로, 연락처 금지)
- todo.md 2절 전체 목록: `| M-<짧은이름> | 내용. 요청 <이름>. 티켓 작성 필요 | 매장 | #분야 | 할 일 | 오늘 | 기한·다음 |`
- 기한이 이번 주 안이거나 사용자가 급하다고 하면 1절 '지금'에도
- 오늘 업무 기록 `docs/log/YYYY/YYYY-MM-DD_<id>.md`: `### 제목  #분야 #종류 #open` + 요청자·내용·기한·다음
- 티켓이 생기면 M-ID를 T-번호로 바꾼다 (todo-sync가 맞춤)

## 3-1. STWS 티켓 만들기 (사용자가 요청할 때만, 하나씩)
- Create → Summary: 사용자 스타일 `<매장약어>-<내용>` (예: `LW- 델리 저울 고장`, `NWHQs-PC office 재설치`)
- Request type: General IT Support / Store: 목록에 있으면 그 매장, 본부 등은 No store / Department: ETC
- Description: 요청자, 기한, 작업 단계
- 입력은 좌표 클릭 후 type (ref로 넣으면 안 들어감), Create는 find로 찾은 "Create request" 버튼 ref로 누른다. 없는 기한은 쓰지 않는다
- Create 누르기 전에 입력값을 사용자에게 보여 주고 승인받는다
- 만든 뒤 목록에서 새 번호를 확인 (생성 직후 목록에 안 보이면 다시 만들지 말고 사용자에게 확인)
- 기존 티켓의 연장이면 서브 티켓으로: 상위 티켓 `https://stws.seoulgrocery.com/st/dashboard/tickets/<번호>` → "Add subtask" → 제목 입력 → Create (Assignee는 상위 티켓 담당을 따름). **이 창은 제목만 받으므로** 새 티켓을 열어 Description "Edit" → 설명(첫 줄에 상위 TICKET 번호) → Save. 설명도 Create 전에 승인받는다
- 내 일이 확실하면 Assignee를 나(profile.md STWS 번호)로 바꾸자고 먼저 사용자에게 묻고, 승인 뒤 바꾼다 (기본 담당자는 Dan Choi)

## 4. 끝
- 받은 건을 표로 짧게 보고 (ID·할 일·기한), 물을 점은 맨 끝에 묶어서
- 여러 건을 받는 중이면 사용자가 "끝"이라고 할 때 커밋·push
- 다음 start-day 보고 맨 위 "어제 받은 요청"에 나온다 (todo.md 갱신일 기준)
