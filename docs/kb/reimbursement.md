# 경비 청구(Reimbursement) 월별 정리 방법 (확인: 2026-11)

## 흐름
노션 DB "Reimbursement"(평소 기록) → 구글 시트 "Reimbursement"로 월 단위 옮김 → 영수증 폴더에서 링크 연결
- 노션: https://app.notion.com/p/24d0aac49b1680e0a2d8f30adf16e33d
- 시트: https://docs.google.com/spreadsheets/d/1MifTpXF_xGcix8ULSKGXnWDnS1pPOi76D2Nh9MmnZEU
- 영수증 폴더: https://drive.google.com/drive/folders/1nrYiVV5Nrwp9glxhdM_Vjyz8P8Gx6hx0 (코드별 하위 폴더)

## 제출
- Dan Choi 부장님 소유 공유 폴더 "Hyunmyung Lee"/Monthly 개인경비/<연도>/ 에 그 달 폴더 `YYYYMM(신청)`을 만들고 정산 시트·사용 내역을 넣는다 (회계 KF 2명 편집 공유)
- 처리 끝나면 폴더 이름을 `YYYYMM(완료)`로 바꾼다. 영수증 원본은 내 드라이브 Reimbursement/PDF/Archive/<월> 아래 WE코드 폴더
- 위치: docs/drive-index/purchase-reimbursement.md "공유 폴더" 절

## 규칙
- Milage 아닌 건 → Others 탭(A~I). Milage → Driving 탭(H 마일, J `=$I$1*H행`, 단가 I1)
- 코드: 분류가 여러 개면 **앞의 분류** 기준. 예외: Meal+Visitor(외부인사 식사)→WE0003. Meal→WE0002, Business Trip→WE0001, Parking→WE0006, Office→WE0011, 정액 출장비→ETC
- 출장 정액 출장비 행(예: 5일 $250)은 노션에 없으므로 따로 추가
- **점심 $18 = 최대 청구 금액**(사용자가 수동으로 깎음). 영수증 금액이 더 커도 같은 날 영수증이면 연결
- 마일 빈칸은 Driving·이전 마일리지 탭의 같은 구간 거리로 채움, 기록 없는 구간은 빼고 알림
- 새 달 넣을 때 요청여부 ✔, 지난달은 완료(Others I / Driving L) ✔
- 노션 시각은 UTC 저장 → PDT/PST로 바꿔 넣기
- 영수증 파일명은 엉터리가 많음 → 내용(날짜·금액)으로 맞춤

## Daily receipt intake (agreed 2026-11-03)
- User scans receipt with Drive app (+ → Scan) straight into the code folder (e.g. WE0002), then says "receipt uploaded"
- Claude: find new file in folder → read date/amount → rename `Receipt - <place> - YYYY. M. D..pdf` → add Notion row (Unpaid) → add Sheet Others row with link (요청여부/완료 FALSE until month-end)
- Photo in chat only when unavoidable: Claude makes PDF and sends it back; user uploads it (connector upload needs inline base64 = error-prone)
- Meal receipt: Notion Doc name "점심", Category Meal, code WE0002(식비); claim cap $18
