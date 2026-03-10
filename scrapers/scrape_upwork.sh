#!/bin/bash
# Quick runner for Upwork scraper with common filters

QUERY="${1:-copywriting}"
OUTPUT="${2:-jobs_$(date +%Y%m%d_%H%M%S).json}"

echo "Scraping Upwork for: $QUERY"
echo "Output: $OUTPUT"
echo ""

python3 /home/clawd/.openclaw/workspace/scrapers/upwork_scraper.py \
    --search "$QUERY" \
    --max 30 \
    --output "$OUTPUT" \
    --min-budget 50 \
    --max-proposals 20 \
    --exclude "expert" "agency" "team" "years experience"

echo ""
echo "Done. Check $OUTPUT for results."
