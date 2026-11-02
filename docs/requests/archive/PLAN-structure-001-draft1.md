# PLAN-structure-001-draft1: 모든 업무 유형을 담는 범용 구조

## 요청 원문(요약)
네트워크·인프라·개발·마트 업무·POS·서류·벤더·계약·자산·빌링·구입·청구서·개인 비용 청구 등 모든 업무를 구조 확장 없이 기록·검색 가능하게. 나중에 "언제 무슨 일, 무슨 결정"을 빠르게 찾기.

## 확정 결정
- D-20261102-2 GitHub=2차 문서, 원본·민감=구글 드라이브 (docs/storage_rules.md)
- 저장소 비공개. 드라이브 연결은 보류

## 설계
1. 기록 단위는 하나: docs/log/YYYY/YYYY-MM-DD.md (하루 1파일, 건별 소제목)
2. 키워드 3갈래 고정(목록은 확장 가능): 분야 / 일의 종류 / 대상(vendor-, store-, asset-, proj-)
3. 허브 4종: vendors/, stores/, assets/, projects/ — 각 이력 표에 기록 링크 한 줄
4. 공용: docs/calendar.md(갱신·만료·청구일·방문), docs/kb/(반복 절차·노하우), docs/decisions.md
5. keywords.md에 동의어 칸 (예: demarcation point, demarc, MPOE → #demarc)

## 바꿀 곳
- 신규: docs/stores/, docs/assets/, docs/projects/ (+INDEX.md), docs/templates/{store,asset,project}.md, docs/calendar.md
- 수정: docs/keywords.md(3갈래+동의어), docs/templates/daily_log.md(front matter: domains/activities/entities), CLAUDE.md 문서 위치 표

## 시험 칸 (가상 사례 → 찾을 수 있어야 하는 경로)
| 사례 | 기대 |
|---|---|
| ○○점 Granite 회선 청구 이의 | log 1건, vendors/granite·stores/○○·assets/회선 이력에서 도달, #billing으로도 검색 |
| 개인 비용 청구 | log + kb 절차, 영수증은 드라이브 링크 |
| POS 교체 프로젝트 | projects/ 허브, 결정 ID 연결, 세부는 드라이브 |
| 라이선스 만료 | calendar.md + assets/ |

## 위험 / 물을 점
- 허브 이력 갱신 누락 → 허브와 log 불일치
- 키워드 남발·동의어 미등록
- 하루 1파일이 커질 가능성
