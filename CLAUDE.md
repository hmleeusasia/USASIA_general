# CLAUDE.md

작업 원칙: **docs/project_instructions.md** 를 따른다 (이 파일은 저장소별 설정만 담는다).

## 세션 시작 순서
1. 이 파일 → `docs/CURRENT_STATE.md` 전부 읽기
2. 할 일·등급(가벼움/무거움)·맡을 곳을 한 번에 알리고 승인받기
3. 끝날 때: CURRENT_STATE 바뀐 절만 고침(80줄 이하), 새 결정은 `docs/decisions.md`, 커밋·push

## 저장소 개요
- USASIA 마트(미국 워싱턴주, 여러 매장) IT 부서 업무 기록·색인 저장소
- 주 업무: ① 구글 드라이브 문서 색인(요약·키워드·링크) ② 이메일 작성 지원 + 날짜별 업무 기록(업체·결정·일정·팁)
- **원본·민감 정보는 구글 드라이브, GitHub엔 2차 문서만** → docs/storage_rules.md 필수 준수

## 문서 위치
| 종류 | 위치 | 템플릿 |
|---|---|---|
| 날짜별 업무 기록 | docs/log/YYYY/YYYY-MM-DD.md | docs/templates/daily_log.md |
| 업체별 요약 | docs/vendors/<이름>.md | docs/templates/vendor.md |
| 드라이브 색인 | docs/drive-index/<주제>.md | docs/templates/drive_index.md |
| 키워드 표준 | docs/keywords.md | — |
| 오래된 기록 | docs/archive/YYYY/ | — |

## 작업 규칙
- 업무 기록 작성 시: 키워드는 keywords.md에서만, 결정은 decisions.md에도 한 줄, 업체 파일 이력 표 갱신
- 민감 정보 발견 시 빼고 "드라이브 보관 추천" 알림
- 드라이브 색인은 폴더 단위로 나눠 진행, 대량 읽기는 작은 모델 하위 에이전트에 맡김
- 세션 끝: docs/session_review.md 점검표 수행 후 비효율 평가 표 보고

## 질문 유형별 먼저 볼 곳
| 질문 | 먼저 볼 곳 |
|---|---|
| 지금 상태·할 일 | docs/CURRENT_STATE.md |
| 과거 결정 이유 | docs/decisions.md |
| 업무 지식·팁 | docs/kb/INDEX.md |
| 과거 업체 일 | docs/vendors/INDEX.md → 업체 파일 |
| 특정 날짜·키워드 | `grep -rl "#키워드" docs/log` |
| 드라이브 문서 찾기 | docs/drive-index/INDEX.md |
| 진행 중 계획 | docs/requests/ |

## 저장소별 설정 (임시값 — 정해지면 교체)
- 시험·빌드:          해당 없음 (문서 저장소). 점검은 session_review.md
- 검색 도구:          grep -rn "#키워드" docs/ (전용 스크립트는 필요해지면 tools/에)
- 지식 문서 시작점:   docs/kb/INDEX.md
- 작업 브랜치 규칙:   claude/* 브랜치에서 작업, main 병합은 사용자 요청 시에만
- 사용자 언어·말투:   한국어, 결론 먼저, 표 활용
