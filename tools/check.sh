#!/usr/bin/env bash
# 문서 점검: 미등록 태그, 허브 없는 대상 태그, 민감 정보 의심, CURRENT_STATE 줄 수
cd "$(dirname "$0")/.." || exit 1
rc=0; logs=$(find docs/log docs/archive -name '*.md' 2>/dev/null)
[ -z "$logs" ] && { echo "기록 없음"; }
for t in $(grep -hoE '#[a-z][a-z0-9-]*' $logs /dev/null | sort -u); do
  case $t in
    \#vendor-*) f=docs/vendors/${t#\#vendor-}.md;;
    \#store-ops) f="";;
    \#store-*) f=docs/stores/${t#\#store-}.md;;
    \#asset-*) f=docs/assets/${t#\#asset-}.md;;
    \#proj-*) f=docs/projects/${t#\#proj-}.md;;
    *) f="";;
  esac
  if [ -n "$f" ]; then [ -f "$f" ] || { echo "허브 없음: $t → $f"; rc=1; }
  else grep -qE -- "$t( |$|\))" docs/keywords.md || { echo "미등록 태그: $t"; rc=1; }; fi
done
grep -rnE '\$ ?[0-9]|[0-9]{1,3}(\.[0-9]{1,3}){3}|([0-9A-Fa-f]{2}:){5}|password|passwd|비밀번호|api[_-]?key' docs --include='*.md' \
  | grep -v -e storage_rules.md -e templates/ -e keywords.md -e requests/ -e CLAUDE.md && { echo "↑ 민감 정보 의심 (storage_rules.md)"; rc=1; }
n=$(wc -l < docs/CURRENT_STATE.md); [ "$n" -gt 80 ] && { echo "CURRENT_STATE $n줄 > 80"; rc=1; }
[ $rc -eq 0 ] && echo "점검 통과"; exit $rc
