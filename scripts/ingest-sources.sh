#!/usr/bin/env bash
# Ingest every URL from research/sources/*.tsv into the project llm-wiki kb.
# Usage: ingest-sources.sh [FILE.tsv ...]   (defaults to research/sources/*.tsv)
set -euo pipefail
shopt -s nullglob

BATCH_SIZE=5
FAIL_LOG="research/sources/ingest-failures.tsv"
KB_LOG=".kb/log.md"

files=("$@")
[ $# -eq 0 ] && files=(research/sources/*.tsv)

declare -A seen
urls=()
skipped=0
for f in "${files[@]}"; do
  [ "$f" = "$FAIL_LOG" ] && continue
  while IFS=$'\t' read -r url _title _kind _cited_by _why access; do
    if [ "$url" = "url" ] || [ -z "$url" ]; then
      continue
    fi
    url="${url%/}"
    if [[ "$url" =~ ^https://pubmed\.ncbi\.nlm\.nih\.gov/([0-9]+)$ ]]; then
      url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=${BASH_REMATCH[1]}&rettype=abstract&retmode=text"
    elif [ "$access" = "js-only" ]; then
      skipped=$((skipped + 1))
      continue
    fi
    if [ -n "${seen[$url]:-}" ]; then
      continue
    fi
    seen[$url]=1
    urls+=("$url")
  done < <(cat "$f"; echo)
done

if [ -f "$FAIL_LOG" ]; then
  survivors=$(mktemp)
  awk -F'\t' -v seen_list="$(printf '%s\n' "${!seen[@]}")" '
    BEGIN { n = split(seen_list, arr, "\n"); for (i = 1; i <= n; i++) skip[arr[i]] = 1 }
    NR == 1 { print; next }
    !($1 in skip)
  ' "$FAIL_LOG" > "$survivors"
  mv "$survivors" "$FAIL_LOG"
else
  printf 'url\treason\n' > "$FAIL_LOG"
fi
new=0 existing=0 failed=0
total=${#urls[@]}
i=0
while [ "$i" -lt "$total" ]; do
  batch=("${urls[@]:i:BATCH_SIZE}")
  out=$(bash -lc 'llmwiki ingest "$@"' _ "${batch[@]}" 2>&1) || true
  echo "$out"
  for u in "${batch[@]}"; do
    status=$(awk -F'\t' -v u="$u" '$3==u{print $2}' <<<"$out")
    case "$status" in
      new) new=$((new + 1)) ;;
      existing | exists) existing=$((existing + 1)) ;;
      *)
        failed=$((failed + 1))
        reason=$(grep -F "$u" "$KB_LOG" 2>/dev/null | tail -1) || true
        printf '%s\t%s\n' "$u" "${reason:-ingest failed, see $KB_LOG}" >> "$FAIL_LOG"
        ;;
    esac
  done
  i=$((i + BATCH_SIZE))
done

echo "new=$new existing=$existing failed=$failed skipped=$skipped"
