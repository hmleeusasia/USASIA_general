# 세션 종료 점검표 (매 세션 끝에 Claude가 수행·보고)

## 1. 문서 점검
- `python3 tools/check.py` 실행 (아래 중 자동 항목 포함)
- `python3 tools/find.py --open` → CURRENT_STATE C절 갱신
- CURRENT_STATE.md 80줄 이하, kb/facts.md 50줄 이하인가
- 새로 알게 된 계속 유효한 사실 → kb/facts.md 반영
- 분기마다, 단 docs/log의 기록 파일이 60개 이상일 때만: 오래된 달부터 월별 요약(docs/log/YYYY/YYYY-MM-summary.md, 10~20줄, 건마다 "### 제목  #태그" 한 줄 + 결정 ID) 작성 → 원본은 docs/archive/YYYY/로 이동
  - 요약에는 #open/#waiting 쓰지 않음. 이동 전 미결 건은 #done 처리하거나 CURRENT_STATE로 옮김
- python3 tools/find.py --open (기한초과 확인), --due (30일 일정)
- 팁 승격은 쓸 때 검색으로 처리(템플릿 주석). 점검 때 따로 찾지 않음
- 분기마다: 남은 claude/* 원격 브랜치 정리를 사용자에게 알림 (GitHub 웹 Branches 화면에서 삭제, D-20261102-7)
- INDEX 파일들이 실제 파일과 맞는가 (빠진 것·죽은 링크)
- keywords.md 밖의 키워드나 같은 뜻 중복이 생겼나
- GitHub에 있으면 안 되는 정보(storage_rules.md)가 섞였나

- 틀 점검(정보가 늘면서): 분류 기준·태그 목록·허브 종류·템플릿·폴더 구조·kb 주제에 바꾸거나 더할 것이 있나
  - 근거 예: 같은 태그 조합 반복(새 태그 후보), 허브 없는 대상 반복 등장, 분류가 애매했던 메일·문서, 한 파일이 너무 커짐
  - 있으면 "틀 변경 제안" 표(무엇·왜·영향 파일)로 사용자에게 보고. 승인 전엔 바꾸지 않음

## 2. 비효율 평가 표 (사용자에게 보고)
| 무엇이 낭비였나 | 원인 | 고칠 안 | 반영 위치 |
|---|---|---|---|

점검 항목:
- 반복된 손작업 → 스크립트(tools/)나 템플릿으로
- 새 업무 유형 → 새 폴더·템플릿 필요 여부
- 서브 에이전트 분담: 작은 모델로 충분했던 일을 큰 모델이 했나, 좌표 없이 맡겨 재검색했나
- 지휘 과정: 질문 왕복이 많았나, 한 번에 묶을 수 있었나
- 사용량: 큰 파일 통째 읽기, 드라이브 중복 조회 등

채택된 안은 decisions.md에 기록하고 해당 문서에 바로 반영.

## 3. 마무리
1. python3 tools/check.py 통과 → CURRENT_STATE 갱신 → 커밋·push(작업 브랜치)
2. `git fetch origin main && git checkout -B main origin/main && git merge --ff-only <작업 브랜치> && git push origin main`
3. fast-forward 안 되면 멈추고 사용자에게 알림
