# PLAN-structure-001-draft2 (확정·구현됨, D-20261102-5)
draft1(archive/) + Sonnet 재검토 반영.
| 재검토 지적 | 반영 |
|---|---|
| 허브 수기 갱신 불일치 | 허브엔 개요+검색 명령만, 이력은 tools/find.py |
| front matter·태그 이중 | 소제목 태그 한 곳으로 통일 |
| 자산·일정 민감 정보 | 템플릿마다 금지 항목 명시, check.sh가 IP·금액·비밀번호 의심 탐지 |
| 시험 공허 통과 | 가상 기록 5건으로 질문형 시험 10건 + 부정 시험(미등록 태그·허브 없음·IP·금액) 실시 후 삭제 |
| 구입·인보이스 연결 키 | PO-/INV-/티켓 번호는 기록 허용 |
| 미결 추적 | find.py --open → CURRENT_STATE |
| 키워드 남발 | 대상 태그는 허브 파일 있을 때만, check.sh 검사 |
시험 결과: 동의어(MPOE→demarc, landline→phone, 구매→purchase), AND 검색, 번호 검색, 결과 없음, 열린 건 모두 기대대로. 발견 버그: 짧은 동의어 오일치 → 수정.
