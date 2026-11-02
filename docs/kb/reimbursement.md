# 경비 청구(Reimbursement) 월별 정리 방법 (확인: 2026-11)

## 흐름
노션 DB "Reimbursement"(평소 기록) → 구글 시트 "Reimbursement"로 월 단위 옮김 → 영수증 폴더에서 링크 연결
- 노션: https://app.notion.com/p/24d0aac49b1680e0a2d8f30adf16e33d
- 시트: https://docs.google.com/spreadsheets/d/1MifTpXF_xGcix8ULSKGXnWDnS1pPOi76D2Nh9MmnZEU
- 영수증 폴더: https://drive.google.com/drive/folders/1nrYiVV5Nrwp9glxhdM_Vjyz8P8Gx6hx0 (코드별 하위 폴더)

## 규칙
- Milage 아닌 건 → Others 탭(A~I). Milage → Driving 탭(H 마일, J `=$I$1*H행`, 단가 I1)
- 코드: 분류가 여러 개면 **앞의 분류** 기준. Meal→WE0002, Business Trip→WE0001, Parking→WE0006, Office→WE0011, 정액 출장비→ETC
- 출장 정액 출장비 행(예: 5일 $250)은 노션에 없으므로 따로 추가
- **점심 $18 = 최대 청구 금액**(사용자가 수동으로 깎음). 영수증 금액이 더 커도 같은 날 영수증이면 연결
- 마일 빈칸은 Driving·이전 마일리지 탭의 같은 구간 거리로 채움, 기록 없는 구간은 빼고 알림
- 새 달 넣을 때 요청여부 ✔, 지난달은 완료(Others I / Driving L) ✔
- 노션 시각은 UTC 저장 → PDT/PST로 바꿔 넣기
- 영수증 파일명은 엉터리가 많음 → 내용(날짜·금액)으로 맞춤
